import os
import glob
import subprocess

# Clear and then compile gui files
all_py_files = glob.glob('design/*.py')

for file in all_py_files:
    print('Removing file \'{}\''.format(file))
    os.remove(file)

all_ui_files = glob.glob('design/*.ui')

for file in all_ui_files:
    folder, filename = os.path.split(file)
    filename = os.path.splitext(filename)[0] + '.py'
    print('Compiling file \'{}\''.format(file))
    subprocess.run(['pyuic6', file, '-o', os.path.join(folder, filename)])
