import os

output = os.system('cp -r /root/hptools/oosha/ \./')

if output != 0:
    print("Failed to copy")
    exit(2)

directory = os.getcwd() + '/oosha'

if os.path.isdir(directory):
    print("Copied HPOO succesfully to the current directory")
else:
    print("Failed to copy")
