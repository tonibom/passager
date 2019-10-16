#!/bin/python3
"""
Core module is responsible for handling the software's execution flow after the
user has logged in successfully.
"""
import logging

from typing import Sequence

import passager.interface as interface
import passager.storage as storage

from passager.data_formats import MainAccount, MenuOptions, ServiceAccount

_logger = logging.getLogger(__name__)


def _help(command_in: MenuOptions, parameters_in: Sequence[str]):
    _logger.debug("Handling help")
    command_help = None
    if len(parameters_in) not in [0, 1]:
        interface.invalid_parameter_count(command_in,
                                          parameters_in)
        return
    if len(parameters_in) == 1:
        try:
            command_help = interface.MENU_COMMANDS[parameters_in[0].upper()]
        except KeyError:
            interface.invalid_command_for_help(parameters_in[0])
            return
    interface.print_help(command_help)


def _authenticate_main(main_account: MainAccount) -> bool:
    username, password = interface.authentication_login(main_account.account_name)
    if username is None or password is None:
        interface.invalid_login()
        return False

    logged_account = storage.validate_main_login(username, password)
    if logged_account is None:
        # Login failed
        interface.invalid_login()
        return False
    return True


def run(main_account: MainAccount):
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
    interface.login_successful(main_account.account_name)
    _logger.info("User %s logged in", main_account.account_name)

    storage.load_service_accounts(main_account)
    command_in = None

    while command_in != MenuOptions.LOGOUT:
        # Take the input from the user
        command_in, parameters_in = interface.main_menu()
        _logger.debug("User %s inputted command %s with parameters %s",
                      main_account.account_name,
                      command_in,
                      parameters_in)
        # TODO: Call the corresponding interface according to the input
        if command_in == MenuOptions.SERVICE_ACCOUNT_ADD:
            _service_add(main_account, command_in, parameters_in)

        elif command_in == MenuOptions.SERVICE_ACCOUNTS:
            _service_display(main_account, command_in, parameters_in)

        elif command_in == MenuOptions.SERVICE_ACCOUNT_REMOVE:
            _service_remove(main_account, command_in, parameters_in)

        elif command_in == MenuOptions.HELP:
            _help(command_in, parameters_in)


def _service_add(main_account: MainAccount,
                 command_in: MenuOptions,
                 parameters_in: Sequence[str]):
    _logger.debug("Handling service account add")
    if len(parameters_in) != 3:
        interface.invalid_parameter_count(command_in,
                                          parameters_in)
        return
    service_name = parameters_in[0]
    service_username = parameters_in[1]
    service_password = parameters_in[2]

    if service_name in main_account.service_names():
        # The main account already has an account added for this service name
        interface.service_already_exists(service_name)
        return

    service_account = ServiceAccount(service_name,
                                     service_username,
                                     service_password)
    main_account.service_accounts.append(service_account)
    storage.store_service_account(main_account.main_pass,
                                  service_account)
    interface.service_account_added(service_account)


def _service_display(main_account: MainAccount,
                     command_in: MenuOptions,
                     parameters_in: Sequence[str]):
    _logger.debug("Handling service accounts print")
    if len(parameters_in) != 0:
        interface.invalid_parameter_count(command_in,
                                          parameters_in)
    interface.service_accounts(main_account)


def _service_remove(main_account: MainAccount,
                    command_in: MenuOptions,
                    parameters_in: Sequence[str]):
    _logger.debug("Handling service account removal")
    if len(parameters_in) != 1:
        interface.invalid_parameter_count(command_in,
                                          parameters_in)
        return
    account_name = parameters_in[0]
    if account_name not in main_account.service_names():
        # If the user has no service set with the requested service name
        interface.invalid_service_account(parameters_in[0])
        return

    if not _authenticate_main(main_account):
        # User couldn't authenticate properly
        return

    # Delete service account from main account runtime list
    main_account.remove_service_account(account_name)
    # Delete service from disk
    storage.delete_service_account(main_account.main_pass,
                                   account_name)
    # Notify user
    interface.service_account_removed(account_name)
