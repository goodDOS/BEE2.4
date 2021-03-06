import tkinter
from tkinter.constants import *
from tkinter.font import Font as tkFont

import utils

LOGGER = utils.getLogger(__name__)

class tkRichText(tkinter.Text):
    """A version of the TK Text widget which allows using special formatting.

    The format for the text is a list of tuples, where each tuple is (type, text).
    Types:
     - "line" : standard line, with carriage return after.
     - "bold" : bolded text, with carriage return
     - "bullet" : indented with a bullet at the beginning
     - "list" : indented with "1. " at the beginning, the number increasing
     - "break" : A carriage return. This ignores the text part.
     - "rule" : A horizontal line. This ignores the text part.
     - "invert": White-on-black text.
    """
    def __init__(self, parent, width=10, height=4, font="TkDefaultFont"):
        super().__init__(
            parent,
            width=width,
            height=height,
            wrap="word",
            font=font,
        )
        self.tag_config(
            "underline",
            underline=1,
        )
        self.tag_config(
            "invert",
            background='black',
            foreground='white',
        )
        self.tag_config(
            "indent",
            lmargin1="10",
            lmargin2="25",
        )
        self.tag_config(
            "hrule",
            relief="sunken",
            borderwidth=1,
            font=tkFont(size=1),
        )
        self['state'] = "disabled"

    _insert = tkinter.Text.insert

    def insert(*args, **kwargs):
        pass

    def set_text(self, desc):
        """Write the rich-text into the textbox."""
        self['state'] = "normal"
        self.delete(1.0, END)
        if isinstance(desc, str):
            super().insert("end", desc)
        else:
            list_ind = 1
            for data in desc:
                line_type = data[0].casefold()
                if line_type == "line":
                    super().insert("end", data[1] + "\n")
                elif line_type == "under":
                    super().insert("end", data[1] + "\n", "underline")
                elif line_type == "invert":
                    super().insert("end", data[1] + "\n", "invert")
                elif line_type == "bullet":
                    super().insert("end", '\u2022 ' + data[1] + "\n", "indent")
                elif line_type == "list":
                    super().insert(
                        "end",
                        str(list_ind) + ". " + data[1] + "\n",
                        "indent",
                    )
                    list_ind += 1
                elif line_type == "break":
                    super().insert("end", '\n')
                elif line_type == "rule":
                    super().insert("end", " \n", "hrule")
                    # Horizontal rules are created by applying a tag to a
                    # space + newline (which affects the whole line)
                    # It decreases the text size (to shrink it vertically),
                    # and gives a border
                else:
                    LOGGER.warning('Unknown description type "{}"!', line_type)
            # delete the trailing newline
            self.delete(self.index(END)+"-1char", "end")
        self['state'] = "disabled"