import urllib.request
import json
import datetime

def test_fetch():
    try:
        # Fetch user profile details
        user_url = "https://api.github.com/users/nisarg1212"
        req = urllib.request.Request(user_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
        
        # Calculate uptime (time since account creation)
        created_at = datetime.datetime.strptime(user_data['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.datetime.utcnow()
        diff = now - created_at
        years = diff.days // 365
        remaining_days = diff.days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        
        uptime_str = f"{years} year(s), {months} month(s), {days} day(s)"
        print("Uptime:", uptime_str)
        print("Followers:", user_data.get('followers', 0))
        print("Public Repos:", user_data.get('public_repos', 0))
        
        # Fetch repos to count stars
        repos_url = "https://api.github.com/users/nisarg1212/repos?per_page=100"
        req_repos = urllib.request.Request(repos_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_repos) as response_repos:
            repos_data = json.loads(response_repos.read().decode())
        
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        print("Total Stars:", total_stars)
        
    except Exception as e:
        print("Error fetching details:", e)

if __name__ == "__main__":
    test_fetch()
