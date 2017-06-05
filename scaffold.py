import logging
from os import getenv

__all__ = ['log', 'check_for_tokens']

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s -'
                    ' %(funcName)s - %(message)s')

log = logging.getLogger('kiteHistory')


def check_for_tokens():
    '''
    Checks for token present in system environment. To set them, export them
    in your ~/.bashrc or ~/.zshrc
    '''
    log.debug('Checking for tokens')

    kite_api_key = getenv('KITE_API_KEY')
    kite_request_token = getenv('KITE_REQUEST_TOKEN')
    kite_secret = getenv('KITE_SECRET')

    # Get your request token from the first time
    # kite.trade/connect/login?api_key=<>

    log.debug("Tokens fetched: {} {} ".format(kite_api_key,
                                              kite_secret,))

    if kite_api_key is None or kite_secret is None:
        print('''
            You need to add your Kite API token,
            along with Secret Key. \n
            export KITE_API_KEY='your-kite-api-key'
            export KITE_SECRET='your-kite-secret-key'
            \n
            You can fetch it from here : https://developers.kite.trade/apps
        ''')
        return False

    log.debug("Kite Request Token: {}".format(kite_request_token))

    if kite_request_token is None:
        print('''
            Set your request token.
            You can do this by setting environment variables: \n
            export KITE_REQUEST_TOKEN='your-kite-request-token' \n
            Generate request token from 
            https://kite.trade/connect/login?api_key=<>
            ''')
        return False
    return True
