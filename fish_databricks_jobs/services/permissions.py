import json
from enum import Enum

import requests
from requests import HTTPError


class AccessType(str, Enum):
    USER = 'user'
    PRINCIPAL = 'principal'
    GROUP = 'group'

    def access_name(self):
        _access_names = {AccessType.USER: 'user_name',
                         AccessType.PRINCIPAL: 'service_principal_name',
                         AccessType.GROUP: 'group_name'}
        return _access_names[self]

    def label(self):
        _lables = {AccessType.USER: 'User',
                   AccessType.PRINCIPAL: 'Service principal',
                   AccessType.GROUP: 'Group'}
        return _lables[self]


class Level(str, Enum):
    CAN_VIEW = 'can_view'
    CAN_MANAGE = 'can_manage'
    CAN_MANAGE_RUN = 'can_manage_run'

    def label(self):
        _lables = {Level.CAN_VIEW: 'Can View',
                   Level.CAN_MANAGE: 'Can Manage',
                   Level.CAN_MANAGE_RUN: 'Can Manage Run'}
        return _lables[self]


class Permission():
    def __init__(self, name: str, type: AccessType, level: Level):
        self.name = name
        self.level = level
        self.type = type

    def json(self):
        return {self.type.access_name(): self.name, 'permission_level': self.level.name}


class PermissionsService():
    def __init__(self, host, token):
        self.host = host
        self.token = token

    def assign_permission(self, job_id, permission: Permission):
        url = f"{self.host}/api/2.0/permissions/jobs/{job_id}"
        data = {'access_control_list': [permission.json()]}
        # print(data)

        try:
            response = requests.patch(url=url, auth=('token', self.token), json=data)
            response.raise_for_status()
        except HTTPError as http_error:
            print(json.dumps(json.loads(response.text), indent=2))
            # error_message = response.json()['message']
            # print(error_message)
            raise http_error
        except Exception as error:
            print(f'Other error occured: {error}')
            raise error
