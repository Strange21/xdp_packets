#![no_std]

#[repr(C)]
#[derive(Debug)]
pub struct NwEvent {
    pub src_addr: u32,
    pub dest_addr: u32,
}