########################################################################################################
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from robinhood_mypuppet.pyrh.robinhood import Robinhood
from pprint import pprint
from robinhood_mypuppet.pyrh.trade_history_downloader import get_symbol_from_instrument_url
import ipdb
import csv
import collections
import re
import argparse
import getpass

########################################################################################################
def get_args(args):

    parser = argparse.ArgumentParser(description='The script reads RH credentials from credentials.txt \
                                                  and takes appropriate action depending on following args')
    parser.add_argument('--dump_portfolio', action="store_true", help="Dumps portfolio into pf_rh.csv", default=True)
    parser.add_argument('--dump_transactions', action="store_true", help="Dumps transactions history", default=False)

    args = parser.parse_args(args)
    return args

########################################################################################################
def get_credentials():
    usename = password = qr_code = user_input = None
    with open('credentials.txt') as f:
        for line in f:
            if "<>" in line:
                user_input = True
                break
            line = line.strip()
            key, value = re.split('=', line)
            if "USER" in key:
                username = value
            if "PASS" in key:
                password = value
            if "QR" in key:
                qr_code = value
    
    if user_input:
        username = input("Username: ")
        password = getpass.getpass()

    return username, password, qr_code

########################################################################################################
def get_pf(rh):

    pf = []
    securities_in_pf = rh.securities_owned()
    positions_list = securities_in_pf['results']

    for pos in positions_list:
        ticker = get_symbol_from_instrument_url(rh, pos['instrument'])
        information = collections.OrderedDict()
        information['Symbol'] = ticker
        information['Quantity'] = float(pos['quantity'])
        information['Cost Basis Per Share'] = float(pos['average_buy_price'])
        information['Cost Basis Total'] = information['Cost Basis Per Share'] * information['Quantity']

        pf.append(information)

    return pf

########################################################################################################
def get_total_dividend_amount_paid(rh):
    
    amount_paid, amount_pending = get_total_dividend_amount()
    return amount_paid

########################################################################################################
def get_total_dividend_amount_pending(rh):
    
    amount_paid, amount_pending = get_total_dividend_amount()
    return amount_pending

########################################################################################################
def get_total_dividend_amount(rh):
    
    div_list = rh.dividends()['results']
    paid_divs = 0
    pending_divs = 0
    for div in div_list:
        if div['state'] == 'paid':
            paid_divs += float(div['amount'])
        elif div['state'] == 'pending':
            pending_divs += float(div['amount'])
        else:
            print('wtf')

    return paid_divs, pending_divs

########################################################################################################
def write_to_csv(pf):

    if len(pf) == 0:
        return
    else:
        with open('rh_pf.csv', 'w') as f:
            w = csv.DictWriter(f, pf[0])
            w.writeheader()
            for stock in pf:
                w.writerow(stock)

########################################################################################################
if __name__ == "__main__":
    
    rh = Robinhood()
    username, password, qr_code = get_credentials()

    rh.login(username=username, password=password, qr_code=qr_code)
   
    args = get_args(sys.argv[1:])
    if args.dump_portfolio:
        pf = get_pf(rh)
        write_to_csv(pf)
