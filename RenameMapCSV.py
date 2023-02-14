import os
import shutil

# Put the folder that contains the CSV files here:
folder = 'C:/Users/speicl/Downloads/cTitkov21-20040'

# number of rows (x) and columns (y) in your map:
nrows = 3
ncolumns = 4

#step sizes (microns)
step_x = 50
step_y = 50

#map origin (x, y)
origin = (0,0)

filelist = []
for root, dirs, files in os.walk(folder):
    for name in files:
        if os.path.splitext(name)[1] == ".CSV" or os.path.splitext(name)[1] == ".csv":
            filelist.append(os.path.join(root, name))

filelist = sorted(filelist)

if len(filelist) == nrows*ncolumns:
    i = 0
    k = 0
    while i < nrows:
        x = origin[0] + i * step_x
        j = 0
        while j < ncolumns:
            y = origin[1] + j * step_y
            filepath = filelist[k].split(os.path.sep)[0]
            newfilename = 'X{} Y{}.CSV'.format(x, y)
            #print('X: {}, Y: {}'.format(x,y))
            shutil.copy(filelist[k], filepath+'/'+newfilename)
            
            k += 1
            j += 1
        i += 1

else:
    print('number of files does not match number of rows and columns')