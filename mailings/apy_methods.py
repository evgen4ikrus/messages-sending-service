import requests


def create_message(host, id, text, mailing_id, create_at, status):
    url = f"{host}/api/messages/"
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


def delete_message(host, message_id):
    url = f"{host}/api/messages/{message_id}"
    response = requests.delete(url)
    response.raise_for_status()


def get_messages_by_status(host, status):
    url = f"{host}/api/messages/"
    params = {'status': status}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_mailing_by_id(host, mailing_id):
    url = f"{host}/api/mailings/{mailing_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_clients(host, tag_id, mobile_operator_code_id):
    url = f"{host}/api/clients/"
    params = {
        'tag': tag_id,
        'mobile_operator_code': mobile_operator_code_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
