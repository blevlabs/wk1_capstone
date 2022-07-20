# sync with github
import os
name = input("Enter push name:")
# make sure you switch your git to the proper branch 'compcore'
os.system("git add . && git commit -m \"" + name + "\" && git push")