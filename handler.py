import os
import requests
import subprocess
import runpod

# Replace with your actual Alexandria PC's Tailscale IP
HOME_PC_IP = os.environ.get('HOME_PC_IP', '100.x.y.z') 

def download_audio(url):
    """
    Downloads YouTube audio through the Alexandria Proxy with human cookies.
    """
    filename = "audio.mp3"
    cookie_file = "youtube_cookies.txt"

    # --- 1. NETWORK & PROXY CHECK ---
    # This verifies if Tailscale is actually routing us through Woodlawn.
    try:
        # We use socks5h to resolve DNS at your home, not in the datacenter.
        proxies = {'https': 'socks5h://127.0.0.1:1080'}
        current_ip = requests.get('https://ifconfig.me', proxies=proxies, timeout=15).text.strip()
        print(f"✅ NETWORK CHECK: Worker is appearing as IP: {current_ip}")
    except Exception as e:
        print(f"❌ NETWORK CHECK FAILED: Proxy unreachable or Tailscale down. Error: {e}")

    # --- 2. FETCH FRESH COOKIES FROM BRIDGE ---
    try:
        print(f"Fetching fresh cookies from Mako Bridge at {HOME_PC_IP}...")
        r = requests.get(f'http://{HOME_PC_IP}:8080/get-cookies', timeout=15)
        if r.status_code == 200:
            with open(cookie_file, 'wb') as f:
                f.write(r.content)
            print("✅ Cookies updated from Alexandria bridge.")
        else:
            print(f"⚠️ Bridge returned error {r.status_code}. Using cached/none.")
    except Exception as e:
        print(f"⚠️ Failed to connect to Mako Bridge: {e}")

    # --- 3. DOWNLOAD VIA YT-DLP ---
    # --proxy socks5h ensures DNS and Data both go through your house IP.
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "--cookies", cookie_file,
        "--proxy", "socks5h://127.0.0.1:1080", 
        "-o", filename,
        "--no-playlist",
        url
    ]
    
    print(f"Starting download: {url}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ YT-DLP ERROR: {result.stderr}")
        raise Exception(f"Download failed: {result.stderr}")
        
    print("✅ Download complete.")
    return filename

# --- RUNPOD HANDLER LOGIC ---

def handler(job):
    """The main entry point for RunPod jobs."""
    job_input = job['input']
    video_url = job_input.get('url')
    
    if not video_url:
        return {"error": "No URL provided."}

    try:
        # Download
        audio_path = download_audio(video_url)
        
        # ... Your existing Whisper/Diarization logic goes here ...
        # (e.g., result = model.transcribe(audio_path))
        
        return {"status": "success", "transcript": "Sample transcript text..."}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Start the serverless worker
runpod.serverless.start({"handler": handler})
