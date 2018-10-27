import os
import sys

# Getting additional modules from the rpgbot directory
base_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(base_dir)
import event.event as event # noqa
import vote.vote as vote # noqa
import updt.updt as updt # noqa


def main(test=False):
    e = event.EventSelector()
    v = vote.Vote()
    u = updt.Updater()

    e.gen_event()
    if test:
        v.make_image()
        v.sim_vote(eval(input("What number choice?\n")))
    else:
        v.retrieve_vote()
    u.upd_items()


main(test=True)
