import requests
from bs4 import BeautifulSoup

def get_hackerrank_stats(username):
    try:
        url = f'https://www.hackerrank.com/profile/{username}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
        }

        # Make the request
        page = requests.get(url, headers=headers)
        if page.status_code != 200:
            print(f"Failed to retrieve data for {username}: {page.status_code}")
            return {}

        soup = BeautifulSoup(page.content, 'html.parser')

        # Final output data
        data = {
            'username': username,
            'profile_name': None,
            'badges': {},
            'certificates': [],
            'education': [],
            'skills': [],  # Add a field for skills
            'total_problems_solved': 0  # Track the total problems solved
        }

        # Extract profile information
        main_div = soup.find('div', {'id': 'content'})
        if main_div is None:
            print(f"No main div found for user {username}.")
            return data

        profile_info_div = main_div.find('div', {'class': 'profile-sidebar'})
        if profile_info_div:
            # Profile Name
            data['profile_name'] = profile_info_div.find('h1').get_text(strip=True)

        # Extract profile data
        profile_data_div = soup.find('div', {'class': 'profile-right-pane'})
        if profile_data_div is None:
            print(f"No profile data div found for user {username}.")
            return data

        # Extract skills
        skill_div = profile_data_div.find('div', {'class': 'hacker-certificates'})
        if skill_div:
            certificates = skill_div.find_all('a')
            for certificate in certificates:
                certificate_name = certificate.find('h2', {'class': 'certificate-heading'}).get_text(strip=True)
                data['certificates'].append(certificate_name)
                data['skills'].append(certificate_name)  # Assuming certificates represent skills

        # Total Problems Solved
        problems_div = profile_data_div.find('div', {'class': 'total-problems-solved'})
        if problems_div:
            try:
                data['total_problems_solved'] = int(problems_div.get_text(strip=True).split()[0])
            except ValueError:
                data['total_problems_solved'] = 0

        return data

    except requests.exceptions.RequestException as e:
        print(f"Request error for {username}: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred for {username}: {e}")
        return {}

def get_leetcode_graphql_data(username):
    url = 'https://leetcode.com/graphql'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    query = f'''
    {{
        matchedUser(username: "{username}") {{
            username
            profile {{
                realName
                reputation
                ranking
                countryName
            }}
            submitStats {{
                acSubmissionNum {{
                    difficulty
                    count
                }}
                totalSubmissionNum {{
                    count
                }}
            }}
        }}
    }}
    '''

    response = requests.post(url, json={'query': query}, headers=headers)

    if response.status_code != 200:
        print(f"HTTP Error {response.status_code} for user {username}")
        return None

    data = response.json()

    if 'errors' in data:
        print(f"Error fetching data for {username}: {data['errors']}")
        return None

    return data['data']

def match_skills(candidates, job_description_skills):
    matched_candidates = []

    for candidate in candidates:
        # Convert candidate skills to lowercase for matching
        candidate_skills = set(skill.lower() for skill in candidate.get('skills', []))
        # Find matched skills based on job description
        matched_skills = candidate_skills.intersection(job_description_skills)

        # Calculate rank starting from 1
        rank = len(matched_skills) + candidate.get('total_problems_solved', 0)
        if rank > 0:
            rank = rank  # Ensure rank is not zero

        matched_candidates.append({
            'username': candidate['username'],
            'profile_name': candidate['profile_name'],
            'matched_skills': list(matched_skills),
            'rank': rank,
            'total_problems_solved': candidate.get('total_problems_solved', 0)  # Add this for display
        })

    # Sort candidates by rank (higher is better)
    matched_candidates.sort(key=lambda x: x['rank'], reverse=True)

    # Adjust ranks to start from 1
    for idx, candidate in enumerate(matched_candidates):
        candidate['rank'] = idx + 1  # Set rank starting from 1

    return matched_candidates

# Example usage
if __name__ == "__main__":
    job_description_skills = {"python", "java", "c++", "javascript", "django", "machine learning", "data analysis"}  # Example job description skills
    usernames_hackerrank = ['kalyands8050', 'vigneshherao']  # Replace with desired usernames
    usernames_leetcode = ['kalyands', 'vigneshherao']  # Add more usernames as needed

    candidates_data = []

    # Fetch data from HackerRank
    for username in usernames_hackerrank:
        stats = get_hackerrank_stats(username)
        if stats:
            candidates_data.append(stats)

    # Fetch data from LeetCode
    for username in usernames_leetcode:
        print(f"Fetching data for {username}...")
        leetcode_data = get_leetcode_graphql_data(username)

        if leetcode_data:
            leetcode_username = leetcode_data['matchedUser']['username']
            leetcode_problems_solved = sum(stat['count'] for stat in leetcode_data['matchedUser']['submitStats']['acSubmissionNum'])
            for candidate in candidates_data:
                if candidate['username'] == leetcode_username:
                    candidate['total_problems_solved'] += leetcode_problems_solved  # Update the problems solved

    # Match skills and rank candidates
    ranked_candidates = match_skills(candidates_data, job_description_skills)

    # Print the ranked candidates
    for candidate in ranked_candidates:
        print(f"Username: {candidate['username']}, Profile Name: {candidate['profile_name']}, "
              f"Matched Skills: {candidate['matched_skills']}, Rank: {candidate['rank']}, "
              f"Total Problems Solved: {candidate['total_problems_solved']}")
