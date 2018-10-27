import random
import json # noqa
import os
import sys
import copy
import markovify
import numpy.random as npr

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..'
sys.path.append(base_dir)
import gen.open_.town as town # noqa
import gen.open_.dung as dung # noqa


class OpenCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create an open area, including all details
        surrounding the open area.

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
        desc_path = base_dir + '\\corp\\desc\\open.txt'
        noun_path = base_dir + '\\rsrc\\gnrl\\nouns.json'
        adj_path = base_dir + '\\rsrc\\gnrl\\adjs.json'
        spec_word_path = base_dir + '\\rsrc\\spec\\words.json'

        # Pull information from the resource directory
        self._nouns = json.loads(open(noun_path).read())['nouns']
        self._adjs = json.loads(open(adj_path).read())['adjs']
        self._sy = json.loads(open(spec_word_path).read())["open"]

        # Pull the desc corpus from the corp directory
        with open(desc_path) as f:
            desc_corpus = f.read()
            self._desc_model = markovify.Text(desc_corpus)

    def gen_name(self):
        '''
            Creates a random name for the open area.

            Returns:
                A string containing the name of the open area.
        '''
        noun = random.choice(self._nouns).capitalize()
        adj = random.choice(self._adjs).capitalize()
        sy = random.choice(self._sy)
        if noun[-1] == 's' or noun[-2:-1] == 'sh':
            name = "The {} of {} {}es".format(sy, adj, noun)
        elif noun[-1] == 'y':
            name = "The {} of {} {}ies".format(sy, adj, noun[:-1])
        else:
            name = "The {} of {} {}s".format(sy, adj, noun)
        return name

    def gen_desc(self):
        '''
            Creates a description for the open area.

            Returns:
                A string describing the open area's origins, nature
                and/or physical appearance.
        '''
        no_sent = random.randint(0, 2)
        desc = self._desc_model.make_short_sentence(150)
        for i in range(no_sent):
            desc = desc + " " + self._desc_model.make_short_sentence(140)
        return desc

    def gen_dungs(self):
        no_dungs = 3
        dungs = []
        for i in range(no_dungs):
            dungs.append(dung.DungeonCreator().gen_dung().get_json())
        return dungs

    def gen_towns(self):
        no_towns = 5
        towns = []
        for i in range(no_towns):
            towns.append(town.TownCreator().gen_town().get_json())
        return towns

    def gen_open(self):
        ''' Creates and returns an Open object '''
        opendict = dict()
        opendict["name"] = self.gen_name()
        opendict["desc"] = self.gen_desc()
        opendict["dungs"] = self.gen_dungs()
        opendict["towns"] = self.gen_towns()
        return Open(opendict)


class Open:
    '''
        An abstract class designed to represent a particular open
        area, including all of its particular attributes.

        Attributes:
            name (str): The name of the open area.
            desc (str): A description of the open area.
            dungs (list(Dungeon)) : The dungeons in the open area
            towns (list(Town)) : The towns in the open area
            type (str): The type of environment ("open")
    '''

    def __init__(self, opendict):
        '''
            Initializes the class and its attributes.

            Args:
                opendict (dict) : A dictionary containing all relevant
                                  information about the open area.

        '''
        self.dict = copy.deepcopy(opendict)
        self.dict["type"] = "open"

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
