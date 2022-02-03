import os


class Config(object):
    # Your Blockstream AMP Account Details
    #######################################
    API_USERNAME = 'your_amp_account_username'
    API_PASSWORD = 'your_amp_account_password'

    # Blockstream AMP API URL
    #########################
    # The URL you use will be linked to the account above.
    # For example; an account created on test will only work with the amp-test URL.

    # For the Test AMP instance use:
    API_URL = os.environ.get('API_URL') or 'https://amp-test.blockstream.com/api'

    # For the Production AMP instance use:
    #API_URL = os.environ.get('API_URL') or 'https://amp.blockstream.com/api'

    # Beta (Blockstream Dev use only):
    #API_URL = os.environ.get('API_URL') or 'https://amp-beta.blockstream.com/api'

    # You should change this to any random alphanumeric:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ncal47ytvny4vCYT9X8YLM498YNVC'
