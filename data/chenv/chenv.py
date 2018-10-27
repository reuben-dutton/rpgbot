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
import gen.open as openm # noqa
import gen.open_.town as town # noqa
import gen.open_.dung as dung # noqa
import gen.open_.town_.chrch as chrch # noqa
import gen.open_.town_.schl as schl # noqa
import gen.open_.town_.schl as tvrn # noqa
import gen.open_.town_.schl as shop # noqa


class ChEnv:

    def __init__(self, chenvdict):
        self.dict = chenvdict

    def get_json(self):
        return self.dict

    def __format__(self, form):
        print(form)
        return eval(form)
