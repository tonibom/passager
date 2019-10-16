#!/bin/python3
"""
Core module is responsible for handling the software's execution flow after the
user has logged in successfully.
"""
import logging

import passager.data_formats
import passager.interface
import passager.storage

from passager.data_formats import MenuOptions

_logger = logging.getLogger(__name__)


def _authenticate_main(main_account: passager.data_formats.MainAccount) -> bool:
    username, password = passager.interface.authentication_login(main_account.account_name)
    if username is None or password is None:
        passager.interface.invalid_login()
        return False

    logged_account = passager.storage.validate_main_login(username, password)
    if logged_account is None:
        # Login failed
        passager.interface.invalid_login()
        return False
    return True


def run(main_account: passager.data_formats.MainAccount):
    """Try for modular structure:
        Open interface's main menu
        Use the result to logout / open up the selected menu
            Add service
            Remove service
            Change password for service
            Change main password
            Remove main
            Display services
            Print help
            Training
            Logout
    """
    passager.interface.login_successful(main_account.account_name)
    _logger.info("User %s logged in", main_account.account_name)

    passager.storage.load_service_accounts(main_account)
    command_in = None

    while command_in != MenuOptions.LOGOUT:
        # Take the input from the user
        command_in, parameters_in = passager.interface.main_menu()
        _logger.debug("User %s inputted command %s with parameters %s",
                      main_account.account_name,
                      command_in,
                      parameters_in)
        # TODO: Call the corresponding interface according to the input
        if command_in == MenuOptions.SERVICE_ACCOUNT_ADD:
            _logger.debug("Handling service account add")
            if len(parameters_in) != 3:
                passager.interface.invalid_parameter_count(command_in,
                                                           parameters_in)
                continue
            service_name = parameters_in[0]
            service_username = parameters_in[1]
            service_password = parameters_in[2]

            if service_name in main_account.service_names():
                # The main account already has an account added for this service name
                passager.interface.service_already_exists(service_name)
                continue

            service_account = passager.data_formats.ServiceAccount(service_name,
                                                                   service_username,
                                                                   service_password)
            main_account.service_accounts.append(service_account)
            passager.storage.store_service_account(main_account.main_pass,
                                                   service_account)
            passager.interface.service_account_added(service_account)

        elif command_in == MenuOptions.SERVICE_ACCOUNTS:
            _logger.debug("Handling service accounts print")
            if len(parameters_in) != 0:
                passager.interface.invalid_parameter_count(command_in,
                                                           parameters_in)
            passager.interface.service_accounts(main_account)

        elif command_in == MenuOptions.SERVICE_ACCOUNT_REMOVE:
            _logger.debug("Handling service account removal")
            if len(parameters_in) != 1:
                passager.interface.invalid_parameter_count(command_in,
                                                           parameters_in)
                continue
            account_name = parameters_in[0]
            if account_name not in main_account.service_names():
                # If the user has no service set with the requested service name
                passager.interface.invalid_service_account(parameters_in[0])
                continue

            if not _authenticate_main(main_account):
                # User couldn't authenticate properly
                continue

            # Delete service account from main account runtime list
            main_account.remove_service_account(account_name)
            # Delete service from disk
            passager.storage.delete_service_account(main_account.main_pass,
                                                    account_name)
            # Notify user
            passager.interface.service_account_removed(account_name)

        elif command_in == MenuOptions.HELP:
            _logger.debug("Handling help")
            command_help = None
            if len(parameters_in) not in [0, 1]:
                passager.interface.invalid_parameter_count(command_in,
                                                           parameters_in)
                continue
            if len(parameters_in) == 1:
                try:
                    command_help = passager.interface.MENU_COMMANDS[parameters_in[0].upper()]
                except KeyError:
                    passager.interface.invalid_command_for_help(parameters_in[0])
                    continue
            passager.interface.print_help(command_help)
