import numpy as np
import math
#
def sample_function():
    def value(position):
        return math.pow(position[0,0],2)+math.pow(position[0,1],2)+1
    return value,2,-1,1