from pprint import pprint
import requests
import time
import json

APP_ID = 6988731

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

user_input = input()
groups_list = []


class User:
    def __init__(self, token):
        self.token = token

    def get_params(self):
        params = dict(
            access_token=self.token,
            v='5.95',
            extended=1,
            count=1000,
            fields=['members_count']
        )
        if type(user_input) == int:
            params['user_id'] = {user_input}
        else:
            params['screen_name'] = {user_input}
        return params

    def get_users_groups(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params
        )
        response_json = response.json()['response']['items']
        print('-')
        return response_json

    def get_unique_groups(self):
        users_groups = self.get_users_groups()
        for group in users_groups:
            group_dict = {
                'name': group['name'],
                'gid': group['id'],
                'members_count': group['members_count']
            }
            params = dict(
                access_token=self.token,
                v='5.95',
                group_id={group['id']},
                count=1000,
                filter='friends'
            )
            try:
                response = requests.get(
                    'https://api.vk.com/method/groups.getMembers',
                    params
                )
            except:
                time.sleep(3)
            else:
                response_json = response.json()
                if response_json['response']['count'] == 0:
                    groups_list.append(group_dict)
            finally:
                print('-')

        with open('groups.json', 'w') as file:
            json.dump(groups_list, file, ensure_ascii=False, indent=2)

        with open('groups.json') as file:
            groups_json = json.load(file)
            pprint(groups_json)


if __name__ == '__main__':
    user1 = User(TOKEN)
    user1.get_unique_groups()
