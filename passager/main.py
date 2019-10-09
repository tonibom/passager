#!/bin/python3
"""
This is the main that works as the entrance for the
passager software. It checks that the user inputted
valid credentials and handles the login of said user.
Core module is started up when a login is successful.
"""
import argparse

import passager.core
import passager.data_formats
import passager.interface
import passager.storage


def _account_verification():
    pass


def _arg_parser():
    # TODO: Parse args
    # TODO: "register", "login"
    pass


def _login():
    pass


def _print_usage():
    pass


def _register() -> str:
    pass


def run():
    # TODO: Grab args
    # TODO: Use storage to check that args are a legit user login
    # TODO: Else print usage
    # TODO: Finally; start core with the authenticated user
    pass
