import random
import json
import os
import sys
import copy

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..'
sys.path.append(base_dir)
import gen.char as char # noqa
import gen.mon as mon # noqa
import gen.open as openm # noqa
import data.chenv.chenv as chenvm # noqa
import data.chda.chda as chdam # noqa


class EventSelector:
    '''
        Abstract class that allows for the selection of a random event
        using given character and environment data.

    '''

    def __init__(self):
        ''' Initializing the class '''
        # Setting filepaths
        chda_path = base_dir + "\\data\\chda\\main.json"
        chenv_path = base_dir + "\\data\\chenv\\main.json"
        events_path = base_dir + "\\corp\\event\\events.json"
        # For updating the current event files (for vote making)
        self.curr_path = base_dir + "\\data\\curr\\event.json"

        # Retrieving data/corpuses from data and corp folders
        # Current character data
        self.chda = json.loads(open(chda_path).read())
        # Current environment data
        self.chenv = json.loads(open(chenv_path).read())
        # Possible events
        self.events = json.loads(open(events_path).read())

    def gen_event(self):
        ''' Create a random event '''
        # Get the current bld type (for determining which events are
        # possible)
        loc_type = self.chda["location"]["type"]

        # Generate a random event (using the current seed)
        eventdict = random.choice(self.events[loc_type])
        event = Event(eventdict)
        event.add_things()
        event.sub_items(self.chenv, self.chda)

        # Update the current event
        ef = event.get_json()

        with open(self.curr_path, 'w') as json_file:
            json.dump(ef, json_file)


class Event:
    '''
        An abstract class intended to represent an event, including
        randomly generated entities and specifics of actions that
        can be taken in response to said event.
    '''

    def __init__(self, eventdict):
        ''' Initialize the class '''
        self.dict = copy.deepcopy(eventdict)

    def __format__(self, form):
        return eval(form)

    def get_json(self):
        return self.dict

    def add_things(self):
        self.dict["mons"] = []
        for i in range(self.dict["no_mon"]):
            self.dict["mons"].append(self.rand_mon())

        self.dict["chars"] = []
        for i in range(self.dict["no_char"]):
            self.dict["chars"].append(self.rand_char())

        self.dict["opens"] = []
        for i in range(self.dict["no_open"]):
            self.dict["opens"].append(self.rand_open())

    def rand_mon(self):
        return mon.MonsterCreator().gen_mon().get_json()

    def rand_char(self):
        return char.CharacterCreator().gen_char().get_json()

    def rand_open(self):
        return openm.OpenCreator().gen_open().get_json()

    def sub_items(self, chenv, chda):
        ''' Format event strings with the correct names and items '''
        d = {'event': self.dict, 'chenv': chenv, 'chda': chda}
        new = self.dict["event_s"].format(**d)
        self.dict["event_s"] = new
        new = []
        for item in self.dict["action_s"]:
            new.append(item.format(**d))
        self.dict["action_s"] = new
        new = []
        for item in self.dict["result_s"]:
            new.append(item.format(**d))
        self.dict["result_s"] = new
