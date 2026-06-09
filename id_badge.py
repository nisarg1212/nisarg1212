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
    
    name = user_data.get('name', 'Nisarg Bhatt')
    if not name: name = "Nisarg Bhatt"
    
    svg = f"""<svg width="800" height="140" viewBox="0 0 800 140" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap');
      .card-bg {{ fill: #0b0f19; stroke: #1e293b; stroke-width: 1; }}
      .name {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 26px; font-weight: 800; fill: #ffffff; letter-spacing: -0.5px; }}
      .title {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 14px; font-weight: 500; fill: #94a3b8; }}
      .status-text {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 11px; font-weight: 500; fill: #64748b; }}
      .stat-num {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 24px; font-weight: 700; fill: #f8fafc; }}
      .stat-label {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; font-size: 10px; font-weight: 600; fill: #475569; letter-spacing: 1px; }}
    </style>
  </defs>

  <!-- Card Background -->
  <rect width="800" height="140" rx="8" class="card-bg" />

  <!-- Left Side: Profile & Role Info -->
  <text x="40" y="55" class="name">{name}</text>
  <text x="40" y="82" class="title">Backend Architect &amp; Software Engineer</text>
  
  <!-- Status Pill -->
  <circle cx="45" cy="106" r="3.5" fill="#10b981" />
  <text x="56" y="110" class="status-text">Active &amp; building new systems</text>

  <!-- Divider -->
  <line x1="510" y1="25" x2="510" y2="115" stroke="#1e293b" stroke-width="1.5" />

  <!-- Right Side: Developer Stats -->
  <!-- Level -->
  <g transform="translate(540, 0)">
    <text x="0" y="60" class="stat-num">{level}</text>
    <text x="0" y="80" class="stat-label">SYSTEM LEVEL</text>
  </g>

  <!-- Repositories -->
  <g transform="translate(670, 0)">
    <text x="0" y="60" class="stat-num">{user_data.get('public_repos', 0)}</text>
    <text x="0" y="80" class="stat-label">REPOSITORIES</text>
  </g>
</svg>"""

    with open("id_badge.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_badge()


