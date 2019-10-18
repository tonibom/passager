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

from passager.data_formats import MainAccount, MenuOptions, ServiceAccount

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

    "MAIN-ACCOUNT-REMOVE": MenuOptions.MAIN_ACCOUNT_REMOVE,
    "MAIN-RM": MenuOptions.MAIN_ACCOUNT_REMOVE,

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
    MenuOptions.TRAINING: {
        "name": ("TRAINING", "aliases: TRAIN, T"),
        "description": "train logging in to a service with your account credentials",
        "usage": "training <SERVICE NAME>",
        "example": "training Google",
        "parameter-count": (1, ),
    },
    MenuOptions.SERVICE_ACCOUNT_ADD: {
        "name": ("SRV-ADD",  "aliases: SERVICE_ACCOUNT_ADD"),
        "description": "add a service account for which you wish to save a password and train login",
        "usage": "srv-add <SERVICE NAME> <ACCOUNT NAME> <PASSWORD>",
        "example": "srv-add Google example@gmail.com h0rr1bl3p455w0rd",
        "parameter-count": (3, ),
    },
    MenuOptions.SERVICE_ACCOUNT_CHANGE_PASSWORD: {
        "name": ("SRV-CHANGE-PW", "aliases: SERVICE_ACCOUNT_CHANGE_PASSWORD"),
        "description": "change a service account's password",
        "usage": "srv-change-pw <SERVICE NAME>",
        "example": "srv-change-pw Google",
        "parameter-count": (1, ),
    },
    MenuOptions.SERVICE_ACCOUNT_REMOVE: {
        "name": ("SRV-RM", "aliases: SERVICE_ACCOUNT_REMOVE"),
        "description": "remove the specified service account",
        "usage": "srv-rm <SERVICE NAME>",
        "example": "srv-rm Google",
        "parameter-count": (1, ),
    },
    MenuOptions.SERVICE_ACCOUNTS: {
        "name": ("ACCOUNTS",  "aliases: SRV-ACC, SERVICE_ACCOUNTS"),
        "description": "display all service accounts created for this main account",
        "usage": "accounts",
        "example": "accounts",
        "parameter-count": (0, ),
    },
    MenuOptions.MAIN_ACCOUNT_CHANGE_PASSWORD: 5,
    MenuOptions.MAIN_ACCOUNT_REMOVE: {
        "name": ("MAIN-RM", "aliases: MAIN_ACCOUNT_REMOVE"),
        "description": "remove the main account along with all of the service accounts associated with it",
        "usage": "main-rm",
        "example": "main-rm",
        "parameter-count": (0, ),
    },
    MenuOptions.LOGOUT: 7,
}
_PADDING = 32
_PW_RANK = {
    0: "poor",
    1: "weak",
    2: "adequate",
    3: "mediocre",
    4: "strong",
    5: "very strong",
}

_logger = logging.getLogger(__name__)


def accept_new_password(account_name: str, password: str, strength: int) -> bool:
    # account_name can be either service name or main account name
    print("You've entered password '{}' for account {}.".format(password,
                                                                account_name))
    print("This password is considered {}.\n".format(_PW_RANK[strength]))
    while True:
        answer = input("Do you wish to make the password change (yes/no)? >")
        if answer.upper() in ("Y", "YES"):
            print("Password was changed successfully.")
            return True
        elif answer.upper() in ("N", "NO"):
            print("Password wasn't changed.")
            return False
        print("Invalid input.")


def authentication_login(main_username: str) -> Tuple[str, str]:
    print("You need to authenticate yourself to use this command.")
    print("Log in using your main account credentials\n")
    username, password = _login_input(main_username)
    return username, password


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


def invalid_password_length(password_length: int,
                            recommended_min: int,
                            recommended_max: int):
    if password_length > recommended_max:
        print("The password length exceeds the max limit of {}.".format(recommended_max))
        print("There's no need to have a password this long.\n")
    elif password_length < recommended_min:
        print("The length of a password should be at least {} characters.\n".format(recommended_min))


def invalid_service_account(service_name: str):
    print("You do not have an account set for service '{}'".format(service_name))
    print("Use command 'ACCOUNTS' to view your service accounts.")


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


def main_account_add() -> Optional[MainAccount]:
    # Optional because might fail
    # Account registration
    pass


def main_account_change_password():
    # TODO: Ask for password again to validate user

    # These can be put into own function in order to be used in service as well
    # TODO: Ask for new password
    # TODO: Check password strength

    pass


def main_account_deletion_confirmation(main_account: MainAccount) -> bool:
    account_count = len(main_account.service_accounts)
    print("You are trying to delete main account '{}'.\n".format(main_account.account_name))
    print("You won't be able to log in to this account after this.")
    print("All of your {} service accounts' login credentials will be deleted.\n".format(account_count))
    while True:
        answer = input("Are you sure you want to delete this account (yes/no)? >")
        if answer.upper() in ["Y", "N"]:
            print("Please, enter the entire word for confirmation.")
        elif answer.upper() == "NO":
            return False
        elif answer.upper() == "YES":
            return True


def main_account_removed(main_account: MainAccount):
    name = main_account.account_name
    service_account_count = len(main_account.service_accounts)
    print("{} service accounts have been removed successfully!".format(service_account_count))
    print("\nMain account {} has been removed successfully!".format(name))
    print("You will now be logged out and the program will shut down.\n")
    input("{} PRESS ENTER TO CONTINUE {}".format(_PADDING * "=", _PADDING * "="))


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


def new_password(account_name: str) -> str:
    # account_name can be either service name or main account name
    print("Changing password for {}.".format(account_name))
    print("If you do not want to change the password, just press enter without entering any characters.")
    password = input("Enter new password: ")
    return password


def password_change_canceled():
    print("Password change was canceled.")


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


def _print_service_account(service_account: ServiceAccount):
    print("SERVICE: {}".format(service_account.service_name))
    print("USERNAME: {}".format(service_account.account_name))
    print("PASSWORD: {}".format(service_account.service_password))


def service_account_added(service_account: ServiceAccount):
    print("Successfully added the following account: ")
    _print_service_account(service_account)
    print("")


def service_account_change_password():
    # These can be put into own function in order to be used in main as well

    # TODO: Ask for password again to validate user
    # TODO: Ask for new password
    # TODO: Check password strength
    pass


def service_account_removed(service_name: str):
    print("Service account for '{}' was removed successfully!".format(service_name))


def service_accounts(main_account: MainAccount):
    print("{} SERVICE ACCOUNTS {}".format(_PADDING * "-", _PADDING * "-"))
    for account in main_account.service_accounts:
        _print_service_account(account)
        print("")


def service_already_exists(service_name: str):
    print("Service cannot be added: You already have a service account for {}".format(
          service_name))


def train_login_for(account: ServiceAccount):
    # Actual implementation for the login
    success_counter = 1
    print("---------- Login Screen ----------")
    print("Enter empty field to either to the username or")
    print("password to return back to the main menu.\n")
    while True:
        username, password = _login_input()
        if username == "" or password == "":
            return
        if (username == account.account_name and
                password == account.service_password):
            print("Login successful x{}\n".format(success_counter))
            success_counter += 1
        else:
            print("Login failed. To return to main menu, enter empty fields.\n")
