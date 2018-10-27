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


class ShopCreator:
    '''
        An abstract class designed to contain all of the methods
        used to create a Shop, including all details
        surrounding the Shop.

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
        desc_path = base_dir + "\\corp\\desc\\shop.txt"

        # Pull information from the resource directory
        self._nouns = json.loads(open(noun_path).read())['nouns']
        self._adjs = json.loads(open(adj_path).read())['adjs']

        # Pull the desc corpus from the corp directory
        with open(desc_path) as f:
            desc_corpus = f.read()
            self._desc_model = markovify.Text(desc_corpus)

    def gen_owner(self):
        '''
            Creates an owner for the shop.

            Returns:
                A Character object.

        '''
        return char.CharacterCreator().gen_char().get_json()

    def gen_name(self, name):
        '''
            Creates a random name for the Shop.

            Args:
                name (str) : A string containing the name of the
                             owner of the shop.

            Returns:
                A string containing the name of the Shop.
        '''
        noun = random.choice(self._nouns).capitalize()
        adj = random.choice(self._adjs).capitalize()
        if noun[-1] == 's' or noun[-2:-1] == 'sh':
            name = "{}'s {} {}es".format(name, adj, noun)
        elif noun[-1] == 'y':
            name = "{}'s {} {}ies".format(name, adj, noun[:-1])
        else:
            name = "{}'s {} {}s".format(name, adj, noun)
        return name

    def gen_desc(self):
        '''
            Creates a description for the Shop object.

            Returns:
                A string describing the shop's origins, nature
                and/or physical appearance.
        '''
        no_sent = random.randint(0, 2)
        desc = self._desc_model.make_short_sentence(150)
        for i in range(no_sent):
            desc = desc + " " + self._desc_model.make_short_sentence(150)
        return desc

    def gen_occu(self):
        '''
            Creates random characters which 'occupy' the shop.

            Returns:
                A list of Character objects.
        '''
        no_occu = random.randint(0, 2)
        occu = []
        creator = char.CharacterCreator()
        for i in range(no_occu):
            occu.append(creator.gen_char().get_json())
        return occu

    def gen_shop(self):
        ''' Creates and returns a Shop object '''
        shopdict = dict()
        shopdict["owner"] = self.gen_owner()
        shopdict["name"] = self.gen_name(shopdict["owner"]["name"])
        shopdict["desc"] = self.gen_desc()
        shopdict["occu"] = self.gen_occu()
        return Shop(shopdict)


class Shop:
    '''
        An abstract class designed to represent a particular Shop,
        including all of its particular attributes.

        Attributes:
            name (str): The name of the shop.
            owner (Character) : The owner of the shop.
            desc (str): A description of the shop.
            occu (list(Character)): The occupants of the shop.
            type (str): The type of building ("shop").
    '''

    def __init__(self, shopdict):
        '''
            Initializes the class and its attributes.

            Args:
                shopdict (dict) : A dictionary containing all relevant
                                  information about the shop.

        '''
        self.dict = copy.deepcopy(shopdict)
        self.dict["type"] = "shop"

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
