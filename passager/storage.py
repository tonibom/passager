#!/bin/python3
"""
Storage module is responsible for handling the data storage. Salting and hashing
is applied to the main account's information in order to ensure password
security. However, as this is a password manager, the service account passwords
need to be retrievable so hashing won't do. Encryption using the main account's
password as a base for the key is therefore used instead.
"""
import os
import logging

from typing import Optional, Sequence, Tuple

import passager.data_formats as data_formats

from passager.data_formats import MainAccount, ServiceAccount

import hashlib

from Crypto.Cipher import AES


ENCRYPT_MODE = AES.MODE_CBC
# TODO: Platform independency
_FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + "/accounts/"
# TODO: Adjust
_ITERATIONS = 150000
_MAIN_FILE_EXT = ".account"
_MAIN_HASH_NAME = "sha256"
_PADDING = " "
_SERVICE_FILE_EXT = ".service"
# The split character for separating metadata from service data on disk
_SPLIT = ";;"
_SRV_IDENTIFIER = "SERVICE"

_logger = logging.getLogger(__name__)


def _compare_hash(first_hash: bytes, second_hash: bytes) -> bool:
    # TODO: Remove loggers from here
    differences = 0
    if len(first_hash) != len(second_hash):
        _logger.debug("Length mismatch: %s =/= %s", len(first_hash), len(second_hash))
        differences += 1
    for i in range(len(first_hash)):
        try:
            if first_hash[i] != second_hash[i]:
                _logger.debug("Hash char mismatch: %s =/= %s", first_hash[i], second_hash[i])
                differences += 1
        except IndexError:
            # The hashes weren't equally long
            differences += 1
            pass
    # TODO: remove
    _logger.debug("Differences %s", differences)
    return differences == 0


def _decrypt_contents(encrypted_contents: bytes,
                      key: bytes,
                      init_vector: bytes) -> Optional[Tuple[str, str]]:

    decryptor = AES.new(key, ENCRYPT_MODE, IV=init_vector)
    contents_bytes = decryptor.decrypt(encrypted_contents)

    contents = data_formats.decode_load(contents_bytes)

    split_contents = contents.split(_SPLIT)
    if len(split_contents) < 3:
        # The contents are not in correct format, either...
        #     wrong decrypting key / IV,
        #     data was tampered with,
        #     data was corrupted or
        #     there's a backwards compability problem in the software
        _logger.warning("There was a problem decrypting service account's credentials!")
        return None
    username_length = int(split_contents[0])
    password_length = int(split_contents[1])

    # Pack up the credentials (if there are places in there with _SPLIT) and
    # get rid of the padding.
    credentials = _right_unpad("".join(split_contents[2:]))
    _logger.debug(credentials)
    _logger.debug("%s == %s",
                  len(credentials),
                  username_length + password_length)

    if len(credentials) != username_length + password_length:
        _logger.warning("Service account's decrypted credentials were of unexpected size!")

    username = credentials[:username_length]
    password = credentials[username_length:]
    return username, password


def _decrypt_filename(encrypted_service_name: bytes,
                      key: bytes,
                      init_vector: bytes) -> str:
    decryptor = AES.new(key, ENCRYPT_MODE, IV=init_vector)
    service_name = decryptor.decrypt(encrypted_service_name)
    return data_formats.decode_load(service_name)


def delete_main_account(main_account: MainAccount):
    # TODO: Derive decryption key from username
    username_file = main_account.account_name + _MAIN_FILE_EXT
    file_path = _FILE_DIR + username_file

    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        _logger.warning("ERROR: Couldn't remove main account file as it doesn't exist!")


def delete_service_account(main_pass: str,
                           service_name: str):
    # TODO: Derive encryption key from main password

    # TODO: Encrypt service name using the key
    filename = service_name

    file_path = _FILE_DIR + filename + _SERVICE_FILE_EXT

    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        _logger.warning("ERROR: Couldn't remove service account file as it doesn't exist!")


def _derive_encryption_key(main_pass: str, main_accountname: str) -> bytes:
    # Use both the accountname and the main password for creating the key
    #   - main accountname is unique for every main account but known to all
    #   - main password may not be unique but is unknown to other users
    password = data_formats.encode_general(main_accountname + main_pass)
    return hashlib.sha3_256(password).digest()


