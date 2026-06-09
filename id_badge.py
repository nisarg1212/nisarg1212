import urllib.request
import json

def generate_badge():
    # We don't need active stats for this ultra-minimalist typographic layout,
    # but we run the request to keep the script structure identical.
    url = "https://api.github.com/users/nisarg1212"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
    except Exception:
        pass

    svg = """<svg width="800" height="120" viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Text Color Gradient -->
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#c084fc" /> <!-- soft violet -->
      <stop offset="100%" stop-color="#22d3ee" /> <!-- vibrant cyan -->
    </linearGradient>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&amp;family=Plus+Jakarta+Sans:wght@500&amp;display=swap');
      .name-text {
        font-family: 'Cinzel', serif;
        font-size: 38px;
        font-weight: 700;
        fill: url(#text-grad);
        letter-spacing: 6px;
      }
      .title-text {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        font-size: 11px;
        font-weight: 500;
        fill: #64748b;
        letter-spacing: 4px;
      }
    </style>
  </defs>

  <!-- Centered Luxury Typography -->
  <g transform="translate(400, 50)">
    <!-- Name -->
    <text x="0" y="0" text-anchor="middle" class="name-text">NISARG BHATT</text>
    
    <!-- Divider Line -->
    <line x1="-150" y1="16" x2="150" y2="16" stroke="#334155" stroke-width="1" opacity="0.6" />
    
    <!-- Title -->
    <text x="0" y="38" text-anchor="middle" class="title-text">PROBLEM SOLVER  •  SOFTWARE ENGINEER</text>
  </g>
</svg>"""

    with open("id_badge.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_badge()






