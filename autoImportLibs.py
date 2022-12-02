import subprocess
import re
import os
import time

#Libraries to import
#   - selenium
#   - webdriver_manager
#   - bs4
#   - pandas
#   - mysql-connector-python
#   - pillow
#   - lxml
#   - customtkinter
#   - requests


def installLibs(venv=False):
    if venv == True:
        try:
            if os.path.exists('test_env'):
                subprocess.run('pip install -r requiredLibs.txt', shell=True, stdout=subprocess.PIPE)
            else:
                raise BaseException('The virtual environment does not yet exist in your directory')
        except Exception as e:
            print('Error: %s' % e)
    else:
        try:
            subprocess.run('py -m venv test_env', shell=True, stdout=subprocess.PIPE)
            print('type this into the command line')
            print('     |          |          |   ')
            print('     v          v          v   ')
            print('test_env\\Scripts\\activate.bat \n')
            print('If you see something like (test_env) C:\\path\\to\\current\\directory> then you are currently in the virtual environment')
        except:
            print('Error while creating virtual environment')
            
if __name__ == '__main__':
    print('Do you have a virtual environment set up? \n1 = Yes \t 2 = No')
    inp = input()
    createEnv = False
    if inp == '1':
        createEnv = True
    installLibs(createEnv)
    

