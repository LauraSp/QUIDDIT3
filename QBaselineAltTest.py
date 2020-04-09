# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import QBaselineAlt as bl_alt
import QBaseline as bl
import os
from pathlib import Path


input_path = Path('C:/Users/l.speich/Documents/Mersmann colour vs platelets/IR')
output_path = Path('C:/Users/l.speich/Desktop/bl_test')
output_path2 = Path('C:/Users/l.speich/Desktop/bl_test2')
#file_to_open = data_folder / "raw_data.txt"

#input_path = r'C:\Users\l.speich\Desktop\Mersmann\IR'
#output_path = r'C:\Users\l.speich\Desktop\bl_test'

spectra = []
filenames = []

for root, dirs, files in os.walk(input_path):    
    for name in files:
        if os.path.splitext(name)[1] == '.CSV' or os.path.splitext(name)[1] == '.csv':
            spectra.append(os.path.join(root,name))
            filenames.append(name)

i = 1
for spec in spectra:
    bl_alt.remove_baseline_alt(spec, output_path, )
    bl.remove_baseline(spec, output_path2)
    print('processing spectrum {} of {}'.format(i, len(spectra)))
    i += 1
    
for file in filenames:
    path_cor_old = os.path.join(output_path2, ('c'+os.path.basename(file)))
    path_cor_new = os.path.join(output_path, ('c'+os.path.basename(file)))
    
    spec_old = np.loadtxt(path_cor_old, delimiter = ',')
    spec_new = np.loadtxt(path_cor_new, delimiter = ',')
    
    plt.figure()
    plt.plot(spec_old[:,0], spec_old[:,1], '-', label='old correction')
    plt.plot(spec_new[:,0], spec_new[:,1], '-', label='new correction')
    
    plt.legend(loc='best')
    
    ax = plt.gca()
    ax.invert_xaxis()