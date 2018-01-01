#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 02:29:40 2017

@author: yvyas
"""
import ConfigParser, sys, argparse, os
from binancewrapper.client import BinanceClient

def parse_conf():
    conf = ConfigParser.ConfigParser()
    conf.read(['~/.moksha.cfg', os.path.expanduser('~/.moksha/credentials.cfg')])
    return conf    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help='the command to run')
    parser.add_argument("symbol", help='the ticker symbol to run command against')
    parser.add_argument('--api_key', help='api key to use')
    parser.add_argument('--api_secret', help='api secret to use')
    parser.add_argument('--exchange', help='exchange to use')
    parser.add_argument('--profile', help='api key to use')

    conf = parse_conf()
    args = parser.parse_args()
    api_key =  args.api_key
    api_secret = args.api_secret

    if api_key is None or api_secret is None:
        print "reading credentials from profile {}".format(args.profile)
    
    if args.profile is not None and conf.has_section(args.profile):
        api_key = conf.get(args.profile, 'api_key')
        api_secret = conf.get(args.profile, 'api_secret')
    
    if (api_key is None or api_secret is None) and args.profile is None:
        print "must provide api key and secret or profile"
        parser.print_help
        sys.exit(1)
        
    exchange = args.exchange
    
    if not exchange:
        exchange = args.profile.partition('_')[0]
        print "working with exchange {}".format(exchange)
    
    return {'api_key': api_key, 'api_secret': api_secret, 'exchange': exchange, 'cmd': args.cmd, 'symbol': args.symbol}

def get_client(params):
    exchange = params['exchange']
    if not exchange or exchange == "binance":
        return BinanceClient(params['api_key'], params['api_secret'])
    else:
        print "exchange {} not supported yet".format(exchange)

def main():
    args = parse_args()
    client = get_client(args)
    resp = client.execute(args['cmd'], args['symbol'])
    if resp is None:
        print "client responded with nothing"
    else:
        print resp
        
if __name__ == "__main__":
    main()
    
        
    
    
    