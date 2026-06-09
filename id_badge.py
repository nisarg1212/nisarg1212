import urllib.request
import json

def generate_badge():
    url = "https://api.github.com/users/nisarg1212"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
    except Exception:
        user_data = {"name": "Nisarg Bhatt", "login": "nisarg1212", "public_repos": 27, "followers": 0}

    # Maintain original level math
    level = (user_data.get("public_repos", 0) * 10) + user_data.get("followers", 0) + 1200
    repos = user_data.get('public_repos', 0)
    
    name = user_data.get('name', 'Nisarg Bhatt')
    if not name: name = "Nisarg Bhatt"
    
    svg = f"""<svg width="800" height="180" viewBox="0 0 800 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Radial Gradients with drifting animations -->
    <radialGradient id="orb-blue" cx="30%" cy="40%" r="60%">
      <animate attributeName="cx" values="30%;45%;30%" dur="14s" repeatCount="indefinite" />
      <animate attributeName="cy" values="40%;60%;40%" dur="14s" repeatCount="indefinite" />
      <stop offset="0%" stop-color="#2563eb" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#2563eb" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="orb-violet" cx="70%" cy="60%" r="60%">
      <animate attributeName="cx" values="70%;55%;70%" dur="18s" repeatCount="indefinite" />
      <animate attributeName="cy" values="60%;40%;60%" dur="18s" repeatCount="indefinite" />
      <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#7c3aed" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="orb-indigo" cx="50%" cy="50%" r="50%">
      <animate attributeName="cx" values="50%;60%;50%" dur="22s" repeatCount="indefinite" />
      <animate attributeName="cy" values="50%;30%;50%" dur="22s" repeatCount="indefinite" />
      <stop offset="0%" stop-color="#4f46e5" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#4f46e5" stop-opacity="0" />
    </radialGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;800&amp;display=swap');
      .card-bg {{ fill: #030712; stroke: #1e293b; stroke-width: 1.2; }}
      .name-text {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 34px; font-weight: 800; fill: #ffffff; letter-spacing: 2px; }}
      .title-text {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 13px; font-weight: 500; fill: #22d3ee; letter-spacing: 3px; opacity: 0.95; }}
      .stats-text {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 10px; font-weight: 500; fill: #475569; letter-spacing: 2px; }}
    </style>
  </defs>

  <!-- Card Background -->
  <rect width="800" height="180" rx="10" class="card-bg" />

  <!-- Ambient Pulsing Orbs -->
  <rect width="800" height="180" fill="url(#orb-blue)" rx="10" />
  <rect width="800" height="180" fill="url(#orb-violet)" rx="10" />
  <rect width="800" height="180" fill="url(#orb-indigo)" rx="10" />

  <!-- Centered Typographic Info -->
  <g transform="translate(400, 85)">
    <!-- Name -->
    <text x="0" y="-5" text-anchor="middle" class="name-text">NISARG BHATT</text>
    
    <!-- Title -->
    <text x="0" y="26" text-anchor="middle" class="title-text">PROBLEM SOLVER  •  SOFTWARE ENGINEER</text>
  </g>

  <!-- Bottom Stats line -->
  <text x="400" y="152" text-anchor="middle" class="stats-text">LEVEL {level}  •  {repos} REPOSITORIES</text>
</svg>"""

    with open("id_badge.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_badge()




