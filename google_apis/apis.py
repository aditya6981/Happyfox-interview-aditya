import requests


def list_messages(creds):
    headers = {
        'Authorization': f"Bearer {creds.token}",
        'Accept': 'application/json'
    }
    response = requests.get(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages', 
        headers=headers)

    messages = response.json().get('messages', [])

    return messages


def get_message(creds, message_id):
    headers = {
        'Authorization': f"Bearer {creds.token}",
        'Accept': 'application/json'
    }
    msg_response = requests.get(
        f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}', 
        headers=headers)

    msg = msg_response.json()

    return msg


def modify_message(creds, message_id, data):
    headers = {
        'Authorization': f"Bearer {creds.token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    requests.post(
        f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify',
        headers=headers, json=data)
