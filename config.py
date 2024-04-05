#!/usr/bin/env python

import configparser
import pathlib

# Ottieni il percorso del file corrente
path = pathlib.Path(__file__).parent.resolve()

# CREA L'OGGETTO
config_file = configparser.ConfigParser()

# AGGIUNGI LA SEZIONE
config_file.add_section("path")

# AGGIUNGI LE IMPOSTAZIONI ALLA SEZIONE
config_file.set("path", "banner", str(path / "Banner/ascii.txt"))
config_file.set("path", "dict", str(path / "Input/stable_dict.txt"))
config_file.set("path", "i_dict", str(path / "Input/dict.txt"))
config_file.set("path", "infile", str(path / "Output/infile.txt"))
config_file.set("path", "outfile", str(path / "Output/outfile.txt"))
config_file.set("path", "tempfile", str(path / "Output/tempfile.txt"))
config_file.set("path", "screenshot", str(path / "Screenshots/"))
config_file.set("path", "home", str(path))
config_file.set("path", "backup", str(path / "Backup/backup_html_table"))

# AGGIUNGI LA SEZIONE DELLE VARIABILI
config_file.add_section("variables")
config_file.set("variables", "my_email", "notifications.shortemall@gmail.com")
config_file.set("variables", "to_email", "notifications.shortemall@gmail.com")
config_file.set("variables", "api_key", "AIzaSyDGkfQWPy4qFvcSuDxSe9EzSj50zJQs_ik")

# SALVA IL FILE DI CONFIGURAZIONE
config_filename = "config.ini"
with open(config_filename, "w") as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()

print(f"Config file '{config_filename}' created")

# STAMPA IL CONTENUTO DEL FILE
with open(config_filename, "r") as read_file:
    content = read_file.read()
    print(f"\nContent of the config file '{config_filename}' are:\n")
    print(content)
