# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 15:28:15 2024

@author: ridva
"""

import pandas as pd
import numpy  as np


# =============================================================================
def Sort_Rows(df_in):

    numRows, numCols          = df_in.shape
    temp_array                = np.array(df_in).copy()
    temp_array_sorted         = np.sort(temp_array, axis=1)
    temp_array_sorted_flipped = np.fliplr(temp_array_sorted)
    df_temp_sorted            = pd.DataFrame(temp_array_sorted_flipped, columns = list(range(numCols)), index = df_in.index)
    
    return df_temp_sorted
    
    


    
    
    
    
    
    
    
    