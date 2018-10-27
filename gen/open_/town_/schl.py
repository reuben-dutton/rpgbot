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


class SchoolCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create a school, including all details
        surrounding the school.

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
        desc_path = base_dir + '\\corp\\desc\\schl.txt'
        spec_word_path = base_dir + '\\rsrc\\spec\\words.json'

        # Pull information from the resource directory
        self._nouns = json.loads(open(noun_path).read())['nouns']
        self._adjs = json.loads(open(adj_path).read())['adjs']
        self._sy = json.loads(open(spec_word_path).read())["schl"]

        # Pull the desc corpus from the corp directory
        with open(desc_path) as f:
            desc_corpus = f.read()
            self._desc_model = markovify.Text(desc_corpus)

    def gen_name(self):
        '''
            Creates a random name for the School.

            Returns:
                A string containing the name of the School.
        '''
        noun = random.choice(self._nouns).capitalize()
        adj = random.choice(self._adjs).capitalize()
        sy = random.choice(self._sy)
        if noun[-1] == 's' or noun[-2:-1] == 'sh':
            name = "{} for {} {}es".format(sy, adj, noun)
        elif noun[-1] == 'y':
            name = "{} for {} {}ies".format(sy, adj, noun[:-1])
        else:
            name = "{} for {} {}s".format(sy, adj, noun)
        return name

    def gen_desc(self):
        '''
            Creates a description for the School object.

            Returns:
                A string describing the school's origins, nature
                and/or physical appearance.
        '''
        no_sent = random.randint(0, 2)
        desc = self._desc_model.make_short_sentence(150)
        for i in range(no_sent):
            desc = desc + " " + self._desc_model.make_short_sentence(150)
        return desc

    def gen_occu(self):
        '''
            Creates random characters which 'occupy' the school.

            Returns:
                A list of Character objects.
        '''
        no_occ = random.randint(1, 3)
        occu = []
        creator = char.CharacterCreator()
        for i in range(no_occ):
            occu.append(creator.gen_char().get_json())
        return occu

    def gen_schl(self):
        ''' Creates and returns a School object '''
        schldict = dict()
        schldict["name"] = self.gen_name()
        schldict["desc"] = self.gen_desc()
        schldict["occu"] = self.gen_occu()
        return School(schldict)


class School:
    '''
        An abstract class designed to represent a particular school,
        including all of its particular attributes.

        Attributes:
            name (str): The name of the school.
            desc (str): A description of the school.
            occu (list(Character)): The occu of the school.
            type (str): The type of building ("schl").
    '''

    def __init__(self, schldict):
        '''
            Initializes the class and its attributes.

            Args:
                schldict (dict) : A dictionary containing all relevant
                                  information about the school.

        '''
        self.dict = copy.deepcopy(schldict)
        self.dict["type"] = "schl"

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
