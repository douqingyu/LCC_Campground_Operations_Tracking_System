"""Script to generate password hashes for LCC Issue Tracker initial user accounts.

This script generates bcrypt password hashes for:
- 20 visitors
- 5 helpers
- 2 administrators

Each user account must have a unique password with at least 8 characters and a mix of character types.
"""
from collections import namedtuple
from flask import Flask
from flask_bcrypt import Bcrypt

UserAccount = namedtuple('UserAccount', ['username', 'password'])

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

# Initial user accounts for LCC Issue Tracker
users = [
    # Visitors (20)
    UserAccount('visitor1', 'LCCvisitor1@2025'),
    UserAccount('visitor2', 'LCCvisitor2@2025'),
    UserAccount('visitor3', 'LCCvisitor3@2025'),
    UserAccount('visitor4', 'LCCvisitor4@2025'),
    UserAccount('visitor5', 'LCCvisitor5@2025'),
    UserAccount('visitor6', 'LCCvisitor6@2025'),
    UserAccount('visitor7', 'LCCvisitor7@2025'),
    UserAccount('visitor8', 'LCCvisitor8@2025'),
    UserAccount('visitor9', 'LCCvisitor9@2025'),
    UserAccount('visitor10', 'LCCvisitor10@2025'),
    UserAccount('visitor11', 'LCCvisitor11@2025'),
    UserAccount('visitor12', 'LCCvisitor12@2025'),
    UserAccount('visitor13', 'LCCvisitor13@2025'),
    UserAccount('visitor14', 'LCCvisitor14@2025'),
    UserAccount('visitor15', 'LCCvisitor15@2025'),
    UserAccount('visitor16', 'LCCvisitor16@2025'),
    UserAccount('visitor17', 'LCCvisitor17@2025'),
    UserAccount('visitor18', 'LCCvisitor18@2025'),
    UserAccount('visitor19', 'LCCvisitor19@2025'),
    UserAccount('visitor20', 'LCCvisitor20@2025'),

    # Helpers (5)
    UserAccount('helper1', 'LCChelper1@2025'),
    UserAccount('helper2', 'LCChelper2@2025'),
    UserAccount('helper3', 'LCChelper3@2025'),
    UserAccount('helper4', 'LCChelper4@2025'),
    UserAccount('helper5', 'LCChelper5@2025'),

    # Administrators (2)
    UserAccount('admin1', 'LCCadmin1@2025'),
    UserAccount('admin2', 'LCCadmin2@2025')
]

print('Username | Password | Hash | Password Matches Hash')
print('-' * 100)

for user in users:
    password_hash = flask_bcrypt.generate_password_hash(user.password)
    password_matches_hash = flask_bcrypt.check_password_hash(password_hash, user.password)
    print(f'{user.username} | {user.password} | {password_hash.decode()} | {password_matches_hash}')