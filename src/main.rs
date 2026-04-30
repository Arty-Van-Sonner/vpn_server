use anyhow::Result;
use clap::Parser;
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use tokio::{net::UdpSocket, signal};
use tracing::{info, warn};

#[derive(Debug, Clone, Serialize, Deserialize)]
struct PacketHeader {
    version: u8,
    session_id: u32,
    payload_len: u16,
}

#[derive(Debug, Parser)]
#[command(author, version, about)]
struct Args {
    #[arg(long, default_value = "0.0.0.0:51820")]
    bind: SocketAddr,
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter("info")
        .with_target(false)
        .compact()
        .init();

    let args = Args::parse();
    let socket = UdpSocket::bind(args.bind).await?;
    info!("Tunnel node is listening on {}", args.bind);

    let mut buffer = [0_u8; 2048];
    loop {
        tokio::select! {
            _ = signal::ctrl_c() => {
                info!("Shutdown signal received");
                break;
            }
            recv = socket.recv_from(&mut buffer) => {
                let (len, addr) = recv?;
                if len < 7 {
                    warn!("Dropping short packet from {}", addr);
                    continue;
                }

                let header = parse_header(&buffer[..7]);
                info!(
                    "Packet received: peer={}, session_id={}, bytes={}",
                    addr,
                    header.session_id,
                    len
                );

                // Placeholder for encryption/decryption and TUN forwarding.
                let _ = socket.send_to(&buffer[..len], addr).await?;
            }
        }
    }

    Ok(())
}

fn parse_header(input: &[u8]) -> PacketHeader {
    let session_id = u32::from_be_bytes([input[1], input[2], input[3], input[4]]);
    let payload_len = u16::from_be_bytes([input[5], input[6]]);
    PacketHeader {
        version: input[0],
        session_id,
        payload_len,
    }
}
