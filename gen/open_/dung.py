import random
import json # noqa
import os
import sys
import copy
import markovify
import numpy.random as npr

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..\\..'
sys.path.append(base_dir)


class DungeonCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create a dungeon, including all details
        surrounding the dungeon.

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
        desc_path = base_dir + '\\corp\\desc\\dung.txt'
        noun_path = base_dir + '\\rsrc\\gnrl\\nouns.json'
        adj_path = base_dir + '\\rsrc\\gnrl\\adjs.json'
        spec_word_path = base_dir + '\\rsrc\\spec\\words.json'

        # Pull information from the resource directory
        self._nouns = json.loads(open(noun_path).read())['nouns']
        self._adjs = json.loads(open(adj_path).read())['adjs']
        self._sy = json.loads(open(spec_word_path).read())["dung"]

        # Pull the desc corpus from the corp directory
        with open(desc_path) as f:
            desc_corpus = f.read()
            self._desc_model = markovify.Text(desc_corpus)

    def gen_name(self):
        '''
            Creates a random name for the dungeon.

            Returns:
                A string containing the name of the dungeon.
        '''
        noun = random.choice(self._nouns).capitalize()
        adj = random.choice(self._adjs).capitalize()
        sy = random.choice(self._sy)
        return "{} of the {} {}".format(sy, adj, noun)

    def gen_desc(self):
        '''
            Creates a description for the dungeon object.

            Returns:
                A string describing the dungeon's origins, nature
                and/or physical appearance.
        '''
        no_sent = random.randint(0, 2)
        desc = self._desc_model.make_short_sentence(150)
        for i in range(no_sent):
            desc = desc + " " + self._desc_model.make_short_sentence(140)
        return desc

    def gen_dung(self):
        ''' Creates and returns a Dungeon object '''
        dungdict = dict()
        dungdict["name"] = self.gen_name()
        dungdict["desc"] = self.gen_desc()
        return Dungeon(dungdict)


class Dungeon:
    '''
        An abstract class designed to represent a particular dungeon,
        including all of its particular attributes.

        Attributes:
            name (str): The name of the dungeon.
            desc (str): A description of the dungeon.
            type (str): The type of building ("dung")
    '''

    def __init__(self, dungdict):
        '''
            Initializes the class and its attributes.

            Args:
                dungdict (dict) : A dictionary containing all relevant
                                  information about the dungeon.

        '''
        self.dict = copy.deepcopy(dungdict)
        self.dict["type"] = "dung"

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
