import requests
import json

def get_github_user_data(username):
    # GitHub API URL for the user profile
    user_url = f"https://api.github.com/users/{username}"
    
    # Fetch user data
    user_response = requests.get(user_url)
    
    if user_response.status_code != 200:
        print(f"Error fetching user data: {user_response.status_code}")
        return None

    user_data = user_response.json()
    
    # Display some general profile data
    profile_info = {
        "Name": user_data.get("name"),
        "Username": user_data.get("login"),
        "Location": user_data.get("location"),
        "Public Repos": user_data.get("public_repos"),
        "Followers": user_data.get("followers"),
        "Following": user_data.get("following"),
        "Profile URL": user_data.get("html_url")
    }

    print("Profile Info:")
    print(json.dumps(profile_info, indent=4))

    # Fetch repositories
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_response = requests.get(repos_url)
    
    if repos_response.status_code != 200:
        print(f"Error fetching repos data: {repos_response.status_code}")
        return None

    repos_data = repos_response.json()

    print("\nRepositories Info:")
    for repo in repos_data:
        repo_info = {
            "Repo Name": repo["name"],
            "Description": repo["description"],
            "Language": repo["language"],
            "Stars": repo["stargazers_count"],
            "Forks": repo["forks_count"],
            "Repo URL": repo["html_url"]
        }
        print(json.dumps(repo_info, indent=4))


# Example usage:
username = "kalyands123"  # Replace with the GitHub username you want to extract data from
get_github_user_data(username)
