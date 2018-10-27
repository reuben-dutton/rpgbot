import random
import json
import os
import sys
import copy
import markovify
import numpy.random as npr

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..\\..'
sys.path.append(base_dir)
import gen.open_.town_.chrch as chrch # noqa
import gen.open_.town_.schl as schl # noqa
import gen.open_.town_.shop as shop # noqa
import gen.open_.town_.tvrn as tvrn # noqa


class TownCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create a Town, including all details
        surrounding the Town.

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
        syllable_path = base_dir + '\\rsrc\\syllables.json'
        desc_path = base_dir + '\\corp\\desc\\town.txt'

        # Pull information from the resource directory
        self._syllables = json.loads(open(syllable_path).read())

        # Pull the desc corpus from the corp directory
        with open(desc_path) as f:
            desc_corpus = f.read()
            self._desc_model = markovify.Text(desc_corpus)

    def gen_name(self):
        '''
            Creates a random name for the Town.

            Returns:
                A string containing the name of the Town.
        '''
        # Get a number of syllables between 2 and 4.
        num_syll = random.randint(2, 4)
        # Select that number of syllables
        name_syll = random.choices(self._syllables, k=num_syll)
        # Join them together
        return "".join(name_syll).capitalize()

    def gen_desc(self):
        '''
            Creates a description for the Tavern object.

            Returns:
                A string describing the tavern's origins, nature
                and/or physical appearance.
        '''
        no_sent = random.randint(0, 2)
        desc = self._desc_model.make_short_sentence(150)
        for i in range(no_sent):
            desc = desc + " " + self._desc_model.make_short_sentence(140)
        return desc

    def gen_tvrn(self):
        return tvrn.TavernCreator().gen_tvrn().get_json()

    def gen_chrch(self):
        return chrch.ChurchCreator().gen_chrch().get_json()

    def gen_schl(self):
        return schl.SchoolCreator().gen_schl().get_json()

    def gen_shop(self):
        return shop.ShopCreator().gen_shop().get_json()

    def gen_town(self):
        ''' Creates and returns a Town object '''
        towndict = dict()
        towndict["name"] = self.gen_name()
        towndict["desc"] = self.gen_desc()
        towndict["tvrn"] = self.gen_tvrn()
        towndict["chrch"] = self.gen_chrch()
        towndict["schl"] = self.gen_schl()
        towndict["shop"] = self.gen_shop()
        return Town(towndict)


class Town:
    '''
        An abstract class designed to represent a particular town,
        including all of its particular attributes.

        Attributes:
            name (str): The name of the town.
            desc (str): A description of the town.
            occu (list(Character)): A list of Character objects
            type (str): The type of building ("town")
    '''

    def __init__(self, towndict):
        '''
            Initializes the class and its attributes.

            Args:
                towndict (dict) : A dictionary containing all relevant
                                  information about the town.

        '''
        self.dict = copy.deepcopy(towndict)
        self.dict["type"] = "town"

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
