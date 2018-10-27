import json
import os
import sys
import facebook # noqa
import requests # noqa

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..'
sys.path.append(base_dir)
import vote.pic as pic # noqa


class Vote:

    def __init__(self):
        ''' Initializing the class '''
        # Setting file path
        self.event_path = base_dir + "\\data\\curr\\event.json"
        self.final_path = base_dir + "\\data\\curr\\final.json"

        # Getting facebook graph stuff
        '''
        env_path = base_dir + "\\env.json"
        env = json.loads(open(env_path).read())
        page_id = env['page_id']
        _access_token = env['page_token']
        graph = facebook.GraphAPI(access_token=_access_token)
        '''

    def make_vote(self):
        # Make later
        pass

    def make_image(self):
        pic.ImageCreator()

    def retrieve_vote(self):
        # Make later
        pass

    def sim_vote(self, choice):
        ''' Simulate a vote (for testing purposes) '''
        # Retrieving event data (sentences)
        self.e = json.loads(open(self.event_path).read())
        self.sit = self.e["event_s"]
        self.poss = self.e["action_s"]
        action = self.e["action_s"][choice]
        result = self.e["result_s"][choice]
        conseq = self.e["conseq"][choice]
        mons = self.e["mons"]
        chars = self.e["chars"]
        opens = self.e["opens"]
        final = {
            "action_s": action,
            "result_s": result,
            "conseq": conseq,
            "mons": mons,
            "chars": chars,
            "opens": opens}
        with open(self.final_path, 'w') as f:
            json.dump(final, f)
