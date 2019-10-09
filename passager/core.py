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
                passager.interface.print_command_usage(MenuOptions.SERVICE_ACCOUNT_ADD)
                continue
            service_name = parameters_in[0]
            service_username = parameters_in[1]
            service_password = parameters_in[2]

            if service_name in main_account.service_accounts:
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
