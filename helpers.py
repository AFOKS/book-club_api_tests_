import requests


def create_club(api_url, headers, club_body):
    response = requests.post(f"{api_url}/clubs/", headers=headers, json=club_body)
    return response