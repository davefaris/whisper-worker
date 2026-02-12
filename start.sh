#!/bin/bash

# Start Tailscale in userspace mode
tailscaled --tun=userspace-networking --socks5-server=localhost:1080 &

# Wait for it to spin up
sleep 5

# USE PLACEHOLDERS: These are filled by RunPod at runtime
tailscale up --authkey=${TS_AUTHKEY} --exit-node=${HOME_PC_IP} --exit-node-allow-lan-access=true

echo "Mako Gateway Connected: Routing through Alexandria office."

# Launch the worker
python -u /handler.py
