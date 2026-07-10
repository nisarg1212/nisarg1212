import urllib.request
import json
import datetime
import os
import base64
from PIL import Image, ImageEnhance

def fetch_github_details():
    # Defaults in case of API failure
    uptime_str = "2 years, 2 months"
    public_repos = 22
    followers = 0
    total_stars = 0

    try:
        user_url = "https://api.github.com/users/nisarg1212"
        req = urllib.request.Request(user_url, headers={'User-Agent': 'AntigravityAgent/1.0'})
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
        
        created_at_str = user_data.get('created_at')
        if created_at_str:
            created_at = datetime.datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
            now = datetime.datetime.now(datetime.timezone.utc)
            created_at = created_at.replace(tzinfo=datetime.timezone.utc)
            diff = now - created_at
            
            years = diff.days // 365
            remaining_days = diff.days % 365
            months = remaining_days // 30
            days = remaining_days % 30
            
            uptime_str = f"{years} yr(s), {months} mo(s), {days} day(s)"
        
        public_repos = user_data.get('public_repos', public_repos)
        followers = user_data.get('followers', followers)

        repos_url = "https://api.github.com/users/nisarg1212/repos?per_page=100"
        req_repos = urllib.request.Request(repos_url, headers={'User-Agent': 'AntigravityAgent/1.0'})
        with urllib.request.urlopen(req_repos) as response_repos:
            repos_data = json.loads(response_repos.read().decode())
        
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        
    except Exception as e:
        print("Fallback to default stats due to API error:", e)

    return uptime_str, public_repos, followers, total_stars

def convert_image_to_ascii(image_path, is_dark_mode, width=40, height=20):
    if not os.path.exists(image_path):
        return []
    
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        
        # 1. Center-crop to square
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        right = (w + min_dim) / 2
        bottom = (h + min_dim) / 2
        img = img.crop((left, top, right, bottom))
        
        # Get background color from top-left corner
        bg_color = img.getpixel((0, 0))
        
        # 2. Boost contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.4)
        
        # 3. Resize to target ASCII grid
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Invert character map density based on Dark/Light mode
        if is_dark_mode:
            CHAR_MAP = " .:-=+*#%@"
        else:
            CHAR_MAP = "@%#*+=-:. "
        
        lines = []
        for y in range(height):
            line_parts = []
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                
                # Dynamic background subtraction (distance threshold to corner color)
                color_dist = ((r - bg_color[0])**2 + (g - bg_color[1])**2 + (b - bg_color[2])**2)**0.5
                if color_dist < 45:
                    line_parts.append('&#160;') # transparent space
                    continue
                
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                char_idx = int((gray / 256.0) * len(CHAR_MAP))
                char = CHAR_MAP[min(char_idx, len(CHAR_MAP) - 1)]
                
                # Escape XML characters
                if char == "<": char = "&lt;"
                elif char == ">": char = "&gt;"
                elif char == "&": char = "&amp;"
                elif char == " ": char = "&#160;"
                
                color_hex = f"#{r:02x}{g:02x}{b:02x}"
                line_parts.append(f'<tspan fill="{color_hex}">{char}</tspan>')
            lines.append("".join(line_parts))
        return lines
    except Exception as e:
        print("Error converting image:", e)
        return []

