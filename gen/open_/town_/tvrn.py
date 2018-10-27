import random
import json
import os
import sys
import copy
import markovify
import numpy.random as npr

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..\\..\\..'
sys.path.append(base_dir)
import gen.char as char # noqa


class TavernCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create a Tavern, including all details
        surrounding the Tavern.

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
        adj_path = base_dir + "\\rsrc\\grnl\\adjs.json"
        noun_path = base_dir + "\\rsrc\\grnl\\nouns.json"
        desc_path = base_dir + '\\corp\\desc\\tvrn.txt'

        # Pull information from the resource directory
        self._nouns = json.loads(open(noun_path).read())['nouns']
        self._adjs = json.loads(open(adj_path).read())['adjs']

        # Pull the desc corpus from the corp directory
        with open(desc_path) as f:
            desc_corpus = f.read()
            self._desc_model = markovify.Text(desc_corpus)

    def gen_name(self):
        '''
            Creates a random name for the Tavern.

            Returns:
                A string containing the name of the Tavern.
        '''
        noun = random.choice(self._nouns).capitalize()
        adj = random.choice(self._adjs).capitalize()
        name = "The {} {}".format(adj, noun)
        return name

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
            desc = desc + " " + self._desc_model.make_short_sentence(150)
        return desc

    def gen_occu(self):
        '''
            Creates random characters which 'occupy' the tavern.

            Returns:
                A list of Character objects.
        '''
        no_occ = random.randint(1, 5)
        occu = []
        creator = char.CharacterCreator()
        for i in range(no_occ):
            occu.append(creator.gen_char().get_json())
        return occu

    def gen_tvrn(self):
        ''' Creates and returns a Tavern object '''
        tvrndict = dict()
        tvrndict["name"] = self.gen_name()
        tvrndict["desc"] = self.gen_desc()
        tvrndict["occu"] = self.gen_occu()
        return Tavern(tvrndict)


class Tavern:
    '''
        An abstract class designed to represent a particular Tavern,
        including all of its particular attributes.

        Attributes:
            name (str): The name of the tavern.
            desc (str): A description of the tavern.
            occu (list(Character)): The occu of the tavern.
            type (str): The type of building ("tvrn").
    '''

    def __init__(self, tvrndict):
        '''
            Initializes the class and its attributes.

            Args:
                tvrndict (dict) : A dictionary containing all relevant
                                  information about the tavern.

        '''
        self.dict = copy.deepcopy(tvrndict)
        self.dict["type"] = "tvrn"

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
