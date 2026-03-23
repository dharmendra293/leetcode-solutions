import requests
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("LEETCODE_USERNAME")

url = "https://leetcode.com/graphql"

query = """
query getRecentSubmissions($username: String!) {
  recentSubmissionList(username: $username) {
    title
    titleSlug
    lang
    timestamp
  }
}
"""

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    json={"query": query, "variables": {"username": username}},
    headers=headers
)

data = response.json()

# Debug print
print(data)

# Safety check
if "data" not in data:
    print("Error fetching data. Check username or connection.")
    exit()

submissions = data["data"]["recentSubmissionList"]

if not os.path.exists("solutions"):
    os.mkdir("solutions")

for sub in submissions:
    title = sub["title"]
    slug = sub["titleSlug"]
    lang = sub["lang"]

    filename = f"solutions/{slug}.{lang.lower()}"

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(f"# {title}\n")

print("Files created successfully!")

# Git automation
os.system("git add .")
os.system('git commit -m "Auto update LeetCode solutions"')
os.system("git push")