"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
        >>> Contains methods and functionality to set the style elements of the GUI  
                                
"""

# global imports
from typing import List

test_data = ("color: rgb(17, 29, 78)",
             "border-style: outset",
             "border-width: 2px")


def insert_strings_to_setStyleSheet(strings: List) -> str :
    """ returns a concatented string of the parameters 
    NOTE: Designed to be directly CALLABLE from 'main_window' """
    print(strings)

def check_if_semicolon_in_string(string: str) -> str :
    """     Appends semicolon ';' to be parseable by PyQt5's .setStyleSheet method """
    if string[-1] != ';' :
        string += ';'
    return string
     
insert_strings_to_setStyleSheet(test_data)
    

