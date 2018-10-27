import json
import os
import sys

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..'
sys.path.append(base_dir)
import data.chda.chda as chdam # noqa
import data.chenv.chenv as chenvm # noqa
import event.event as eventm # noqa


class Updater:

    def __init__(self):
        # Setting filepaths
        self.chda_path = base_dir + "\\data\\chda\\main.json"
        self.chenv_path = base_dir + "\\data\\chenv\\main.json"
        self.event_path = base_dir + "\\data\\curr\\event.json"
        self.final_path = base_dir + "\\data\\curr\\final.json"

    def upd_items(self):
        '''
            Update data folder with what needs to be changed (as a
            result of an action taken).
        '''
        # Retrieving data/corpuses from data and corp folders
        self.chda = json.loads(open(self.chda_path).read())
        self.chenv = json.loads(open(self.chenv_path).read())
        self.event = json.loads(open(self.event_path).read())
        self.final = json.loads(open(self.final_path).read())

        # Get lists of item names and new values
        self.conseq = self.final["conseq"]

        # Set variables
        chda = chdam.ChDa(self.chda)
        chenv = chenvm.ChEnv(self.chenv)
        event = eventm.Event(self.event) # noqa

        # For each variable that needs to be changed, execute a command
        # designated in the event file (this will change something in
        # either chda or chenv)
        for i in range(len(self.conseq)):
            exec(self.conseq[i])

        # Save changes to data files
        with open(self.chda_path, 'w') as f:
            json.dump(chda.get_json(), f)
        with open(self.chenv_path, 'w') as f:
            json.dump(chenv.get_json(), f)
