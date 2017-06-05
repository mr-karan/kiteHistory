#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
from os import getenv

import pandas as pd
import requests
from kiteconnect import KiteConnect

from config import KITE_API_KEY, KITE_REQUEST_TOKEN, KITE_SECRET
from scaffold import *

KITE_API_KEY = getenv('KITE_API_KEY')
KITE_REQUEST_TOKEN = getenv('KITE_REQUEST_TOKEN')
KITE_SECRET = getenv('KITE_SECRET')
CSV_URL = "https://api.kite.trade/instruments?api_key='{}'".format(
    KITE_API_KEY)

kite = KiteConnect(api_key=KITE_API_KEY)

try:
    with open('token.ini', 'r') as the_file:
        access_token = the_file.readline()
        try:
            kite.set_access_token(access_token)

        except Exception as e:
            print("Authentication failed", str(e))
            raise

except FileNotFoundError:
    user = kite.request_access_token(
        request_token=KITE_REQUEST_TOKEN, secret=KITE_SECRET)

    with open('token.ini', 'w') as the_file:
        the_file.write(user['access_token'])

    try:
        kite.set_access_token(user["access_token"])

    except Exception as e:
        print("Authentication failed", str(e))
        raise


def get_history(symbol, from_date, to_date, interval, exchange='NSE'):
    """
    can be used this w/o cli
    :param symbol:
    :return:
    """
    # if csv not found
    try:
        df = pd.read_csv('temp.csv')

    except FileNotFoundError:
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
        with open('temp.csv', "w") as the_file:
            writer = csv.writer(the_file, delimiter=',')
            for line in my_list:
                writer.writerow(line)
        df = pd.read_csv('temp.csv')

    result = df.query(
        "tradingsymbol=='{0}' and exchange=='{1}'".format(symbol, exchange))
    # filter exchange in query too
    token = result.iloc[0][0]
    # use token with kite api
    d = kite.historical(token, from_date, to_date, interval)
    return d


def main():
    print(get_history('INFY', '2017-05-18', '2017-05-19', 'minute', 'NSE'))


if __name__ == '__main__':
    log.info('Initiating Kite History...')
    log.debug('Initiating Kite History with DEBUG mode')
    if not check_for_tokens():
        exit()
    exit(main())
