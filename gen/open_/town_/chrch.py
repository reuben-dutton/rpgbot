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


class ChurchCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create a church, including all details
        surrounding the church itself.

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
        adj_path = base_dir + "\\rsrc\\gnrl\\adjs.json"
        noun_path = base_dir + "\\rsrc\\gnrl\\nouns.json"
        desc_path = base_dir + '\\corp\\desc\\chrch.txt'
        spec_word_path = base_dir + '\\rsrc\\spec\\words.json'

        # Pull information from the resource directory
        self._nouns = json.loads(open(noun_path).read())['nouns']
        self._adjs = json.loads(open(adj_path).read())['adjs']
        self._sy = json.loads(open(spec_word_path).read())["chrch"]

        # Pull the desc corpus from the corp directory
        with open(desc_path) as f:
            desc_corpus = f.read()
            self._desc_model = markovify.Text(desc_corpus)

    def gen_name(self):
        '''
            Creates a random name for the Church.

            Returns:
                A string containing the name of the Church.
        '''
        noun = random.choice(self._nouns).capitalize()
        adj = random.choice(self._adjs).capitalize()
        sy = random.choice(self._sy)
        name = "{} of the {} {}".format(sy, adj, noun)
        return name

    def gen_desc(self):
        '''
            Creates a description for the Church object.

            Returns:
                A string describing the church's origins, nature
                and/or physical appearance.
        '''
        no_sent = random.randint(0, 2)
        desc = self._desc_model.make_short_sentence(150)
        for i in range(no_sent):
            desc = desc + " " + self._desc_model.make_short_sentence(150)
        return desc

    def gen_occu(self):
        '''
            Creates random characters which 'occupy' the church.

            Returns:
                A list of Character objects.
        '''
        no_occ = random.randint(1, 3)
        occu = []
        creator = char.CharacterCreator()
        for i in range(no_occ):
            occu.append(creator.gen_char().get_json())
        return occu

    def gen_chrch(self):
        ''' Creates and returns a Church object '''
        chrchdict = dict()
        chrchdict["name"] = self.gen_name()
        chrchdict["desc"] = self.gen_desc()
        chrchdict["occu"] = self.gen_occu()
        return Church(chrchdict)


class Church:
    '''
        An abstract class designed to represent a particular church,
        including all of its particular attributes.

        Attributes:
            name (str): The name of the church.
            desc (str): A description of the church.
            occu (list(Character)): The occupants of the church.
            type (str): The type of building ("chrch").
    '''

    def __init__(self, chrchdict):
        '''
            Initializes the class and its attributes.

            Args:
                shopdict (dict) : A dictionary containing all relevant
                                  information about the church.

        '''
        self.dict = copy.deepcopy(chrchdict)
        self.dict["type"] = "chrch"

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