def _encrypt_contents(username: str,
                      password: str,
                      key: bytes,
                      init_vector: bytes) -> bytes:
    # The lengths of username and password are stored so that the values can
    # be read from the file content string on load.
    username_length = str(len(username)) + _SPLIT
    password_length = str(len(password)) + _SPLIT
    length_data = username_length + password_length

    plain_text = length_data + username + password

    if len(plain_text) % 16 != 0:
        plain_text = _right_pad(plain_text)

    encryptor = AES.new(key, ENCRYPT_MODE, IV=init_vector)
    encrypted_contents = encryptor.encrypt(plain_text)
    return encrypted_contents


def _encrypt_filename(service_name_in: str, key: bytes, init_vector: bytes) -> str:

    encryptor = AES.new(key, ENCRYPT_MODE, IV=init_vector)
    service_name = _SRV_IDENTIFIER + _SPLIT + service_name_in
    if len(service_name) % 16 != 0:
        service_name = _right_pad(service_name)
    _logger.debug("STORE - Padded filename (%s): %s",
                  str(len(service_name)),
                  service_name)
    encrypted_filename = encryptor.encrypt(service_name)
    _logger.debug("STORE - Encrypted filename RAW: %s", encrypted_filename)
    _logger.debug("STORE - Encrypted filename: %s", data_formats.decode_store(encrypted_filename))
    _logger.debug("LOAD - INIT VECTOR RAW: %s", data_formats.decode_store(init_vector))
    _logger.debug("STORE - INIT VECTOR: %s", init_vector)
    return data_formats.decode_store(init_vector) + data_formats.decode_store(encrypted_filename)


def _generate_init_vector() -> bytes:
    return os.urandom(data_formats.IV_LENGTH)


def _generate_salt() -> bytes:
    return os.urandom(data_formats.SALT_LENGTH)


def get_usernames() -> Optional[Sequence[str]]:
    filenames = _read_filenames(_MAIN_FILE_EXT)
    # Cut the file extensions out
    filenames = [filename.split(".")[0] for filename in filenames]
    return filenames


def _load_service_account(filename: str, key: bytes) -> Optional[ServiceAccount]:
    encrypted_service_name = filename.split(".")[0]

    _logger.debug("LOAD - 'Final' filename: %s", filename)

    # Get the initialization vector
    # 2x to accommodate for bytes in hex
    init_vector = data_formats.encode_general(encrypted_service_name[:data_formats.IV_LENGTH * 2])
    _logger.debug("LOAD - INIT VECTOR RAW: %s", init_vector)
    init_vector = data_formats.encode_load(init_vector.decode("utf-8"))
    _logger.debug("LOAD - INIT VECTOR: %s", init_vector)

    # Cut out the initialization vector
    # 2x to accommodate for bytes in hex
    encrypted_service_name = encrypted_service_name[data_formats.IV_LENGTH * 2:]
    _logger.debug("LOAD - Encrypted filename: %s", encrypted_service_name)

    encrypted_service_name = data_formats.encode_load(encrypted_service_name)
    _logger.debug("STORE - Encrypted filename RAW: %s", encrypted_service_name)

    service_name = _decrypt_filename(encrypted_service_name, key, init_vector)

    _logger.debug("LOAD - Padded filename: %s", service_name)
    service_name = _right_unpad(service_name)
    _logger.debug("LOAD - Actual filename: %s", service_name)

    if not service_name.startswith(_SRV_IDENTIFIER + _SPLIT):
        # This file didn't contain a service account for this main account
        _logger.info("%s wasn't a service account for this main account.",
                     service_name)
        return None

    # Cut the service header from the name
    service_name = "".join(service_name.split(_SPLIT)[1:])
    # Decrypted successfully -> it's a correct service

    encrypted_contents = _read_file(filename)
    username, password = _decrypt_contents(encrypted_contents,
                                           key,
                                           init_vector)
    service = ServiceAccount(service_name,
                             username,
                             password)
    _logger.info("Loaded service account for %s.", service_name)
    return service


