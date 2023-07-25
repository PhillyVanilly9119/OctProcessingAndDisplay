"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2023 
                                        ******
                                         
        >>> Contains methods and functionality for OCT volume resampling      
                                
"""

# global imports
import os
import sys
import importlib.util

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

class PerformComputePreChecks():
    def __init__(self) -> None:
        self.is_gpu_available()
    
    def is_gpu_available(self, module_name="pytorch") -> bool:
        spam_spec = importlib.util.find_spec(module_name)
        found = spam_spec is not None
        if found:
            print("Found GPU-compute capabilities -> OCT reconstruction tasks will be carried out on a GPU")
            return found
        print("Didn't find GPU-compute capabilities -> OCT reconstruction will be carried out on a CPU")
        return found