def generate_svg(filename, is_dark_mode, uptime, repos, followers):
    ascii_art_lines = convert_image_to_ascii("123_edited.jpg", is_dark_mode, 40, 20)

    # Backup ASCII art if conversion fails
    if not ascii_art_lines:
        ascii_art_lines = [
            "     _________________     ",
            "    |.---------------.|    ",
            "    ||               ||    ",
            "    ||   &gt;_ hello    ||    ",
            "    ||               ||    ",
            "    ||_______________||    ",
            "    /.-.-.-.-.-.-.-.-.\\    ",
            "   /.-.-.-.-.-.-.-.-.-.\\   ",
            "  /.-.-.-.-.-.-.-.-.-.-.\\  ",
            " /_______________________\\ ",
            "       \\_______/           "
        ]

    # Theme Specific Colors
    if is_dark_mode:
        bg = "#0d1117"
        border = "#30363d"
        header_bg = "#161b22"
        title = "#8b949e"
        text_primary = "#c9d1d9"
        ascii_fallback = "#94a3b8"
        user = "#58a6ff"
        host = "#3fb950"
        key = "#ffa657"
        val = "#a5d6ff"
        separator = "#30363d"
        color_black = "#161b22"
        color_white = "#8b949e"
        shadow_color = "#000000"
        shadow_opacity = "0.35"
    else:
        bg = "#ffffff"
        border = "#d0d7de"
        header_bg = "#e3e8ec"
        title = "#57606a"
        text_primary = "#24292f"
        ascii_fallback = "#475569"
        user = "#0969da"
        host = "#1a7f37"
        key = "#953800"
        val = "#0a3069"
        separator = "#d0d7de"
        color_black = "#24292f"
        color_white = "#57606a"
        shadow_color = "#000000"
        shadow_opacity = "0.08"

    svg_parts = []
    svg_parts.append('<svg width="650" height="310" viewBox="0 0 650 310" xmlns="http://www.w3.org/2000/svg">')
    
    svg_parts.append(f'''  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&amp;display=swap');

      .bg-card {{ fill: {bg}; stroke: {border}; stroke-width: 1px; rx: 8px; }}
      .header-bg {{ fill: {header_bg}; }}
      .title-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13px; font-weight: 500; fill: {title}; }}
      
      .ascii-text {{ font-family: 'Fira Code', monospace; font-size: 10px; fill: {ascii_fallback}; white-space: pre; letter-spacing: 0.5px; }}
      .stats-text {{ font-family: 'Fira Code', monospace; font-size: 13px; fill: {text_primary}; }}
      
      .user {{ fill: {user}; font-weight: bold; }}
      .host {{ fill: {host}; font-weight: bold; }}
      .key {{ fill: {key}; }}
      .val {{ fill: {val}; }}
      .separator {{ fill: {separator}; }}

      .cursor {{
        animation: blink 1s step-start infinite;
        fill: {text_primary};
      }}
      @keyframes blink {{
        50% {{ opacity: 0; }}
      }}
    </style>
    <filter id="card-shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="{shadow_color}" flood-opacity="{shadow_opacity}" />
    </filter>
  </defs>''')

    # Main Card
    svg_parts.append('  <rect width="648" height="308" x="1" y="1" class="bg-card" filter="url(#card-shadow)" />')
    
    # Header bar
    svg_parts.append('  <rect x="1" y="1" width="646" height="34" rx="7" class="header-bg" />')
    svg_parts.append('  <rect x="1" y="20" width="646" height="15" class="header-bg" />')
    
    # macOS window buttons
    svg_parts.append('  <circle cx="20" cy="18" r="5" fill="#ff5f56" />')
    svg_parts.append('  <circle cx="36" cy="18" r="5" fill="#ffbd2e" />')
    svg_parts.append('  <circle cx="52" cy="18" r="5" fill="#27c93f" />')
    
    # Title text
    svg_parts.append('  <text x="325" y="22" class="title-text" text-anchor="middle">nisarg@terminal: ~</text>')

    # Left Column (Image / ASCII Art)
    svg_parts.append('  <text x="20" y="65" class="ascii-text">')
    for i, line in enumerate(ascii_art_lines):
        dy = "0" if i == 0 else "11"
        svg_parts.append(f'    <tspan x="20" dy="{dy}">{line}</tspan>')
    svg_parts.append('  </text>')

    # Right Column (Stats)
    svg_parts.append('  <text x="290" y="70" class="stats-text">')
    # Customized hostname prompt
    svg_parts.append('    <tspan x="290" dy="0"><tspan class="user">nisarg</tspan>@<tspan class="host">afterfiveyears.life</tspan>:~$ <tspan class="val">neofetch</tspan><tspan class="cursor">█</tspan></tspan>')
    svg_parts.append('    <tspan x="290" dy="14" class="separator">-------------------</tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">💻 OS</tspan>: <tspan class="val">Windows 11 / WSL</tspan></tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">🌐 Host</tspan>: <tspan class="val">nisarg.is-a.dev</tspan></tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">⏱️ Uptime</tspan>: <tspan class="val">{uptime}</tspan></tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">🐚 Shell</tspan>: <tspan class="val">zsh / powershell</tspan></tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">📝 Editor</tspan>: <tspan class="val">Cursor / VS Code</tspan></tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">🛠️ Tech</tspan>: <tspan class="val">Python, Django, FastAPI, React</tspan></tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">📦 Repos</tspan>: <tspan class="val">{repos}</tspan></tspan>')
    svg_parts.append(f'    <tspan x="290" dy="18"><tspan class="key">👥 Followers</tspan>: <tspan class="val">{followers}</tspan></tspan>')
    svg_parts.append('  </text>')

    # Terminal Color blocks
    colors = [color_black, "#ff5f56", "#27c93f", "#ffbd2e", "#58a6ff", "#d370e3", "#38bdf8", color_white]
    for idx, color in enumerate(colors):
        x = 290 + (idx * 24)
        svg_parts.append(f'  <rect x="{x}" y="260" width="20" height="15" fill="{color}" rx="2" />')

    svg_parts.append('</svg>')

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

def main():
    uptime, repos, followers, stars = fetch_github_details()
    generate_svg("id_badge_light.svg", False, uptime, repos, followers)
    generate_svg("id_badge_dark.svg", True, uptime, repos, followers)

if __name__ == "__main__":
    main()
