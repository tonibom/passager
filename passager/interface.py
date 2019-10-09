#!/bin/python3
"""
Interface module is responsible for displaying the user interface to the user
and receiving the required input from the user. The user input is validated
here and returned back to the caller.
Currently the only implementation is going to be CLI, but GUI might be implemented
later on.
"""
import getpass

from typing import Optional, Sequence, Tuple

import passager.data_formats

from passager.data_formats import MenuOptions

_MENU_COMMANDS = {
    "HELP": MenuOptions.HELP,
    "H": MenuOptions.HELP,
    "?": MenuOptions.HELP,

    "TRAINING": MenuOptions.TRAINING,
    "TRAIN": MenuOptions.TRAINING,
    "T": MenuOptions.TRAINING,

    "SERVICE_ACCOUNT_ADD": MenuOptions.SERVICE_ACCOUNT_ADD,
    "SRV-ADD": MenuOptions.SERVICE_ACCOUNT_ADD,

    "SERVICE_ACCOUNT_CHANGE_PASSWORD": MenuOptions.SERVICE_ACCOUNT_CHANGE_PASSWORD,
    "SRV-CHANGE-PW": MenuOptions.SERVICE_ACCOUNT_CHANGE_PASSWORD,

    "SERVICE_ACCOUNT_REMOVE": MenuOptions.SERVICE_ACCOUNT_REMOVE,
    "SRV-RM": MenuOptions.SERVICE_ACCOUNT_REMOVE,

    "MAIN_ACCOUNT_CHANGE_PASSWORD": MenuOptions.MAIN_ACCOUNT_CHANGE_PASSWORD,
    "MAIN-CHANGE-PW": MenuOptions.MAIN_ACCOUNT_CHANGE_PASSWORD,

    "LOGOUT": MenuOptions.LOGOUT,
    "EXIT": MenuOptions.LOGOUT,
    "QUIT": MenuOptions.LOGOUT,
    "Q": MenuOptions.LOGOUT,
    "SHUTDOWN": MenuOptions.LOGOUT,
    "CLOSE": MenuOptions.LOGOUT,
}
_MENU_COMMAND_INFO = {
    MenuOptions.HELP: 0,
    MenuOptions.TRAINING: 1,
    MenuOptions.SERVICE_ACCOUNT_ADD: {
        "description": "add a service account for which you wish to save a password and train login",
        "usage": "srv-add <SERVICE NAME> <ACCOUNT NAME> <PASSWORD>",
        "example": "srv-add Google example@gmail.com h0rr1bl3p455w0rd",
    },
    MenuOptions.SERVICE_ACCOUNT_CHANGE_PASSWORD: 3,
    MenuOptions.SERVICE_ACCOUNT_REMOVE: 4,
    MenuOptions.MAIN_ACCOUNT_CHANGE_PASSWORD: 5,
    MenuOptions.MAIN_ACCOUNT_REMOVE: 6,
    MenuOptions.LOGOUT: 7,
}
_PADDING = 32


def invalid_login():
    print("\nInvalid login username or password")


def login() -> Tuple[str, str]:
    print("\nWelcome to Passager!")
    print("Please enter your Main Account credentials to log in\n")
    username, password = _login_input()
    return username, password


def _login_input(known_username: str = None) -> Tuple[str, str]:
    if known_username is not None:
        print("Username: {}".format(known_username))
        username = known_username
    else:
        username = input("Username: ")
    password = getpass.getpass("Password: ")
    return username, password


def login_successful(username: str):
    print("Logged in successfully as {}!\n".format(username))


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


def main_menu() -> Optional[Tuple[MenuOptions, Sequence[str]]]:
    """User interface for the main menu structure. Provides the user the options
    to choose from and asks what the user wants to do. User inputs their choice,
    this selection is validated and responded to.
        Valid -> response to user + return appropriate command to be handled in core
        Invalid -> response to user + prompt to try again
    Options:
        Logout
        Train password
    """

    print("\n{} MAIN MENU {}\n".format(_PADDING * "=", _PADDING * "="))

    while True:
        user_input = input("Enter command >").split(" ")
        input_command = user_input[0]
        input_parameters = user_input[1:]
        print("")
        if input_command.upper() in _MENU_COMMANDS.keys():
            return _MENU_COMMANDS[input_command.upper()], input_parameters
        else:
            print("Invalid command")


def print_help():
    pass


def print_command_usage(command: MenuOptions):
    print("Usage: " + _MENU_COMMAND_INFO[command]["usage"])
    print("For help, use HELP command")


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
