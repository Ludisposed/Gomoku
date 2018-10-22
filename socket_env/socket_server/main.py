# -*- coding: utf-8 -*-
import threading
import argparse
import logging
import settings
from server import GomokuServer, GomokuRequestHandler

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s')


def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket server @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python main.py -p 9999
'''
                                        )
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    parser.add_argument('-r','--row', type=int, default=5, help='board row length')
    parser.add_argument('-c','--column', type=int, default=5, help='board column length')
  
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    logger = logging.getLogger('Main')
    args = parse_options()
    # settings.board_size = (args.row, args.column)
    # print(settings.board_size)
    logger.info(f"board size {args.row}/{args.column}")
    address = ('localhost', args.port)
    server = GomokuServer(address, GomokuRequestHandler)
    ip, port = server.server_address

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(False)
    t.start()
    logger.info(f"Server on {ip}:{port}")

