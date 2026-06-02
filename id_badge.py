import urllib.request
import json
import base64
import random

def generate_badge():
    url = "https://api.github.com/users/nisarg1212"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
    except Exception:
        user_data = {"name": "Nisarg", "login": "nisarg1212", "public_repos": 99, "followers": 42}

    # Fetch and base64 encode the user's GitHub avatar so it embeds directly into the SVG
    avatar_url = user_data.get("avatar_url", "")
    try:
        req_av = urllib.request.Request(avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_av) as response:
            av_data = response.read()
            av_b64 = base64.b64encode(av_data).decode('utf-8')
            avatar_href = "data:image/png;base64," + av_b64
    except Exception:
        avatar_href = ""

    # Generate a static "fake" barcode
    barcode_svg = ""
    x = 220
    random.seed(42) 
    for _ in range(35):
        w = random.randint(2, 7)
        barcode_svg += f'<rect x="{x}" y="180" width="{w}" height="40" fill="#38bdf8" />\n'
        x += w + random.randint(2, 5)

    # Some arbitrary "Level" math for the Sci-Fi element
    level = (user_data.get("public_repos", 0) * 10) + user_data.get("followers", 0) + 1200
    name = user_data.get('name', 'Nisarg Bhatt')
    if not name: name = "Nisarg"

    svg = f"""<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e1b4b" />
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#f43f5e" />
    </linearGradient>
    <filter id="glow">
        <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
        <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
    
    <!-- Clip path to round the corners of the base64 image -->
    <clipPath id="avatarClip">
      <rect x="40" y="50" width="140" height="140" rx="10" />
    </clipPath>
  </defs>

  <!-- Background base -->
  <rect width="800" height="250" rx="15" fill="url(#bg)" stroke="url(#accent)" stroke-width="4"/>
  
  <!-- Top accent bar -->
  <rect x="0" y="0" width="800" height="15" fill="url(#accent)" opacity="0.9" />
  
  <!-- Top Right Title -->
  <text x="770" y="45" font-family="'Courier New', monospace" font-size="14" fill="#64748b" text-anchor="end" letter-spacing="2">GLOBAL SECURITY CLEARANCE /// LEVEL {level}</text>

  <!-- Avatar glowing box -->
  <rect x="35" y="45" width="150" height="150" fill="#000" stroke="#38bdf8" stroke-width="3" rx="12" filter="url(#glow)" />
  """
    
    if avatar_href:
        svg += f'<image x="40" y="50" width="140" height="140" href="{avatar_href}" clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice" />\n'
    else:
        svg += f'<rect x="40" y="50" width="140" height="140" fill="#334155" rx="8" />\n'

    svg += f"""
  <!-- Grid overlay -->
  <g stroke="#334155" stroke-width="1" opacity="0.4">
      <line x1="20" y1="10" x2="20" y2="240" />
      <line x1="200" y1="10" x2="200" y2="240" />
  </g>

  <!-- Data text -->
  <text x="220" y="85" font-family="'Courier New', monospace" font-size="32" font-weight="bold" fill="#f8fafc" letter-spacing="2">ID: {user_data.get('login', 'NISARG1212').upper()}</text>
  <text x="220" y="115" font-family="'Courier New', monospace" font-size="18" fill="#cbd5e1">NAME: {name.upper()}</text>
  <text x="220" y="145" font-family="'Courier New', monospace" font-size="16" fill="#38bdf8">ROLE: ADVANCED BACKEND &amp; AI ENGINEER</text>

  <!-- Status indicator -->
  <circle cx="225" cy="165" r="5" fill="#10b981" filter="url(#glow)"/>
  <text x="240" y="170" font-family="'Courier New', monospace" font-size="14" fill="#10b981">STATUS: OPERATIONAL [ACTIVE UPLINK]</text>

  <!-- Barcode -->
  <g opacity="0.85">
      {barcode_svg}
  </g>

  <!-- Cyberpunk Decals -->
  <rect x="730" y="195" width="40" height="20" fill="none" stroke="#f43f5e" stroke-width="2" />
  <rect x="740" y="200" width="20" height="10" fill="#f43f5e" />
  <rect x="220" y="235" width="300" height="3" fill="#cbd5e1" opacity="0.2" />
</svg>
"""

    with open("id_badge.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_badge()
