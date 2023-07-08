import requests


def create_message(home_url, id, text, mailing_id, create_at, status):
    url = f"{home_url}/api/messages/"
    data = {
        "id": id,
        "text": text,
        "create_at": create_at,
        "mailing": mailing_id,
        "status": status,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def delete_message(home_url, message_id):
    url = f"{home_url}/api/messages/{message_id}"
    response = requests.delete(url)
    response.raise_for_status()


def get_messages_by_status(home_url, status):
    url = f"{home_url}/api/messages/"
    params = {'status': status}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_mailing_by_id(home_url, mailing_id):
    url = f"{home_url}/api/mailings/{mailing_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_clients(home_url, tag_id, mobile_operator_code_id):
    url = f"{home_url}/api/clients/"
    params = {
        'tag': tag_id,
        'mobile_operator_code': mobile_operator_code_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
