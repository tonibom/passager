#!/bin/python3
"""
Storage module is responsible for handling the data storage. Salting and hashing
is applied to the main account's information in order to ensure password
security. However, as this is a password manager, the service account passwords
need to be retrievable so hashing won't do. Encryption using the main account's
password as a base for the key is therefore used instead.
"""
import os

import passager.data_formats


def _decrypt(string: str, key: str) -> str:
    return string


def _encrypt(string: str, key: str) -> str:
    return string


def _generate_salt() -> str:
    # TODO: generate unique salt
    # Hint: Use os.urandom
    return ""


def load_password_hash(user: str, service: str) -> str:
    return ""


def salt_and_hash_new(password: str) -> str:
    # New as in password hasn't been salted and hashed before
    salt = _generate_salt()
    # TODO: hash
    hashed_pass = password
    return salt + hashed_pass


def salt_and_hash(password: str, salt: str) -> str:
    # TODO: hash
    hashed_pass = password
    return salt + hashed_pass


def store_password_hash(password: str, user: str, service: str):
    pass

