import sys
import os
import json

dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..\\..'
sys.path.append(base_dir)

# "VALID LOCATIONS:"
# " - open"
# " - dung"
# " - town"
# " - tvrn"
# " - shop"
#  - schl"
# " - chrch"
# "FORMATTING FOR RANDOMIZED ITEMS"
# " e.g. Character name = {{:self.char[1].name}}"
# " e.g. Monster race = {{:self.mon[0].race}}"
# "FORMATTING FOR CONSEQ"
# " e.g. Change current environment to church in the town:"
# ' "env["type"]" changed to "chenv["bld"]["chrch"]["type"]'


# Create a new event
def new_event():
    # Open events file
    events = json.loads(open(base_dir + '\\corp\\event\\events.json').read())
    f = open(base_dir + "\\corp\\event\\input.txt", "r")

    # Get the location where the event can happen
    event_loc = f.readline().strip("\n")
    # Sentence describing the event
    event_s = f.readline().strip("\n")
    action_s = []
    result_s = []
    conseq = []
    action_no = eval(f.readline().strip("\n"))
    for i in range(action_no):
        action_s.append(f.readline().strip("\n"))
        result_s.append(f.readline().strip("\n"))

    # For each result, how many commands are being executed
    for result in result_s:
        no_commands = eval(f.readline().strip("\n"))
        commands = []
        # Get the commands for each result
        for i in range(no_commands):
            commands.append(f.readline().strip("\n"))
        conseq.append(commands)

    # How many new mons, chars and opens are being generated.
    no_mon = eval(f.readline().strip("\n"))
    no_char = eval(f.readline().strip("\n"))
    no_open = eval(f.readline().strip("\n"))

    # Create the new event
    new_event = {"event_s": event_s,
                 "no_act": len(action_s),
                 "action_s": action_s,
                 "result_s": result_s,
                 "conseq": conseq,
                 "no_mon": no_mon,
                 "no_char": no_char,
                 "no_open": no_open}

    # Add the new event to the events file and save
    events[event_loc].append(new_event)

    with open(base_dir + '\\corp\\event\\events.json', 'w') as outfile:
        json.dump(events, outfile)

    f.close()


new_event()
