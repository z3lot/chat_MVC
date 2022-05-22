#!/usr/bin/python3

import argparse
from model import SocketServer,SocketClient

def consol_log(t,**args):
    print(t)

def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-s","--server",action="store_true",help="init server")
    group.add_argument("-c","--client",action="store_true",help="connect to server")

    parser.add_argument("ip",help="server ip")
    parser.add_argument("port",type=int,help="server port")

    args = parser.parse_args()

    if args.server == True:
        s = SocketServer(args.ip,args.port,consol_log)
        s.run()
        input("[*] precione enter para cerrar ...\n")
    elif args.client == True:
        s = SocketClient(args.ip,args.port,consol_log)
        s.run()

if __name__ == "__main__":
    main()

