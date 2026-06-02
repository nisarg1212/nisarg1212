import datetime
import urllib.request
import json

def generate_desk():
    # 1. Get current time in IST (UTC+5:30)
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    hour = now.hour

    # 2. Theme settings based on time
    if 6 <= hour < 18:
        # Day theme
        wall_color = "#f4f4f5"
        window_sky = "#87CEEB"
        celestial_body = '<circle cx="450" cy="80" r="20" fill="#FFD700" />' # Sun
        screen_glow = "#ffffff"
        lamp_on = False
    else:
        # Night theme
        wall_color = "#2c3e50"
        window_sky = "#0f172a"
        # Crescent Moon
        celestial_body = '<circle cx="450" cy="80" r="15" fill="#fef08a" /><circle cx="455" cy="75" r="15" fill="#0f172a" />' 
        screen_glow = "#38bdf8"
        lamp_on = True

    # 3. Check GitHub for recent activity (coffee steam)
    is_steaming = False
    try:
        req = urllib.request.Request("https://api.github.com/users/nisarg1212/events/public", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            events = json.loads(response.read().decode())
            if len(events) > 0:
                last_event_time = datetime.datetime.strptime(events[0]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                # If the last public event was within the last 2 hours
                if (datetime.datetime.utcnow() - last_event_time).total_seconds() < 7200: 
                    is_steaming = True
    except:
        pass

    steam_svg = ""
    if is_steaming:
        steam_svg = """
  <path d="M140 180 Q 130 160 140 140 T 140 120" stroke="#cbd5e1" stroke-width="3" fill="none" opacity="0.6" >
    <animate attributeName="d" values="M140 180 Q 130 160 140 140 T 140 120; M140 180 Q 150 160 140 140 T 140 120; M140 180 Q 130 160 140 140 T 140 120" dur="3s" repeatCount="indefinite"/>
  </path>
  <path d="M155 185 Q 145 165 155 145 T 155 125" stroke="#cbd5e1" stroke-width="3" fill="none" opacity="0.4" >
    <animate attributeName="d" values="M155 185 Q 165 165 155 145 T 155 125; M155 185 Q 145 165 155 145 T 155 125; M155 185 Q 165 165 155 145 T 155 125" dur="4s" repeatCount="indefinite"/>
  </path>"""

    # 4. Compile SVG
    svg = f"""<svg width="600" height="300" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="screenGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{screen_glow}" stop-opacity="0.2" />
      <stop offset="100%" stop-color="{screen_glow}" stop-opacity="0" />
    </radialGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Wall -->
  <rect width="600" height="300" fill="{wall_color}" />
  
  <!-- Window -->
  <rect x="350" y="40" width="180" height="120" rx="10" fill="{window_sky}" stroke="#475569" stroke-width="6" />
  {celestial_body}
  <!-- Window Pane Lines -->
  <line x1="440" y1="40" x2="440" y2="160" stroke="#475569" stroke-width="4" />
  <line x1="350" y1="100" x2="530" y2="100" stroke="#475569" stroke-width="4" />

  <!-- Desk -->
  <rect x="50" y="220" width="500" height="80" fill="#8B4513" rx="5" filter="url(#shadow)"/>
  <rect x="30" y="220" width="540" height="15" fill="#A0522D" rx="5" />

  <!-- Laptop -->
  <rect x="230" y="140" width="140" height="90" rx="5" fill="#334155" />
  <rect x="235" y="145" width="130" height="80" rx="3" fill="#0f172a" />
  <rect x="210" y="230" width="180" height="8" rx="2" fill="#94a3b8" />
  <!-- Screen Glow -->
  <rect x="200" y="100" width="200" height="150" fill="url(#screenGlow)" pointer-events="none" />
  
  <!-- Code lines on screen -->
  <line x1="245" y1="160" x2="290" y2="160" stroke="#10b981" stroke-width="3" stroke-linecap="round"/>
  <line x1="245" y1="170" x2="310" y2="170" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
  <line x1="255" y1="180" x2="320" y2="180" stroke="#e2e8f0" stroke-width="3" stroke-linecap="round"/>
  <line x1="255" y1="190" x2="280" y2="190" stroke="#f43f5e" stroke-width="3" stroke-linecap="round"/>

  <!-- Coffee Mug -->
  <rect x="130" y="190" width="35" height="40" rx="3" fill="#e2e8f0" />
  <path d="M165 200 C 175 200, 175 220, 165 220" stroke="#e2e8f0" stroke-width="4" fill="none" />
  {steam_svg}

  <!-- Lamp -->
  <path d="M480 230 L 500 150" stroke="#475569" stroke-width="4" />
  <path d="M490 150 Q 500 130 510 150" fill="#cbd5e1" />
  { '<circle cx="500" cy="150" r="8" fill="#fef08a" filter="url(#shadow)" />' if lamp_on else '' }
  <rect x="470" y="225" width="20" height="5" fill="#475569" />

  <!-- Info Text -->
  <text x="580" y="20" font-family="monospace" font-size="12" fill="#94a3b8" text-anchor="end">Status Desk | Time: {now.strftime('%I:%M %p')} IST</text>
  { '<text x="580" y="40" font-family="monospace" font-size="10" fill="#10b981" text-anchor="end">[Recently Committed ☕]</text>' if is_steaming else '' }
</svg>"""

    with open("live_desk.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    generate_desk()
