"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
    >>> file with a class and its methods for handling *.JSON file parsing-parameters for GUI     
                                
"""

# global imports
import os
import json

# custom imports 
from rgbcolorcodemanager import RgbColorCodeManager


class GuiConfigDataManager(RgbColorCodeManager) :
    """ 
    simple class that creates a dictionary containing the content of a config-file 
    with the GUI parsing parameters and returns them as parseable parameters
    """
    def __init__(self, filename: str='config_gui_layout') -> None :
        self.full_file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config', filename + '.json')) 

    def load_json_file(self) -> dict :
        """ returns a dict containing the json file"""
        with open(self.full_file_path) as json_file :
            json_object = json.load(json_file)
            json_file.close()
        return json_object
    
    def get_json_file_var(self, json_var: str) -> str :
        """ returns value of a string to be expected in json file
        TODO: rethink if method needed... """
        pass


# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from < gui_config_pasring.py > ...")
    filename = 'config_gui_layout'
    GCONF = GuiConfigDataManager(filename).load_json_file()
    print(GCONF["testVar"])