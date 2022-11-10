from model import *

def main():
    s = SocketServer("0.0.0.0",9090,consol_log)
    s.run()
    input("[*] precione enter para cerrar ...\n")
if __name__ == '__main__':
    main()
