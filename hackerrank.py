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
            print(f"Failed to retrieve data: {page.status_code}")
            return {}

        soup = BeautifulSoup(page.content, 'html.parser')

        # Final output data
        data = {
            'username': username,
            'profile_name': None,
            'location': None,
            'badges': {},
            'certificates': [],
            'education': []
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

            # Location
            location_div = profile_info_div.find('p', {'class': 'profile-country'})
            if location_div:
                data['location'] = location_div.get_text(strip=True)

        # Extract profile data
        profile_data_div = soup.find('div', {'class': 'profile-right-pane'})
        if profile_data_div is None:
            print(f"No profile data div found for user {username}.")
            return data

        # Badges
        badges_div = profile_data_div.find('section', {'class': 'section-card hacker-badges'})
        if badges_div:
            badges_items = badges_div.find_all('div', {'class': 'hacker-badge'})
            for badge in badges_items:
                badge_name = badge.find('text').get_text(strip=True)
                star_div = badge.find('g', {'class': 'star-section'})
                count_star = star_div.find_all('svg', {'class': 'badge-star'}) if star_div else []
                stars = f"{len(count_star)} star"
                data['badges'][badge_name] = stars

        # Verified Skills (Certificates)
        skill_div = profile_data_div.find('div', {'class': 'hacker-certificates'})
        if skill_div:
            certificates = skill_div.find_all('a')
            for certificate in certificates:
                certificate_name = certificate.find('h2', {'class': 'certificate-heading'}).get_text(strip=True)
                data['certificates'].append(certificate_name)

        # Education
        education_div = profile_data_div.find('ul', {'class': 'ui-timeline'})
        education_tags = education_div.find_all('li') if education_div else []
        for tag in education_tags:
            content = tag.find('div', {'class': 'timeline-item-content'})
            if content:
                institute = content.find('h2').get_text(strip=True)
                stream = content.find('p').get_text(strip=True)
                data['education'].append({'institute': institute, 'stream': stream})

        return data

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Example usage
if __name__ == "__main__":
    usernames = ['kalyands8050', 'vigneshherao']  # Replace with the desired usernames
    for username in usernames:
        stats = get_hackerrank_stats(username)
        print(stats)
