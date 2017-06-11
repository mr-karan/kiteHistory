#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import csv
from logging import DEBUG
from os import curdir, getenv, path
from sys import exit

import numpy as np
import pandas as pd
import requests
from kiteconnect import KiteConnect

from bokeh.plotting import figure, output_file, show

from .config import KITE_API_KEY, KITE_REQUEST_TOKEN, KITE_SECRET
from .scaffold import *

parser = argparse.ArgumentParser(prog='kiteHistory')
parser.add_argument('-s', '--symbol', action='store', type=str,
                    help='Specify Trading Symbol ', required=True)
parser.add_argument('-i', '--interval', action='store', type=str,
                    help='''Specify interval. Possible values are · day · 3minute
					· 5minute · 10minute · 15minute · 30minute · 60minute''', required=True)
parser.add_argument('-f', '--from_date', action='store', type=str,
                    help='Specify yyyy-mm-dd formatted date indicating the start date of records.', required=True)
parser.add_argument('-t', '--to_date', action='store', type=str,
                    help='Specify yyyy-mm-dd formatted date indicating the end date of records.', required=True)
parser.add_argument('-e', '--exchange', action='store', type=str,
                    help='''Specify exchange name.
                    ·BSE, ·NFO, ·CDS, ·MCX, ·MCXSX, ·BFO ''', required=True)
parser.add_argument('-p', '--path', action='store', default=curdir,
                    help='Set the path to store token keys and data dumps. Defaults to current directory')
parser.add_argument('-V', '--verbose', action='store_true',
                    help='Show more information on what''s happening.')
parser.add_argument('-o', '--output', action='store_true',
                    help='Set flag to store data in csv file', required=False)
parser.add_argument('--plot', action='store_true',
                    help='Set flag to plot data in html file', required=False)

args = parser.parse_args()

if args.verbose:
    log.setLevel(DEBUG)

CSV_URL = "https://api.kite.trade/instruments?api_key='{}'".format(
    KITE_API_KEY)


def datetime(x):
    """
    Helper function to convert list of string objects to np.datetime64 objects.
    """
    return np.array(x, dtype=np.datetime64)


def initialize_kite():
    """
    Helper function to initialize Kite.
    """
    kite = KiteConnect(api_key=KITE_API_KEY)

    try:
        with open(path.join(args.path, 'token.ini'), 'r') as the_file:
            access_token = the_file.readline()
            try:
                kite.set_access_token(access_token)

            except Exception as e:
                log.error("Authentication failed {}".format(str(e)))
                raise

    except FileNotFoundError:
        try:
            user = kite.request_access_token(
                request_token=KITE_REQUEST_TOKEN, secret=KITE_SECRET)
        except Exception as e:
            log.error("{}".format(str(e)))
            exit()

        with open(path.join(args.path, 'token.ini'), 'w') as the_file:
            the_file.write(user['access_token'])

        try:
            kite.set_access_token(user["access_token"])

        except Exception as e:
            log.error("Authentication failed {}".format(str(e)))
            raise

    return kite


def get_history(kite_instance, symbol, from_date, to_date, interval, exchange):
    """
    params
        - kite_instance: <kiteconnect.KiteConnect object>
        - symbol(str): Stock's Trading Symbol
        - from_date(str): YYYY-MM-DD formatted date indicating the start date of records
        - to_date(str): YYYY-MM-DD formatted date indicating the end date of records
        - interval(str): Specify interval between tick data.
        - exchange(str): Specify exchange name.

    return
        -result_data(List): object with filtered data.
    """
    # if csv not found
    try:
        df = pd.read_csv('INSTRUMENTS_MASTER.csv')

    except FileNotFoundError:
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

        with open(path.join(args.path, 'INSTRUMENTS_MASTER.csv'), 'w') as the_file:
            writer = csv.writer(the_file, delimiter=',')
            for line in my_list:
                writer.writerow(line)

        df = pd.read_csv('INSTRUMENTS_MASTER.csv')

    try:
        result = df.query(
            "tradingsymbol=='{0}' and exchange=='{1}'".format(symbol, exchange))
        token = result.iloc[0][0]
        result_data = kite_instance.historical(
            token, from_date, to_date, interval)
        return result_data

    except IndexError as e:
        log.error("Cannot find any data.")
        log.debug(str(e))
        exit()


def write_to_csv(stock_data, name):
    """
    params:
        - stock_data(list) : list of dict objects containing stock data
        - name(str) : output file name specified by `-output` param.
    """
    with open(path.join(args.path, name + '.csv'), 'w') as the_file:
        fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume']
        writer = csv.DictWriter(the_file, fieldnames=fieldnames)
        writer.writeheader()
        for line in stock_data:
            writer.writerow(line)


def plot_csv(stock_data, symbol):
    """
    params:
        - stock_data(list) : list of dict objects containing stock data
        - name(str) : output file name specified by `-output` param.
    """

    try:
        df = pd.read_csv('{}.csv'.format(symbol))

    except:
        write_to_csv(stock_data, symbol)
        df = pd.read_csv('{}.csv'.format(symbol))

    p1 = figure(x_axis_type="datetime", title="Stock Closing Price")
    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(datetime(list(df['date'])), list(df['close']),
            color='#A6CEE3', legend=symbol)
    output_file("{}.html".format(symbol), title="Stock Closing Prices")

    show(p1)  # open a browser


def main():
    kite_instance = initialize_kite()
    result = get_history(kite_instance, args.symbol, args.from_date,
                         args.to_date, args.interval, args.exchange)

    if args.plot:
        plot_csv(result, args.symbol)

    if args.output:
        write_to_csv(result, args.symbol)


if __name__ == '__main__':
    log.info('Initiating Kite History...')
    log.debug('Initiating Kite History with DEBUG mode')
    if not check_for_tokens():
        exit()
    exit(main())
