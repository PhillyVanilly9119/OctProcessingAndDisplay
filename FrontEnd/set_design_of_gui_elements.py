"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
        >>> Contains methods and functionality to set the style elements of the GUI  
                                
"""

# global imports
from typing import List

test_data = ["color: rgb(17, 29, 78)",
             "border-style: outset",
             "border-width: 2px"]

med_uni_vienna_color_code_rgb_2021 = {
    "dark_blue": (17, 29, 78),
    "light_blue1": (95, 180, 229),
    "light_blue2": (151, 207, 236),
    "light_blue3": (181, 220, 241),
    "light_blue4": (207, 232, 246),
    "light_blue5": (231, 243, 251),
    "green1": (47, 142, 145),
    "green2": (132, 201, 188),
    "green3": (168, 215, 205),
    "green4": (200, 229, 223),
    "green5": (228, 242, 239),
    "skin1": (240, 167, 148),
    "skin2": (248, 192, 176),
    "skin3": (250, 209, 196),
    "skin4": (252, 225, 216),
    "skin5": (253, 240, 235),
    "skin6": (254, 247, 245)
    }


class RgbColorCodeManager():
    def __init__(self, rgb_dict: dict) -> None:
        self.rgb_dict = {k.lower(): v for k, v in rgb_dict.items()}
        
    def get_rgb_tuple_from_dict(self, key: str) :
        """ returns RGB-tuple from dictionary, if the key exists """
        if not key.lower() in self.rgb_dict :
            print("Key not found")
            return
        return self.rgb_dict.get(key)
        
        
Colors = RgbColorCodeManager(med_uni_vienna_color_code_rgb_2021)
key = Colors.get_rgb_tuple_from_dict("green1")
print(key)


def insert_strings_to_setStyleSheet(strings: List) -> str :
    """ returns a concatented string of the parameters 
    NOTE: Designed to be directly CALLABLE from 'main_window' """
    for c_str in enumerate(strings) :
        print(c_str)
        strings[c_str] = check_if_semicolon_in_string(c_str)
    print(strings)    
    ret_str = strings.join(check_if_semicolon_in_string())
    print(ret_str)

def check_if_semicolon_in_string(string: str) -> str :
    """     Appends semicolon ';' to be parseable by PyQt5's .setStyleSheet method """
    if string[-1] != ';' :
        string += ';'
    return string
     
# insert_strings_to_setStyleSheet(test_data)
    


