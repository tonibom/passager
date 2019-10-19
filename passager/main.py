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
        if username is None or password is None:
            interface.invalid_login()
            continue

        # TODO: Use storage to check that args are a legit user login
        main_account = storage.validate_main_login(username, password)

        if main_account is not None:
            # Login successful
            break
        interface.invalid_login()

    # Finally; start core with the authenticated user
    core.run(main_account)




def _register() -> str:
    pass


def run():
    logging.basicConfig(level=logging.DEBUG)

    arg_parser = _arg_parser()
    args = arg_parser.parse_args()

    if args.command == "login":
        _login()
    elif args.command == "register":
        _register()


if __name__ == "__main__":
    run()
