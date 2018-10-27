import random # noqa
import json # noqa
import os
import sys
import copy # noqa
import numpy.random as npr # noqa

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..\\..'
sys.path.append(base_dir)


class ChDa:

    def __init__(self, chdadict):
        self.dict = chdadict

    def get_json(self):
        return self.dict

    def __format__(self, form):
        print(form)
        return eval(form)
