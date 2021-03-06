import random
import json
import os
import sys # noqa
import copy
import markovify
import numpy.random as npr

dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..'


class CharacterCreator:
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
        stat_path = base_dir + '\\rsrc\\stats\\char_stats.json'
        names_path = base_dir + '\\rsrc\\gnrl\\names.json'
        character_path = base_dir + '\\rsrc\\poss\\char.json'
        characterp_path = base_dir + '\\rsrc\\prob\\char_p.json'
        bio_path = base_dir + '\\corp\\bio\\char.txt'

        # Pull information from the resource directory
        self._stats = json.loads(open(stat_path).read())
        self._names = json.loads(open(names_path).read())
        self._character = json.loads(open(character_path).read())
        self._characterp = json.loads(open(characterp_path).read())

        # Pull the bio corpus from the corp directory
        with open(bio_path) as f:
            bio_corpus = f.read()
            self._bio_model = markovify.Text(bio_corpus)

    def gen_name(self):
        '''
            Creates a name for a Character.

            Returns:
                A string containing a name randomly selected from a
                list of about 22000 assorted first names.

        '''
        return random.choice(self._names)

    def gen_stats(self):
        '''
            Creates a dictionary of stats for a Character. (An unused
            method for now)

            Returns:
                A dictionary containing a series of stat attributes
                and their respective levels.

        '''
        player_stats = dict()
        # For each stat in the stats.json resource file:
        for stat in self._stats.items():
            # Get the bounds
            lower = stat[1][0]
            higher = stat[1][1]
            # Generate a number in those bounds (somewhat normally
            # distributed).
            player_stats[stat[0]] = int(random.triangular(lower, higher))
        return player_stats

    def gen_gender(self):
        '''
            Selects a random gender for a Character.

            Returns:
                A string containing a character gender.

        '''
        rnd = self._character["genders"]
        prob = self._characterp["genders"]
        return npr.choice(rnd, size=1, p=prob)[0]

    def gen_race(self):
        '''
            Selects a random race for a Character.

            Returns:
                A string containing a character race.

        '''
        rnd = self._character["races"]
        prob = self._characterp["races"]
        return npr.choice(rnd, size=1, p=prob)[0]

    def gen_class(self):
        '''
            Selects a random class for a Character.

            Returns:
                A string containing a character class.

        '''
        rnd = self._character["classes"]
        prob = self._characterp["classes"]
        return npr.choice(rnd, size=1, p=prob)[0]

    def gen_bio(self):
        '''
            Creates a bio for the Character.

            Returns:
                A string describing the character's origins.
        '''
        # Choose a number of extra sentences between 0 and 1
        bio_sent = random.randint(0, 1)
        # Make a sentence starting with "They"
        bio = self._bio_model.make_sentence_with_start("They")
        # Add extra sentences
        for i in range(bio_sent):
            bio += " " + self._bio_model.make_short_sentence(100)
        return bio

    def gen_char(self):
        ''' Creates and returns a character object '''
        player = dict()
        player["name"] = self.gen_name()
        player["gender"] = self.gen_gender()
        player["race"] = self.gen_race()
        player["class"] = self.gen_class()
        player["bio"] = self.gen_bio()
        return Character(player)


class Character:

    def __init__(self, chardict):
        self.dict = copy.deepcopy(chardict)

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict
