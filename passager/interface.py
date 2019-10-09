#!/bin/python3
"""
Interface module is responsible for displaying the user interface to the user
and receiving the required input from the user. The user input is validated
here and returned back to the caller.
Currently the only implementation is going to be CLI, but GUI might be implemented
later on.
"""
from typing import Optional

import passager.data_formats


def login() -> Optional[passager.data_formats.MainAccount]:
    # Optional, because might fail
    pass


def logout():
    # Python garbage collection regarding the accounts?
    pass


def main_account_add() -> Optional[passager.data_formats.MainAccount]:
    # Optional because might fail
    # Account registration
    pass


def main_account_change_password():
    # TODO: Ask for password again to validate user

    # These can be put into own function in order to be used in service as well
    # TODO: Ask for new password
    # TODO: Check password strength

    pass


def main_account_remove():
    pass


def main_menu() -> Optional[str]:
    """User interface for the main menu structure. Provides the user the options
    to choose from and asks what the user wants to do. User inputs their choice,
    this selection is validated and responded to.
        Valid -> response to user + return appropriate command to be handled in core
        Invalid -> response to user + prompt to try again
    Options:
        Logout
        Train password
    """
    return ""


def print_help():
    pass


def service_account_add() -> Optional[passager.data_formats.ServiceAccount]:
    pass


def service_account_change_password():
    # These can be put into own function in order to be used in main as well

    # TODO: Ask for password again to validate user
    # TODO: Ask for new password
    # TODO: Check password strength
    pass


def service_account_remove():
    pass


def train_login():
    """Menu in which the user chooses the service for which they wish to train
    logging in and possible parameters for the training.
    """
    pass


def train_login_for(account: passager.data_formats.ServiceAccount):
    # Actual implementation for the login
    pass
