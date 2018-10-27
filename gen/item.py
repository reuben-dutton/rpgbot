import random
import json # noqa
import os
import sys # noqa
import copy
import markovify # noqa
import numpy.random as npr

dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..'


class ItemCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create a character, including all details surrounding
        the character.

        Attributes:
            seed (str): an alphanumeric value intended to seed the RNG
    '''

    def __init__(self, seed=None):
        '''
            Initializes the class.

            Args:
                seed (str): for seeding the RNG
        '''
        if seed is not None:
            random.seed(seed)
            npr.seed(seed)

        # Setting filepaths

        # Pull information from the resource directory

    def gen_name(self):
        '''
            Creates a name for an Item

            Returns:
                A string containing a name randomly selected from a
                list of about 22000 assorted first names.

        '''
        pass

    def gen_mon(self):
        ''' Creates and returns a character object '''
        desc = dict()
        desc["name"] = self.gen_name()
        return Item(desc)


class Item:
    '''
        An abstract class designed to represent a particular Item,
        including all of its particular attributes.

        Attributes:
            seed (str): an alphanumeric value intended to seed the RNG
    '''

    def __init__(self, itemdict):
        self.dict = copy.deepcopy(itemdict)

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
