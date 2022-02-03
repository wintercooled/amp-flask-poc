import json

import requests
from flask import current_app


class BlockstreamAMPAPI:

    def get_auth_header():
        username = current_app.config['API_USERNAME']
        password = current_app.config['API_PASSWORD']
        token = BlockstreamAMPAPI.get_auth_token(username, password)
        return {'content-type': 'application/json', 'Authorization': f'token {token}'}

    def request_get(url, use_auth=True):
        api_url = current_app.config['API_URL']
        url = f'{api_url}/{url}'
        if use_auth:
            headers = BlockstreamAMPAPI.get_auth_header()
        else:
            headers = {'content-type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 403 or response.status_code == 404 or response.status_code == 400:
            raise PermissionError
        data = json.loads(response.text)
        return data

    def request_post(url, payload, use_auth=True):
        api_url = current_app.config['API_URL']
        url = f'{api_url}/{url}'
        if use_auth:
            headers = BlockstreamAMPAPI.get_auth_header()
        else:
            headers = {'content-type': 'application/json'}
        response = requests.post(
            url, data=json.dumps(payload), headers=headers)
        if response.status_code == 403 or response.status_code == 404 or response.status_code == 400:
            message = 'An error occured.'
            if response.text:
                data = json.loads(response.text)
                for value in data.values():
                    if isinstance(value, list):
                        message = message + f' {value[0]}.'
                    else:
                        message = message + f' {value}.'
            raise ValueError(message)
        data = json.loads(response.text)
        return data

    def get_auth_token(username, password):
        payload = {'username':  username, 'password': password}
        data = BlockstreamAMPAPI.request_post(
            'user/obtain_token', payload, False)
        return data['token']

    def assets():
        data = BlockstreamAMPAPI.request_get('assets')
        return data

    def asset(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}')
        return data

    def asset_summary(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}/summary')
        return data

    def asset_activities(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}/activities')
        return data

    def asset_ownerships(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}/ownerships')
        return data

    def asset_balance(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}/balance')
        return data

    def asset_utxos(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}/utxos')
        return data

    def asset_assignments(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}/assignments')
        return data

    def asset_distributions(asset_uuid):
        data = BlockstreamAMPAPI.request_get(f'assets/{asset_uuid}/distributions')
        return data

    def investors():
        data = BlockstreamAMPAPI.request_get('investors')
        return data

    def investor(investor_id):
        data = BlockstreamAMPAPI.request_get(f'investors/{investor_id}')
        return data

    def investors_add(name, gaid=None):
        # TODO: remove hardcoded false and use form to get if you like
        if gaid == '':
            gaid = None
        payload = {'is_company': False,
            'name': name,
            'GAID': gaid
        }
        data = BlockstreamAMPAPI.request_post('investors/add', payload)
        return data

    def gaid_balance(gaid):
        data = BlockstreamAMPAPI.request_get(f'gaids/{gaid}/balance')
        return data
