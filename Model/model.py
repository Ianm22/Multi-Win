import os
import re
import traceback

# ------------ Functions ------------------
# Function what creates the .desktop for execute
def create_script(name_quick_access, selected_apps, dir_scripts):

    try:
        try:
            os.makedirs(dir_scripts, 0o700)
        except FileExistsError:
            print("The folder has already been created")

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
        output = True
    
    except Exception as e:
        output = False
        traceback.print_tb(e)

    return output
    


# Function what creates the .desktop for execute
def create_quick_access(name_quick_access, dir_quick_access, dir_scripts):

    try:
        try:
            os.makedirs(dir_quick_access, 0o700)
        except FileExistsError:
            print("The folder has already been created")


        file = open("{}/{}.desktop".format(dir_quick_access, name_quick_access),"w+")


        file.write(
        """[Desktop Entry]
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
        
        output = True

    except Exception as e:
        output = False
        traceback.print_tb(e)

    return output
