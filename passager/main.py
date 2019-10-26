#!/bin/python3
"""
This is the main that works as the entrance for the
passager software. It checks that the user inputted
valid credentials and handles the login of said user.
Core module is started up when a login is successful.
"""
import argparse
import logging


import passager.core as core
import passager.interface as interface
import passager.storage as storage

from passager.data_formats import MainAccount

_logger = logging.getLogger(__name__)


def _arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage and train logging in with your passwords")
    parser.add_argument("command",
                        choices=["login", "register"],
                        default="login",
                        help="command you wish to execute",)
    return parser


def _login():
    # Use interface to get input for username and password
    main_account = None

    while True:
        username, password = interface.login()

        if username == "" and password == "":
            interface.logout()
            return
        if username == "" or password == "":
            interface.invalid_login()
            continue

        main_account = storage.validate_main_login(username, password)

        if main_account is not None:
            # Login successful
            break
        interface.invalid_login()

    # Finally; start core with the authenticated user
    core.run(main_account)


def _register() -> bool:

    # Get existing usernames
    unavailable_usernames = storage.get_usernames()

    while True:
        username = interface.main_account_register_username(unavailable_usernames)

        if username is None:
            # Registration canceled
            break

        password = interface.main_account_register_password(username)
        if password is None:
            # Registration canceled
            break

        main_account = MainAccount(username, password)
        storage.store_main_account(main_account)
        return True
    return False


def run():
    logging.basicConfig(level=logging.INFO)

    arg_parser = _arg_parser()
    args = arg_parser.parse_args()

    if args.command == "login":
        _login()
    elif args.command == "register":
        if _register():
            # If account was registered successfully, enter login screen
            _login()


if __name__ == "__main__":
    run()
