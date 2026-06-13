import requests
import datetime
import re

# সোর্স লিঙ্ক
M3U_SOURCES = {
    "Ayna": "https://raw.githubusercontent.com/ibstvofficial/Live-events/refs/heads/main/playlist.m3u",
    "IPTVOrg": "https://iptv-org.github.io/iptv/index.m3u",
    "Akash": "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash_live.m3u"
}

# ক্যাটাগরি ম্যাপিং
CATEGORY_MAP = {
    "FIFA World cup": ["SOMOY", "BTV", "T SPORTS", "FIFA"],
    "News": ["NEWS", "BBC", "CNN", "AL JAZEERA", "CHANNEL 24", "JOMUNA", "INDEPENDENT"],
    "Sports": ["SPORTS", "CRICKET", "FOOTBALL", "GOLF", "TEN", "ESPN"],
    "Bangladesh": ["BD", "BANGLA", "DHAKA", "CHANNEL I", "ATN"],
    "Music": ["MUSIC", "SONG", "GAAN", "MTV"],
    "Kids": ["KIDS", "CARTOON", "NICK", "DISNEY", "POGO", "CBEEBIES"],
    "Movie": ["MOVIE", "FILM", "HBO", "STAR MOVIES", "CINEMA"]
}

ORDERED_CATEGORIES = list(CATEGORY_MAP.keys())

def get_category(name, group):
    name_up = name.upper()
    group_up = (group or "").upper()
    
    for cat, keywords in CATEGORY_MAP.items():
        if any(k in name_up for k in keywords) or any(k in group_up for k in keywords):
            return cat
    return None

def fetch_m3u(url):
    channels = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        current_name = None
        current_logo = ""
        current_group = ""
        
        for line in response.iter_lines():
            if not line: continue
            line = line.decode('utf-8')
            
            if line.startswith("#EXTINF"):
                logo_match = re.search(r'tvg-logo="(.*?)"', line)
                group_match = re.search(r'group-title="(.*?)"', line)
                current_logo = logo_match.group(1) if logo_match else ""
                current_group = group_match.group(1) if group_match else ""
                current_name = line.split(',')[-1].strip()
                
            elif line.startswith("http"):
                if current_name:
                    cat = get_category(current_name, current_group)
                    if cat:
                        channels.append({
                            "name": current_name, 
                            "group": cat, 
                            "logo": current_logo, 
                            "url": line
                        })
                current_name = None 
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return channels

def write_m3u(all_channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Playlist update dates and times: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbdn")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # সর্টিং ও ডুপ্লিকেট রিমুভ
        all_channels.sort(key=lambda x: ORDERED_CATEGORIES.index(x['group']) if x['group'] in ORDERED_CATEGORIES else 99)
        
        seen_urls = set()
        for ch in all_channels:
            if ch['url'] not in seen_urls:
                f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n{ch["url"]}\n')
                seen_urls.add(ch['url'])

if __name__ == "__main__":
    final_channels = []
    for source_name, url in M3U_SOURCES.items():
        print(f"Fetching from {source_name}...")
        final_channels.extend(fetch_m3u(url))
    
    write_m3u(final_channels)
    print("Playlist generated successfully!")
                
