import requests
import datetime

# কনফিগারেশন
SOURCES = [
    "https://raw.githubusercontent.com/srhady/tapmad-bd/refs/heads/main/tapmad_bd.json",
    "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json",
    "https://raw.githubusercontent.com/srhady/bingstream/refs/heads/main/playlist.json",
    "https://raw.githubusercontent.com/srhady/data/refs/heads/main/playlist.json"
]
M3U_SOURCE = "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u"
FALLBACK_LOGO = "https://camo.githubusercontent.com/93929647baabb50606ccf95056c8ff42b3f2f9249c5364fa1e0f8b7dcef395f3/68747470733a2f2f626469786970747662642e636f6d2f6c6f676f2e706e67"
FALLBACK_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4"

def generate():
    # এখানে লজিক লিখবেন যা JSON/M3U পার্স করে M3U ফরম্যাটে সাজাবে
    # FIFA world cup ক্যাটাগরি উপরে রেখে বাকিগুলো সাজাবে
    header = f"""#EXTM3U
# Playlist update dates and times: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Playlist owner: STAR OTT BD
# Playlist Creator: MD shakib Hasan
# What's app: +8801610598422
# Telegram: https://t.me/ibstvbd
# Our official partner : IBS TV. STAR SHARE. OPPLEX.
"""
    # ফাইল রাইট করার কোড এখানে হবে...
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write(header)
        # আপনার লজিক অনুযায়ী চ্যানেল লুপ চালিয়ে এখানে লিখুন

generate()
