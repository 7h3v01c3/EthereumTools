import requests
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv("venv/.env")
api_key = os.getenv("API_Key")
# Note you mudy obtain an API key on Etherscan by creating an account
# and setting the API key in the environment variables
# More information can be found at: https://etherscan.io/apis


def is_valid_ethereum_address(address):
    """
    Check if an entry is valid.

    :param address: Ethereum account or address to validate.
    :return: True if valid, False otherwise.
    """
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))


def is_smart_contract(address):
    """
    Determine if an Ethereum address represents a smart contract.

    :param address: Ethereum address to check.
    :return: A tuple containing a boolean result and the response.
    """
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={address}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'result' in data:
        code = data['result']
        return code != '0x', response  # Return both the boolean result and the response
    else:
        return False, response


def main():
    """
    Main program execution.
    """
    # Input prompt for the Ethereum address
    contract_address = input("Enter an Ethereum address: ")

    if not is_valid_ethereum_address(contract_address):
        print("Not a valid account or contract")
        quit()

    # Check if the address is a smart contract
    is_contract, response = is_smart_contract(contract_address)
    print(f"Is this a smart contract? {is_contract}")


if __name__ == "__main__":
    main()
