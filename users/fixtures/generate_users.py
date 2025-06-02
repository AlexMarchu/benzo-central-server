import json
import string
import random
import os
import sys

import django
from django.contrib.auth.hashers import make_password

project_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), os.pardir)
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, LoyaltyCard

def generate_password(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_username(name):
    return ''.join(name.lower().split())

def import_data():
    path = os.path.join(os.path.dirname(__file__), 'loyalty_card.json')

    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f'Error while reading file: {e}')
    
    users_data = list()

    for card_data in data['LoyaltyCard']:
        first_name, last_name = map(str.capitalize, card_data['holder_name'].split())
        username = create_username(card_data['holder_name'])
        password = generate_password()

        loyalty_card = LoyaltyCard.objects.create(
            number=card_data['number'],
            balance=card_data['balance']
        )

        user = User.objects.create(
            username=username,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            loyalty_card=loyalty_card
        )

        users_data.append({
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'loyalty_card_number': card_data['number']
        })

        print(f'User {first_name} {last_name} created successfully')

    output_path = os.path.join(os.path.dirname(__file__), 'users.json')
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(users_data, file, ensure_ascii=False, indent=2)

    print(f'Created {len(users_data)} users and loyalty_cards')

if __name__ == '__main__':
    import_data()
