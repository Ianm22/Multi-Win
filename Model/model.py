import os
from pathlib import Path
import re
import traceback
import json

# -----------------------------------------
# ------------ Functions ------------------
# -----------------------------------------
# Function what creates the .desktop for execute
def create_script(name_quick_access, selected_apps, dir_scripts):

    try:
        file = open("{}/{}.sh".format(dir_scripts, name_quick_access),"w+")
        file.write("#!/bin/bash\n")

        if selected_apps['app1'] is not None:
            file.write("{} &\n".format(re.sub(" %[A-Za-z]", "", selected_apps['app1'])))

        if selected_apps['app2'] is not None:
            file.write("{} &\n".format(re.sub(" %[A-Za-z]", "", selected_apps['app2'])))

        if selected_apps['app3'] is not None:
            file.write("{} &\n".format(re.sub(" %[A-Za-z]", "", selected_apps['app3'])))

        if selected_apps['app4'] is not None:
            file.write("{} &\n".format(re.sub(" %[A-Za-z]", "", selected_apps['app4'])))

        file.close

        print('Script created')
        os.chmod("{}/{}.sh".format(dir_scripts, name_quick_access), 0o744)
        print('Permissions 744 set in the script file\n')
        output = True
    
    except Exception as e:
        output = False
        print('Something went wrong creating the script file!\n')
        traceback.print_exc()

    return output
    

# Function what creates the .desktop for execute
def create_quick_access(name_quick_access, dir_quick_access, dir_scripts):

    try:
        file = open("{}/{}.desktop".format(dir_quick_access, name_quick_access),"w+")

        file.write(
        """[Desktop Entry]
        Encoding=UTF-8
        Version=1.0
        Type=Application
        Terminal=false
        Icon=applications-system
        Exec={}/'{}.sh'
        Name={}
        Comment=Custom app
        """.format(dir_scripts, name_quick_access, name_quick_access))

        file.close
        print('Quick access created')
        os.chmod("{}/{}.desktop".format(dir_quick_access, name_quick_access), 0o744)
        print('Permissions 744 set in the quick access file\n')
        output = True

    except Exception as e:
        output = False
        print('Something went wrong creating the quick access file!\n')
        traceback.print_exc()

    return output

# Function what adds in a .json file the name of the app and its path of the script and quick access
def addAppIntoList(dir_config, name_quick_access, dir_quick_access, dir_scripts):
    try:
        data = {}
        with open('{}/AppList.json'.format(dir_config)) as json_file:
            data = json.load(json_file)
            
        data[name_quick_access] = []
        data[name_quick_access].append({
            'dir_script': "{}/{}.sh".format(dir_scripts, name_quick_access),
            'dir_quick_access': "{}/{}.desktop".format(dir_quick_access, name_quick_access)
        })

        with open('{}/AppList.json'.format(dir_config), 'w') as outfile:
            json.dump(data, outfile)

    except Exception as e:
        print('Something went wrong!\n')
        traceback.print_exc()

# List apps
def getAppsList(dir_config):
    try:
        data = {}
        with open('{}/AppList.json'.format(dir_config)) as json_file:
            data = json.load(json_file)

        return data

    except Exception as e:
        print('Something went wrong!\n')
        traceback.print_exc()

# Function what removes from .json file the name of the app and its path of the script and quick access
# Removes the files too
def removeApp(dir_config, name_quick_access):
    try:
        data = {}
        with open('{}/AppList.json'.format(dir_config)) as json_file:
            data = json.load(json_file)
        
        for app in data[name_quick_access]:
            file_script = Path(app['dir_script'])
            file_quick_acces = Path(app['dir_quick_access'])
            file_script.unlink()
            file_quick_acces.unlink()

        data.pop(name_quick_access)
        
        with open('{}/AppList.json'.format(dir_config), 'w') as outfile:
            json.dump(data, outfile)
        
        print("Removed successfully!")

    except Exception as e:
        print('Something went wrong!\n')
        traceback.print_exc()

# Create everything you need at the beginning of the program
def startApp(dir_scripts, dir_quick_access, dir_config_apps, dir_config):
    try:
        os.makedirs(dir_config, 0o700)
    except FileExistsError:
        print("The 'multi-win' folder has already been created")

    try:
        os.makedirs(dir_scripts, 0o700)
    except FileExistsError:
        print("The 'script' folder has already been created")

    try:
        os.makedirs(dir_config_apps, 0o700)
    except FileExistsError:
        print("The 'config' folder has already been created\n")
    
    try:
        os.makedirs(dir_quick_access, 0o700)
    except FileExistsError:
        print("The 'Application' folder has already been created")

    if not os.path.isfile('{}/AppList.json'.format(dir_config_apps)):
        file = open('{}/AppList.json'.format(dir_config_apps), "w")
        file.write(r'{}')
        file.close()