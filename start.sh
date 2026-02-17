#!/bin/bash
# Start tailscaled in userspace mode with a SOCKS5 listener
tailscaled --tun=userspace-networking --socks5-server=localhost:1080 &

sleep 5

# Connect and FORCE all traffic through your home exit node
tailscale up --authkey=${TS_AUTHKEY} --exit-node=${HOME_PC_IP} --exit-node-allow-lan-access=true

# CRITICAL: Verify the connection is working
echo "Testing proxy connection..."
curl --socks5-hostname localhost:1080 https://ifconfig.me
# This should print your ALEXANDRIA home IP, not a RunPod IP.

python -u /handler.py
