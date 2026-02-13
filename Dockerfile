# Base Image: RunPod's official PyTorch image
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# 1. Install System Tools & Tailscale
RUN apt-get update && \
    apt-get install -y ffmpeg git curl iptables kmod && \
    curl -fsSL https://tailscale.com/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# 2. Copy dependencies
COPY requirements.txt .

# 3. Install Python Dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy Application Code & Startup Script
COPY handler.py .
COPY start.sh /start.sh

# 5. Fix permissions and Line Endings (Surgical Fix)
RUN chmod +x /start.sh && sed -i 's/\r$//' /start.sh

# 6. Use the Startup Script as the Entrypoint
ENTRYPOINT [ "/start.sh" ]
