from enum import Enum


class UserRoles(str, Enum):
    user = 'User'
    admin = 'Admin'
    superuser = 'Superuser'