def load_service_accounts(main_account: MainAccount):
    filenames = _read_filenames(_SERVICE_FILE_EXT)
    decryption_key = _derive_encryption_key(main_account.main_pass,
                                            main_account.account_name)

    for filename in filenames:
        # Cut the file extension out
        try:
            service = _load_service_account(filename, decryption_key)
        except Exception as e:
            # Very likely that the service account was for another main account
            # but it could be that there's a bug in the system.
            _logger.warning("Service account couldn't be loaded: %s", e)
            service = None

        if service is not None:
            main_account.service_accounts.append(service)


def _read_file(filename: str) -> bytes:
    # TODO: Platform indepedency
    file_path = _FILE_DIR + filename
    with open(file_path, "rb") as source:
        contents = source.read()
    return contents


def _read_filenames(extension: str = None) -> Sequence[str]:

    files_list = [f for f in os.listdir(_FILE_DIR) if os.path.isfile(os.path.join(_FILE_DIR, f))]
    if extension is not None:
        # If file extension is specified, only return filenames with said extension
        files_list = [f for f in files_list if f.endswith(extension)]
    _logger.debug("Retrieved files list: %s", files_list)
    return files_list


def _right_pad(payload: str, chunk_size: int = 16):
    pad_length = chunk_size - (len(payload) % chunk_size)
    return payload + _PADDING * pad_length


def _right_unpad(string: str) -> str:
    return string.rstrip(_PADDING)


def salt_and_hash(password_in: str, salt: bytes) -> bytes:
    # Encode into bytes
    password = data_formats.encode_general(password_in)
    # Salt & hash
    hashed_pass = hashlib.pbkdf2_hmac(_MAIN_HASH_NAME,
                                      password,
                                      salt,
                                      _ITERATIONS,
                                      dklen=data_formats.KEY_LENGTH)
    return salt + hashed_pass


def store_main_account(main_account: MainAccount):

    if main_account.salt is None:
        main_account.salt = _generate_salt()
    filename = main_account.account_name
    salted_hash = salt_and_hash(main_account.main_pass, main_account.salt)

    filename += _MAIN_FILE_EXT
    _write_file(filename, salted_hash)


def store_service_account(main_pass: str,
                          main_accountname: str,
                          service_account: ServiceAccount):
    # TODO: Derive encryption key from main password

    encryption_key = _derive_encryption_key(main_pass, main_accountname)
    initiation_vector = _generate_init_vector()

    # Encrypt service name to be used as filename
    # The filename includes the init vector at the beginning.
    filename = _encrypt_filename(service_account.service_name,
                                 encryption_key,
                                 initiation_vector)

    # Encrypt the accountname and the password
    contents = _encrypt_contents(service_account.account_name,
                                 service_account.service_password,
                                 encryption_key,
                                 initiation_vector)

    # filename = data_formats.decode_to_string(filename)
    _logger.debug("STORE - Final filename: %s", filename)
    filename += _SERVICE_FILE_EXT
    _write_file(filename, contents)


def validate_main_login(username: str, password_in: str) -> Optional[MainAccount]:
    main_account = None

    # TODO: Derive decryption key from username
    username_file = username + _MAIN_FILE_EXT
    filenames = _read_filenames(_MAIN_FILE_EXT)
    # TODO: Derive decryption key from password
    # TODO: Decrypt filenames with decryption key

    # TODO: Consider timing attacks
    if username_file in filenames:
        # Account exists
        contents = _read_file(username_file)

        # TODO: Separate from service accounts
        # Still leaving this previous implementation here as a reminder
        # if len(contents) != 1:
        #     return None

        # Includes the salt
        actual_password = contents
        actual_salt = contents[:data_formats.SALT_LENGTH]

        hashed_password_in = salt_and_hash(password_in, actual_salt)

        if _compare_hash(hashed_password_in, actual_password):
            # Login successful
            main_account = MainAccount(username, password_in, actual_salt)

    return main_account


def _write_file(filename: str, contents: bytes):
    """Writes the account credentials into a file
    For main accounts
        filename: the account's name as plain text
        contents: the salted password hash
    For service accounts
        filename: the service's name as encrypted
        contents: the service account's username & password as encrypted
    """

    file_path = _FILE_DIR + filename

    with open(file_path, "wb") as source:
        source.write(contents)
        _logger.info("Saved account in file %s", filename)
