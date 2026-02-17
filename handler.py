def download_audio(url):
    filename = "audio.mp3"
    
    # 1. Fetch fresh cookies from your Alexandria PC
    # Replace '100.x.y.z' with your actual Home PC Tailscale IP
    try:
        r = requests.get('http://100.112.213.123:8080/get-cookies', timeout=15)
        with open('youtube_cookies.txt', 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(f"Warning: Cookie fetch failed: {e}. Worker may be blocked.")

    # 2. FORCE yt-dlp through the Tailscale tunnel (localhost:1080)
    # We use 'socks5h' to ensure DNS is also resolved through your home network
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "--cookies", "youtube_cookies.txt",
        "--proxy", "socks5h://127.0.0.1:1080", 
        "-o", filename,
        url
    ]
    
    print("Starting download through Alexandria proxy...")
    subprocess.run(cmd, check=True)
    return filename
