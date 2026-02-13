def download_audio(url):
    filename = "audio.mp3"
    
    # 1. Tell yt-dlp to use the Tailscale proxy on localhost:1080
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "--proxy", "socks5://127.0.0.1:1080", 
        "-o", filename,
        url
    ]
    subprocess.run(cmd, check=True)
    return filename
