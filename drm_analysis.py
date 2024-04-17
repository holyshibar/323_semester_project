import requests


class DRMAnalysis:
    def __init__(self, game_name):
        self.game_name = game_name
        self.base_url = "https://www.pcgamingwiki.com/w/api.php"

    # Retrieves relevant data in order to analyze DRM information for a given Steam game
    def get_pcgamingwiki_info(self):
        # Assembles the necessary parameters for the PCGamingWiki API request
        params = {
            "action": "parse",
            "format": "json",
            "page": self.game_name,
            "prop": "wikitext"
        }
        print("game name:", self.game_name)
        response = requests.get(self.base_url, params=params) # Sends a get request to the API
        if response.status_code == 200: # Checks to see if there was an error upon request, if not, start extracting data
            data = response.json()
            if 'error' in data:
                print("Error: ", data['error']['info'])
                return None, None
            elif 'parse' in data:
                wikitext = data['parse']['wikitext']['*']
                availability_section, denuvo_detected = self.extract_availability_section(
                    wikitext)
                return availability_section, denuvo_detected
        else:
            return None, None

    # From the WikiText, extracts the availability section by finding the start and end indexes
    def extract_availability_section(self, wikitext):
        start_index = wikitext.find("==Availability==")
        if start_index == -1:
            return "Availability section not found", False

        end_index = wikitext.find("==", start_index + 16)
        if end_index == -1:
            return wikitext[start_index:], "Denuvo" in wikitext

        return wikitext[start_index:end_index], "Denuvo" in wikitext

    # Based on the extracted availability section, examines Steams' availability and usage of the game's DRM info
    def analyze_steam_availability(self, availability_section):
        analysis_result = ""
        if availability_section:
            lines = availability_section.split('\n')
            for line in lines:
                parts = [part.strip() for part in line.split('|')]
                print("parts:", parts)
                if len(parts) > 1 and parts[1] == 'Steam':
                    print(
                        f"Steam detected in the line: {parts[1]} ** THIS ONE ***")
                    drm_status = parts[3]
                    if 'Steam' in drm_status:
                        analysis_result += "Requires Steam\n"
                    elif 'DRM-free' in drm_status:
                        analysis_result += "Doesn't use DRM\n"
                    else:
                        analysis_result += "Cannot decrypt DRM information: " + drm_status + "\n"
                    break
        return analysis_result


'''
# manual usage for TESTING

# game_name = "Palworld"  # expected no drm
# game_name = "Visions of Mana"  # expected denuvo
# game_name = "Factorio"  # expected steam
game_name = "Totally Accurate Battle Simulator"  # expected steam

# Instantiate the DRMAnalysis class with the game name
drm_analysis = DRMAnalysis(game_name)

# Call the method to get the PCGamingWiki information
availability_section, denuvo_detected = drm_analysis.get_pcgamingwiki_info()

# Output the results
if denuvo_detected:
    print("Denuvo Anti-Tamper detected.")
elif availability_section:
    # Call the method to analyze the Steam availability and DRM status
    analysis_result = drm_analysis.analyze_steam_availability(
        availability_section)
    print("Analysis Result:")
    print(analysis_result)  # This will print the analysis result
else:
    print("Availability section not found or failed to retrieve data for", game_name)
 '''
