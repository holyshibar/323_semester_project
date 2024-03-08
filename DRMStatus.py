import requests


def extract_availability_section(wikitext):
    start_index = wikitext.find("==Availability==")
    if start_index == -1:
        return "Availability section not found"

    # Attempt to find the start of the next section by searching for "=="
    # 16 characters offset to move beyond "==Availability=="
    end_index = wikitext.find("==", start_index + 16)

    # If there's no next section, just return from the Availability section to the end of the text
    if end_index == -1:
        return wikitext[start_index:]

    # Extract and return the Availability section including up to the start of the next section
    denuvo_detected = "Denuvo" in wikitext

    return wikitext[start_index:end_index], denuvo_detected


def analyze_steam_availability(availability_section):
    lines = availability_section.split('\n')
    for line in lines:
        parts = [part.strip() for part in line.split('|')]
        print("parts:", parts)
        if len(parts) > 1 and parts[1] == 'Steam':
            print(f"Steam detected in the line: {parts[1]} ** THIS ONE ***")
            drm_status = parts[3]  # Check DRM status in the fourth part
            if 'Steam' in drm_status:
                print("Uses Steam DRM")
            elif 'DRM-free' in drm_status:
                print("Doesn't use DRM")
            else:
                print("Cannot decrypt DRM information:", drm_status)
            break  # Assuming only the first occurrence is relevant
        else:
            print("No Steam detected in this line.")


def get_pcgamingwiki_info(game_name):
    pcgamingwiki_url = f"https://www.pcgamingwiki.com/w/api.php?action=parse&format=json&page={game_name}&prop=wikitext"
    response = requests.get(pcgamingwiki_url)
    if response.status_code == 200:
        data = response.json()
        wikitext = data['parse']['wikitext']['*']
        availability_section, denuvo_detected = extract_availability_section(
            wikitext)

        if denuvo_detected:
            print("Cannot decrypt DRM information: Denuvo Anti-Tamper")
            return  # Skip further analysis if Denuvo Anti-Tamper is detected

        if availability_section:
            print(availability_section)
            analyze_steam_availability(availability_section)
        else:
            print("Availability section not found.")
    else:
        print(f"Failed to retrieve data for {game_name}")


# Example usage
game_name = "Lethal Company"
get_pcgamingwiki_info(game_name)
print("Done")
