import urllib.request
import json
import random
import datetime

def generate_badge():
    url = "https://api.github.com/users/nisarg1212"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
    except Exception:
        user_data = {"name": "Nisarg", "login": "nisarg1212", "public_repos": 99, "followers": 42}

    # Level math
    level = (user_data.get("public_repos", 0) * 10) + user_data.get("followers", 0) + 1200
    
    name = user_data.get('name', 'Nisarg Bhatt')
    if not name: name = "Nisarg"
    
    # Hex/Timestamp details
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    barcode_svg = ""
    x = 640
    random.seed(42) 
    for _ in range(15):
        w = random.randint(1, 4)
        barcode_svg += f'<rect x="{x}" y="160" width="{w}" height="40" fill="#00ffcc" opacity="0.8"/>\n'
        x += w + random.randint(2, 4)

    svg = f"""<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow">
        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
        <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#cbd5e1" stroke-width="0.5" stroke-opacity="0.03"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="800" height="250" fill="#030712" rx="10" />
  <rect width="800" height="250" fill="url(#grid)" rx="10" />
  
  <!-- Frame Brackets (Sci-Fi Targeting UI) -->
  <path d="M 25 55 L 25 25 L 55 25" fill="none" stroke="#00ffcc" stroke-width="2" filter="url(#glow)"/>
  <path d="M 775 55 L 775 25 L 745 25" fill="none" stroke="#00ffcc" stroke-width="2" filter="url(#glow)"/>
  <path d="M 25 195 L 25 225 L 55 225" fill="none" stroke="#00ffcc" stroke-width="2" filter="url(#glow)"/>
  <path d="M 775 195 L 775 225 L 745 225" fill="none" stroke="#00ffcc" stroke-width="2" filter="url(#glow)"/>

  <!-- Decorative Hex / Coordinates -->
  <text x="35" y="218" font-family="'Courier New', monospace" font-size="10" fill="#475569">SYS.INIT. {now}</text>
  <text x="640" y="218" font-family="'Courier New', monospace" font-size="10" fill="#475569">SEC-CLR: Lvl {level} // V.1.0</text>

  <!-- Main Data Display -->
  <text x="60" y="80" font-family="'Courier New', monospace" font-size="14" fill="#00ffcc" font-weight="bold" letter-spacing="2" filter="url(#glow)">>_ UPLINK ESTABLISHED</text>
  
  <text x="60" y="125" font-family="'Courier New', monospace" font-size="42" fill="#f8fafc" font-weight="bold" letter-spacing="4">{name.upper()}</text>
  <text x="65" y="155" font-family="'Courier New', monospace" font-size="16" fill="#94a3b8" letter-spacing="3">ADVANCED BACKEND &amp; AI ENGINEER</text>

  <!-- Connecting Lines -->
  <line x1="65" y1="180" x2="350" y2="180" stroke="#00ffcc" stroke-width="1" opacity="0.4" />
  <circle cx="355" cy="180" r="3" fill="#00ffcc" filter="url(#glow)" />

  <!-- Minimal Barcode Right -->
  {barcode_svg}
  
  <!-- Side Data / Terminal readout -->
  <text x="640" y="70" font-family="'Courier New', monospace" font-size="12" fill="#64748b">AUTH: VERIFIED</text>
  <text x="640" y="90" font-family="'Courier New', monospace" font-size="12" fill="#64748b">NODE: {user_data.get('login', 'NISARG1212').upper()}</text>
  <rect x="640" y="105" width="80" height="2" fill="#00ffcc" filter="url(#glow)" opacity="0.8" />
  <rect x="725" y="105" width="10" height="2" fill="#00ffcc" filter="url(#glow)" opacity="0.8" />
</svg>
"""

    with open("id_badge.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_badge()
