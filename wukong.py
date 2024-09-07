import requests
import time
from colorama import Fore, Style, init

init()

print(f"{Fore.BLUE}")
print("               WUKONG AUTO CLEAR TASK            ")
print("__________ ________    ___________________ _________")
print("\\______   \\_____  \\  /   _____|_   _____//   _____/")
print(" |       _/ /   |   \\ \\_____  \\ |    __)_ \\_____  \\ ")
print(" |    |   \\/    |    \\/        \\|        \\/        \\")
print(" |____|_  /\\_______  /_______  /_______  /_______  /")
print("        \\/         \\/        \\/        \\/        \\/ ")
print("                                                         ")
print("           https://github.com/Kapaljetz666/              ")
print("              https://discord.gg/3Bpcexn6                ")
print("                  AIRDROP INDONESIA BOT                ")
print(f"{Style.RESET_ALL}")

def read_tokens_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]
            return tokens
    except Exception as e:
        print(f"{Fore.RED}Failed to read tokens from file: {e}{Style.RESET_ALL}")
        return []

def check_missions(token):
    url = "https://uat-api.sunkong.cloud/v1/missions"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{Fore.RED}Failed to retrieve missions: Please check your data.txt{Style.RESET_ALL}")
        return None

def complete_mission(token, mission_id):
    url = f"https://uat-api.sunkong.cloud/v1/missions/complete/{mission_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        detail = response.json().get('detail', response.text)
        mission_name = mission_name_map.get(mission_id, 'Unknown Mission')
        print(f"{Fore.RED}Failed to complete mission '{mission_name}': {response.status_code} {detail}{Style.RESET_ALL}")
        return None

def claim_mission(token, mission_id):
    url = f"https://uat-api.sunkong.cloud/v1/missions/claim/{mission_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        detail = response.json().get('detail', response.text)
        mission_name = mission_name_map.get(mission_id, 'Unknown Mission')
        print(f"{Fore.RED}Failed to claim mission '{mission_name}': {response.status_code} {detail}{Style.RESET_ALL}")
        return None

def claim_rewards(token):
    url = "https://uat-api.sunkong.cloud/v1/missions/rewards"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        detail = response.json().get('detail', response.text)
        print(f"{Fore.RED}Failed to claim rewards: {response.status_code} {detail}{Style.RESET_ALL}")
        return None

def print_mission_titles(missions):
    if missions:
        print("All Missions Unclaim:")
        for mission in missions:
            mission_title = mission.get('title', 'No Title')
            print(f"Title: {mission_title}")
    else:
        print("No missions available.")

def print_invite_missions(missions):
    if missions:
        for mission in missions:
            mission_type = mission.get('type', 'Unknown Type')
            if mission_type == 'invite':
                mission_id = mission.get('id')
                mission_name = mission.get('title', 'No Title')
                mission_status = mission.get('status', 'No Status')
                print(f"ID: {mission_id}, Name: {mission_name}, Status: {mission_status}")

def auto_clear_task(token):
    last_six_digits = token[-6:]
    print(f"{Fore.CYAN}Using token: *****{last_six_digits}{Style.RESET_ALL}")

    missions = check_missions(token)
    
    if missions:
        print_mission_titles(missions)
        
        global mission_name_map
        mission_name_map = {mission.get('id'): mission.get('title', 'Unknown Mission') for mission in missions}

        for mission in missions:
            mission_id = mission.get('id')
            mission_name = mission_name_map.get(mission_id, 'Unknown Mission')
            if mission_id:
                time.sleep(5)
                print(f"Attempting to complete mission '{mission_name}'...")
                completion_result = complete_mission(token, mission_id)
                if completion_result:
                    print(f"Attempting to claim mission '{mission_name}'...")
                    claim_result = claim_mission(token, mission_id)
                    
                    if claim_result:
                        print(f"{Fore.GREEN}Mission '{mission_name}' completed and claimed successfully!{Style.RESET_ALL}")
                        time.sleep(5)
                    else:
                        print(f"{Fore.RED}Mission '{mission_name}' completed but failed to claim.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Mission '{mission_name}' could not be completed.{Style.RESET_ALL}")
        
        print("Attempting to claim rewards...")
        rewards = claim_rewards(token)
        if rewards:
            print(f"{Fore.GREEN}Rewards claimed successfully: {rewards}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No rewards to claim or an error occurred.{Style.RESET_ALL}")

token_file_path = "token.txt"
tokens = read_tokens_from_file(token_file_path)

print(f"{Fore.CYAN}Total of accounts: {len(tokens)}{Style.RESET_ALL}")

if tokens:
    for token in tokens:
        auto_clear_task(token)
else:
    print(f"{Fore.RED}Failed to get tokens. Please check your data.txt file.{Style.RESET_ALL}")
