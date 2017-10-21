
import logging

import requests
import matplotlib.pyplot as plt
import numpy as np


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s ' + logging.BASIC_FORMAT, datefmt='%Y-%m-%dT%H:%M:%SZ')


class KiwiMl(object):
    """Tools for processing data from Kiwi API and looking for original formula of the Black box."""
    def __init__(self, host, port, x_min_value, x_max_value):
        """
        Args:
            host (str): IP address of Kiwi API.
            port (int): Port of Kiwi API.
            x_min_value (float): Minimal value of x coordinate
            x_max_value (float): Maximal value of y coordinate
        """
        self.host = host
        self.port = port
        self.x_min_value = x_min_value
        self.x_max_value = x_max_value

    def run(self):
        """Main run function for loading data and showing it in plot."""
        logging.debug('Loading of base coordinates')
        x_list, y_list = self._load_base_coordinates()
        logging.debug('Interpolation of several points')
        x_vals, y_interp = self._interpolate(x_list, y_list)

        logging.debug('Calculate the formula')
        formula = self._calculate_formula(x_vals, y_interp)

        logging.debug('Showing of the plot')
        self._show_plot(x_vals, y_interp, formula)

    def _calculate_formula(self, x_vals, y_vals):
        polyvals = np.polyfit(x_vals, y_vals, 10)

        formula = ''
        for polyval, exponent in zip(polyvals, reversed(range(len(polyvals)))):
            if round(polyval) == 0.0:
                continue

            if formula != '':
                formula += ' + '

            formula += str(int(round(polyval)))
            if exponent != 0:
                formula += 'x^{}'.format(exponent)

        return 'y = ' + formula

    def _show_plot(self, x_vals, y_vals, formula):
        """Shows plot with data.

        Args:
            x_vals (list[float]): Values of 'x' coordinate
            y_vals (list[float]): Values of 'y' coordinate
            formula (str): Formula for showing it in the plot
        """
        fig = plt.figure()
        fig.suptitle(formula, fontsize=14, fontweight='bold')

        plt.plot(x_vals, y_vals, '-r')

        plt.show()

    def _interpolate(self, x_list, y_list):
        """Interpolates several points

        Args:
            x_list (list[float]): Values of 'x' coordinate
            y_list (list[float]): Values of 'y' coordinate

        Returns:
            tuple(list[float], list[float]): Values of 'x' coordinate, Values of 'y' coordinate
        """
        x_vals = [_x for _x in np.linspace(self.x_min_value, self.x_max_value, 500)]

        y_interp = np.interp(x_vals, x_list, y_list)

        return x_vals, y_interp

    def _load_base_coordinates(self):
        """Loads several points from Kiwi API.

        Returns:
            tuple(list, list): Values of 'x' coordinate, Values of 'y' coordinate
        """
        x_list, y_list = [], []
        for _x in np.linspace(self.x_min_value, self.x_max_value, num=100):
            coordinates = self._request_api(_x)['data']
            if coordinates['y'] is None:
                continue

            x_list.append(coordinates['x'])
            y_list.append(coordinates['y'])

        return x_list, y_list

    def _request_api(self, x):
        """Requests Kiwi API.

        Args:
            x (float): 'x' value

        Returns:
            dict: Response from Kiwi API
        """
        response = requests.get('http://{}:{}/api/do_measurement?x={}'.format(self.host, self.port, x))

        return response.json()



