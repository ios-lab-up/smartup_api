
import os
import requests
import csv
import subprocess
import json


gh_token = os.environ.get("GH_TOKEN")

if gh_token is None:
    print("GitHub token is not set. Exiting.")
    exit(1)

owner = "iOS-Lab-UP"
repo = "juegaElPollo"


def run_command(command_list, cwd=None):
    try:
        subprocess.run(command_list, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running: {' '.join(command_list)}")
        print(str(e))

def get_all_commits(owner, repo, branch_name, last_sha, gh_token):
    commits = []
    page = 1
    while True:
        if last_sha:
            commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch_name}&since={last_sha}&page={page}&per_page=100"
        else:
            commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch_name}&page={page}&per_page=100"
        
        headers = {"Authorization": f"token {gh_token}"}
        response = requests.get(commits_url, headers=headers)
        data = response.json()
        
        if not data:  # No more commits to fetch
            break

        commits.extend(data)
        page += 1  # Next page

    return commits

# Set global git config (Only need to set these once per machine)
run_command(['git', 'config', '--global', 'user.email', '0241823@up.edu.mx'])
run_command(['git', 'config', '--global', 'user.name', 'HeinrichGomTag'])

# Clone the repository to get last_shas.json if it exists
run_command(['git', 'clone', f"https://{gh_token}@github.com/{owner}/{repo}.git"])

# Load previous SHAs from the repository (if it exists)
try:
    with open(f"{repo}/last_shas.json", "r") as f:
        last_shas = json.load(f)
except FileNotFoundError:
    last_shas = {}

with open("commits.csv", "w", newline='') as csvfile:
    fieldnames = ["Branch", "Commit SHA", "Author", "Date", "Message"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    branches_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    headers = {"Authorization": f"token {gh_token}"}
    branches_response = requests.get(branches_url, headers=headers).json()

    for branch in branches_response:
        branch_name = branch["name"]
        last_sha = last_shas.get(branch_name)

        commits_response = get_all_commits(owner, repo, branch_name, last_sha, gh_token)

        for commit in commits_response:
            writer.writerow({
                "Branch": branch_name,
                "Commit SHA": commit["sha"],
                "Author": commit["commit"]["author"]["name"],
                "Date": commit["commit"]["author"]["date"],
                "Message": commit["commit"]["message"]
            })

        if commits_response:
            last_shas[branch_name] = commits_response[0]["sha"]

# Save the latest SHAs to a local file inside the repo
with open(f"{repo}/last_shas.json", "w") as f:
    json.dump(last_shas, f)

# Copy commits.csv into the repo
run_command(['cp', 'commits.csv', f"{repo}/commits.csv"])

# Commit and push the updated commits.csv and last_shas.json to the repository
try:
    run_command(['git', 'add', '.'], cwd=repo)
    run_command(['git', 'commit', '-m', 'Added CSV and updated JSON'], cwd=repo)
    run_command(['git', 'push', 'origin', 'main'], cwd=repo)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running a subprocess: {e}")

