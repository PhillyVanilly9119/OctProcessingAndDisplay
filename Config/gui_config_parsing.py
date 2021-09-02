"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2021 Medical University of Vienna 
                                        ******
                                         
    >>> file with a class and its methods for handling *.JSON file parsing-parameters for GUI     
                                
"""

# global imports
import os
import json

class GuiConfigDataManager() :
    """ 
    simple class that loads and returns a dictionary containing 
    the config-file with the GUI parsing parameters 
    """
    def __init__(self, filename) -> None :
        self.full_file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config', filename + '.json'))

    def load_json_file(self) :
        """ returns a dict containing the json file"""
        with open(self.full_file_path) as json_file :
            json_object = json.load(json_file)
            json_file.close()
        return json_object


# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from gui_config_pasring.py ...")
    filename = 'config_gui_layout'
    GCONF = GuiConfigDataManager(filename).load_json_file()
    # print(type(GCONF))