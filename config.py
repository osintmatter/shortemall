#!/usr/bin/env python


import configparser
import pathlib

path = pathlib.Path(__file__).parent.resolve()
# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("path")
directory = str(path)

# ADD SETTINGS TO SECTION
config_file.set("path", "banner", directory + "/Banner/ascii.txt")
config_file.set("path", "dict", directory + "/Input/stable_dict.txt")
config_file.set("path", "i_dict", directory + "/Input/dict.txt")
config_file.set("path", "infile", directory + "/Output/infile.txt")
config_file.set("path", "outfile", directory + "/Output/outfile.txt")
config_file.set("path", "screenshot", directory + "/Screenshots/")
config_file.set("path", "home", directory)
config_file.set("path", "backup", directory + "/Backup/backup_html_table")
config_file.add_section("variables")
config_file.set("variables", "my_email", "insert the email address you utilized for the OAUTH2.0 process")
config_file.set("variables", "to_email", "insert the mail address that will receive email notifications")
config_file.set("variables", "api_key", "insert your Google API Key")


# SAVE CONFIG FILE
with open(r"config.ini", "w") as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("config.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()
