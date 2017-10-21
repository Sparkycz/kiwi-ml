
import argparse

from kiwi_ml.app import KiwiMl

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--host', action='store', dest='host', required=True, help="IP address of the API")
    parser.add_argument('-p', '--port', action='store', dest='port', type=int, default=8080, help="Host of the API")
    parser.add_argument('-n', '--max', action='store', dest='x_min_value', type=float, default=-10, help="Min. value")
    parser.add_argument('-x', '--min', action='store', dest='x_max_value', type=float, default=10, help="Max. value")

    args = parser.parse_args()

    kiwi_ml = KiwiMl(args.host, args.port, args.x_min_value, args.x_max_value)
    kiwi_ml.run()
