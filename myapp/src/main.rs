use anyhow::Context;
use aya::{
    include_bytes_aligned,
    maps::RingBuf,
    programs::{Xdp, XdpFlags},
    Ebpf,
};
use aya_log::EbpfLogger;
use clap::Parser;
use log::{info, warn};
use tokio::time::{sleep, Duration};
use std::{fmt::format, net::Ipv4Addr};
use tokio::net::UnixStream;
use tokio::io::AsyncWriteExt;

#[derive(Debug, Parser)]
struct Opt {
    #[clap(short, long, default_value = "eth0")]
    iface: String,
}

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    let opt = Opt::parse();

    env_logger::init();

    // This will include your eBPF object file as raw bytes at compile-time and load it at
    // runtime. This approach is recommended for most real-world use cases. If you would
    // like to specify the eBPF program at runtime rather than at compile-time, you can
    // reach for `Bpf::load_file` instead.
    // #[cfg(debug_assertions)]
    let mut bpf = Ebpf::load(include_bytes_aligned!(
        "../../target/bpfel-unknown-none/debug/myapp"
    ))?;
    // #[cfg(not(debug_assertions))]
    // let mut bpf = Bpf::load(include_bytes_aligned!(
    //     "../../target/bpfel-unknown-none/release/xdp-drop"
    // ))?;
    if let Err(e) = EbpfLogger::init(&mut bpf) {
        // This can happen if you remove all log statements from your eBPF program.
        warn!("failed to initialize eBPF logger: {}", e);
    }
    let program: &mut Xdp = bpf.program_mut("xdp_firewall").unwrap().try_into()?;
    program.load()?;
    program.attach("enp0s3", XdpFlags::default())
        .context("failed to attach the XDP program with default flags - try changing XdpFlags::default() to XdpFlags::SKB_MODE")?;

    let mut ring = RingBuf::try_from(bpf.map_mut("NwEvent").unwrap())?;
    let _ = ring.next();
    println!("got RingBuf array for network");
    let mut stream = UnixStream::connect("/home/nuc2kor/Desktop/ipc_new.sock").await?;

    // let mut packet_count_map = HashMap::<Ipv4Addr, NwCount>::default();
    loop {
        if let Some(item) = ring.next() {
            // Interpret bytes as u32 values representing IPv4 addresses
            let src_addr_bytes: [u8; 4] = item[..4].try_into().unwrap();
            let dest_addr_bytes: [u8; 4] = item[4..].try_into().unwrap();

            // Convert u8 arrays to u32 values
            let src_addr_u32 = u32::from_le_bytes(src_addr_bytes);
            let dest_addr_u32 = u32::from_le_bytes(dest_addr_bytes);

            // Convert u32 values to Ipv4Addr
            let src_addr = Ipv4Addr::from(src_addr_u32);
            let dest_addr = Ipv4Addr::from(dest_addr_u32);
            // tx.send(format!("Temp is: 100"));
            let message  = format!("Src address: {}, Dest address: {}", src_addr, dest_addr);
            stream.write_all(message.as_bytes()).await?;
            println!("Src address: {}, Dest address: {}", src_addr, dest_addr);
        }
    }
    // info!("Waiting for Ctrl-C...");
    // signal::ctrl_c().await?;
    // info!("Exiting...");

    // Ok(())
}
