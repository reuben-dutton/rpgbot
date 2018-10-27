from PIL import Image, ImageDraw, ImageFilter, ImageFont # noqa
import os
import sys
import random # noqa
import math # noqa
import string # noqa
import textwrap as tw # noqa
import json

# Getting additional modules from the rpgbot directory
dir_p = os.path.dirname(os.path.realpath(__file__))
base_dir = dir_p + '\\..'
sys.path.append(base_dir)
import data.chda.chda as chdam # noqa
import data.chenv.chenv as chenvm # noqa

font = {"r": {'path': "IBM_VGA8"},
        "b": {'path': "RobotoMono-Bold"},
        "i": {'path': "RobotoMono-Italic"},
        "bi": {'path': "RobotoMono-BoldItalic"}}

reacts = ["Love",
          "Haha",
          "Wow",
          "Sad",
          "Angry"]

f_s = 64
f_w, f_h = 32, 48
f_c = (40, 200, 40, 255)

fonts = dict()
for key, item in font.items():
    path = base_dir + "\\rsrc\\font\\{}.ttf".format(item['path'])
    fonts[key] = ImageFont.truetype(font=path, size=f_s)

margins = (120, 120)
left_margin = margins[0]
top_margin = 120
image_dim = (2400, 2000)
image_col = (0, 0, 0, 255)

display_dim = (image_dim[0] - sum(margins), image_dim[1] - top_margin)
char_width = display_dim[0] // f_w
char_nlgap = 16


class ImageCreator():

    def __init__(self):
        self.im = Image.new("RGBA", image_dim, color=image_col)
        self.c = ImageDraw.Draw(self.im)

        self.parse_text()
        self.save_image()

    def parse_text(self):
        event_path = base_dir + "\\data\\curr\\event.json"
        event = json.loads(open(event_path).read())
        final_path = base_dir + "\\data\\curr\\final.json"
        final = json.loads(open(final_path).read()) # noqa

        action_s = " > " + final["action_s"]
        result_s = final["result_s"]
        result_s = tw.fill(result_s, width=char_width)
        event_s = event["event_s"]
        event_s = tw.fill(event_s, width=char_width)
        poss_actions = event["action_s"]
        for i in range(len(poss_actions)):
            j = len(poss_actions[i])
            k = len(reacts[i])
            space = " " * (52 - j - k)
            poss_actions[i] += space + "({})".format(reacts[i])

        main_text = "\n\n".join([action_s, result_s])
        main_text = ("\n." * 5 + "\n\n").join([main_text, event_s])

        options = "\n\n     > ".join(poss_actions)
        main_text = "\n\n\n     > ".join([main_text, options])

        pos = (left_margin, top_margin)
        self.c.text(pos, main_text, font=fonts['r'], fill=f_c)

    def save_image(self):
        self.im.save(base_dir + '\\vote\\image.png', 'PNG')
