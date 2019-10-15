#!/bin/python3
"""
Interface module is responsible for displaying the user interface to the user
and receiving the required input from the user. The user input is validated
here and returned back to the caller.
Currently the only implementation is going to be CLI, but GUI might be implemented
later on.
"""
import getpass
import logging

from typing import Optional, Sequence, Tuple

import passager.data_formats

from passager.data_formats import MenuOptions

MENU_COMMANDS = {
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

    "SERVICE_ACCOUNTS": MenuOptions.SERVICE_ACCOUNTS,
    "SRV-ACC": MenuOptions.SERVICE_ACCOUNTS,
    "ACCOUNTS": MenuOptions.SERVICE_ACCOUNTS,

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
    MenuOptions.HELP: {
        "name": ("HELP", "aliases: H, ?"),
        "description": "display information about available commands",
        "usage": "help <COMMAND>",
        "example": "help training",
        "parameter-count": (0, 1),
    },
    MenuOptions.TRAINING: 1,
    MenuOptions.SERVICE_ACCOUNT_ADD: {
        "name": ("SRV-ADD",  "aliases: SERVICE_ACCOUNT_ADD"),
        "description": "add a service account for which you wish to save a password and train login",
        "usage": "srv-add <SERVICE NAME> <ACCOUNT NAME> <PASSWORD>",
        "example": "srv-add Google example@gmail.com h0rr1bl3p455w0rd",
        "parameter-count": (3, ),
    },
    MenuOptions.SERVICE_ACCOUNT_CHANGE_PASSWORD: 3,
    MenuOptions.SERVICE_ACCOUNT_REMOVE: 4,
    MenuOptions.SERVICE_ACCOUNTS: {
        "name": ("ACCOUNTS",  "aliases: SRV-ACC, SERVICE_ACCOUNTS"),
        "description": "display all service accounts created for this main account",
        "usage": "accounts",
        "example": "accounts",
        "parameter-count": (0, ),
    },
    MenuOptions.MAIN_ACCOUNT_CHANGE_PASSWORD: 5,
    MenuOptions.MAIN_ACCOUNT_REMOVE: 6,
    MenuOptions.LOGOUT: 7,
}
_PADDING = 32

_logger = logging.getLogger(__name__)


def invalid_command_for_help(command: str):
    print("'{}' is not a valid command. ".format(command), end="")
    print("For full help list, do not enter any parameters.")
    print("\n---------- The help command ----------")
    print_help(MenuOptions.HELP)
    _print_available_commands()


def invalid_login():
    print("\nInvalid login username or password")


def invalid_parameter_count(command: MenuOptions, parameters: Sequence[str]):
    try:
        # TODO: Remove this check when all commands have been implemented
        expected_count = _MENU_COMMAND_INFO[command]["parameter-count"]
    except TypeError:
        _logger.warning("Tried to access unimplemented command's parameter count")
        return
    expected_count = [str(a) for a in expected_count]
    if len(expected_count) != 1:
        # There are multiple valid parameter counts
        expected_count = " or ".join(expected_count)
    else:
        expected_count = expected_count[0]
    print("Invalid number of parameters! ({})".format(len(parameters)))
    print("The command {} takes {} parameters.\n".format(command.name,
                                                         expected_count))
    print_command_usage(command)


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
        if input_command.upper() in MENU_COMMANDS.keys():
            return MENU_COMMANDS[input_command.upper()], input_parameters
        else:
            print("Invalid command")


def _print_available_commands():
    print("\nAvailable commands:")
    for i in _MENU_COMMAND_INFO.values():
        if type(i) is not int:
            # TODO: fix when all commands have been added
            print(i["name"])


def print_command_usage(command: MenuOptions):
    print("Usage: " + _MENU_COMMAND_INFO[command]["usage"])
    print("For help, run 'HELP {}'".format(_MENU_COMMAND_INFO[command]["name"][0]))


def print_help(command_in: MenuOptions = None):

    def print_command_info(cmd: MenuOptions):
        name = _MENU_COMMAND_INFO[cmd]["name"][0] \
               + " | " \
               + _MENU_COMMAND_INFO[cmd]["name"][1]
        print("Name: " + name)
        print("Usage: " + _MENU_COMMAND_INFO[cmd]["usage"])
        print("Example: " + _MENU_COMMAND_INFO[cmd]["example"])

    if command_in is not None:
        # TODO: Change when all commands implemented
        if type(_MENU_COMMAND_INFO[command_in]) == dict:
            print_command_info(command_in)
            return
        else:
            print("{} is a valid command, but not yet implemented".format(command_in))

    print("{} HELP {}\n".format(_PADDING * "=", _PADDING * "="))
    print("The commands are not case sensitive and have multiple aliases.")
    print("Some commands require parameters to be passed as well.")
    print("\n++++++++++ COMMANDS ++++++++++\n")
    for command in _MENU_COMMAND_INFO:
        # TODO: Change when all commands implemented
        if type(_MENU_COMMAND_INFO[command]) == dict:
            print_command_info(command)
        else:
            print("{} is a valid command, but not yet implemented".format(command))
        print("\n")


def _print_service_account(service_account: passager.data_formats.ServiceAccount):
    print("SERVICE: {}".format(service_account.service_name))
    print("USERNAME: {}".format(service_account.account_name))
    print("PASSWORD: {}".format(service_account.service_password))


def service_account_added(service_account: passager.data_formats.ServiceAccount):
    print("Successfully added the following account: ")
    _print_service_account(service_account)
    print("")


def service_account_change_password():
    # These can be put into own function in order to be used in main as well

    # TODO: Ask for password again to validate user
    # TODO: Ask for new password
    # TODO: Check password strength
    pass


def service_account_remove():
    pass


def service_accounts(main_account: passager.data_formats.MainAccount):
    print("{} SERVICE ACCOUNTS {}".format(_PADDING * "-", _PADDING * "-"))
    for account in main_account.service_accounts:
        _print_service_account(account)
        print("")


def service_already_exists(service_name: str):
    print("Service cannot be added: You already have a service account for {}".format(
          service_name))


def train_login():
    """Menu in which the user chooses the service for which they wish to train
    logging in and possible parameters for the training.
    """
    pass


def train_login_for(account: passager.data_formats.ServiceAccount):
    # Actual implementation for the login
    pass
