import os
import re

# ------------ Functions ------------------
# Function what creates the .desktop for execute
def create_script(name_quick_access, arrayApps, dir_scripts):

    try:
        os.makedirs(dir_scripts, 0o500)
    except FileExistsError:
        print("The folder has already been created")

    file = open("{}/{}.sh".format(dir_scripts, name_quick_access),"w+")
    file.write("#!/bin/bash\n")

    if arrayApps[0] is not None:
        file.write("{} &\n".format(re.sub(" %[A-Za-z]","",arrayApps[0])))

    if arrayApps[1] is not None:
        file.write("{} &\n".format(re.sub(" %[A-Za-z]","",arrayApps[1])))

    if arrayApps[2] is not None:
        file.write("{} &\n".format(re.sub(" %[A-Za-z]","",arrayApps[2])))

    if arrayApps[3] is not None:
        file.write("{} &\n".format(re.sub(" %[A-Za-z]","",arrayApps[3])))

    file.close

    print('Script created')
    os.chmod("{}/{}.sh".format(dir_scripts, name_quick_access), 0o744)
    


# Function what creates the .desktop for execute
def create_quick_access(name_quick_access, dir_quick_access, dir_scripts, arrayApps):

    try:
        os.makedirs(dir_quick_access, 0o500)
    except FileExistsError:
        print("The folder has already been created")


    file = open("{}/{}.desktop".format(dir_quick_access, name_quick_access),"w+")


    file.write("""[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Exec={}/'{}.sh'
Name={}
Comment=Custom app;
""".format(dir_scripts, name_quick_access, name_quick_access))

    file.close
    print('Quick access created')
    os.chmod("{}/{}.desktop".format(dir_quick_access, name_quick_access), 0o744)
