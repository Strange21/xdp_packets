#![no_std]
#![no_main]
#![allow(nonstandard_style, dead_code)]

use aya_ebpf::{
    bindings::xdp_action, macros::{map, xdp}, maps::{RingBuf}, programs::XdpContext
};
use aya_log_ebpf::info;
use myapp_common::NwEvent;

use core::mem;
use network_types::{
    eth::{EthHdr, EtherType},
    ip::{IpProto, Ipv4Hdr},
};

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    unsafe { core::hint::unreachable_unchecked() }
}

// #[map(name = "BLOCKLIST")] // 
// static mut BLOCKLIST: HashMap<u32, u32> =
//     HashMap::<u32, u32>::with_max_entries(1024, 0);

#[map]
static NwEvent: RingBuf = RingBuf::with_byte_size(256 * 1024, 0); // 256 KB

#[xdp]
pub fn xdp_firewall(ctx: XdpContext) -> u32 {
    match try_xdp_firewall(ctx) {
        Ok(ret) => ret,
        Err(_) => xdp_action::XDP_ABORTED,
    }
}

#[inline(always)]
unsafe fn ptr_at<T>(ctx: &XdpContext, offset: usize) -> Result<*const T, ()> {
    let start = ctx.data();
    let end = ctx.data_end();
    let len = mem::size_of::<T>();

    if start + offset + len > end {
        return Err(());
    }

    let ptr = (start + offset) as *const T;
    Ok(&*ptr)
}

// 
// fn block_ip(address: u32) -> bool {
//     unsafe { BLOCKLIST.get(&address).is_some() }
// }

fn try_xdp_firewall(ctx: XdpContext) -> Result<u32, ()> {
    let ethhdr: *const EthHdr = unsafe { ptr_at(&ctx, 0)? };
    match unsafe { (*ethhdr).ether_type } {
        EtherType::Ipv4 => {}
        _ => return Ok(xdp_action::XDP_PASS),
    }

    let ipv4hdr: *const Ipv4Hdr = unsafe { ptr_at(&ctx, EthHdr::LEN)? };
    let source =  u32::from_be(unsafe { (*ipv4hdr).src_addr });
    let dest =  u32::from_be(unsafe { (*ipv4hdr).dst_addr });
    // let protocol =  u32::from_be(unsafe { (*ipv4hdr).proto });

    // let action = xdp_action::XDP_PASS;
    
    // let action = if block_ip(source) {
    //     xdp_action::XDP_DROP;
    //     "Blocked"
    // } else {
    //     xdp_action::XDP_PASS;
    //     "Pass"
    // };
    if let Some(mut buf) = NwEvent.reserve::<NwEvent>(0) {
        // let len = ctx.skb.len() as usize;

        unsafe { (*buf.as_mut_ptr()).src_addr = source };
        unsafe { (*buf.as_mut_ptr()).dest_addr = dest };

        buf.submit(0);
    }
    info!(
        &ctx,
        "AF_INET src address: {:i}, dest address: {:i}", source, dest,
    );
    
    // info!(&ctx, "SRC: {:i}, DEST: {}", source, dest );

    Ok(2)
}
