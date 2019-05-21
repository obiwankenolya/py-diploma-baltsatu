from pprint import pprint
import requests
import time

APP_ID = 6988731

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

user_input = input()


class User:
    def __init__(self, token):
        self.token = token

    def get_params(self):
        if type(user_input) == int:
            return dict(
                access_token=self.token,
                v='5.95',
                user_id={user_input},
                extended=1,
                count=1000,
                fields=['members_count']
        )
        else:
            return dict(
                access_token=self.token,
                v='5.95',
                screen_name={user_input},
                extended=1,
                count=1000,
                fields=['members_count'],
            )

    def get_users_groups(self):
        params = self.get_params()
        groups = requests.get(
            'https://api.vk.com/method/groups.get',
            params
        )
        groups_json = groups.json()['response']['items']
        for item in groups_json:
            item.pop('is_closed')
            item.pop('photo_100')
            item.pop('photo_200')
            item.pop('photo_50')
            item.pop('screen_name')
            item.pop('type')
            print('-')
        return groups_json

    def get_unique_groups(self):
        groups = self.get_users_groups()
        for group in groups:
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
                if response_json['response']['count'] > 0:
                    groups.remove(group)
                    print('-')
        pprint(groups)
        print('-')


user1 = User(TOKEN)
user1.get_unique_groups()
