#!/usr/bin/env python

import itertools
import argparse
from socket import gaierror
import string
import progressbar
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import shutil
import warnings
import configparser
import pandas as pd
import lxml.html as lh
import requests
from termcolor import colored
from requests.exceptions import Timeout


# config parameters

onlygreen = "zzz"
config = configparser.ConfigParser()
config.read("config.ini")
settingscfg = config["path"]
dictionary_options = "zzzz"
screenshot_options = "zzzz"
parser = argparse.ArgumentParser(description="URL Shortener Scanner Tool")
parser.add_argument("-t", "--target", help=" insert target keyword")
parser.add_argument(
    "-s",
    "--screenshot",
    help="Take screenshots on found results",
    nargs="?",
    type=int,
    const=1,
)
parser.add_argument(
    "-v", "--verbose", help="turn on verbose mode", nargs="?", type=int, const=1
)


args = parser.parse_args()

# banner
banner = open(config.get("path", "banner"), "r")
print("".join([line for line in banner]))
# config CLI user options

if args.target is not None:
    dictionary_options = str(args.target)
    with open(config.get("path", "i_dict"), "w+") as dict:
        contents = dict.write(dictionary_options)
        dictionary_options = "null"
        print(colored("start scanning on target keyword:", "yellow"))
else:
    print(colored("Config options:", "yellow"))
while True and args.target is None:
    dictionary_options = input(
        colored(
            "[*] Do you want to use the dict.txt file to generate URLs? (y: Yes, n: No)",
            "green",
        )
    )
    dictionary_options = dictionary_options.lower()
    if dictionary_options == "y":
        dictionary_options = "yes"
        print(colored("Generating URLs based on the following inputs:", "yellow"))
        with open(config.get("path", "dict"), "r") as stable_dict:
            contents = stable_dict.read()
            print(colored(contents, "green"))
            break
    elif dictionary_options == "n":
        dictionary_options = "null"
        with open(config.get("path", "i_dict"), "w+") as dict:
            print("Insert a keyword:")
            contents = dict.write(input())
            break
    else:

        dictionary_options = "error"
        print(colored("error,  y: Yes, n: No", "red"))

if args.screenshot is not None:
    screenshot_options = "y"
while True and args.screenshot is None:
    screenshot_options = input(
        colored(
            "[*] Do you want to take screenshot for found URLs? (y: Yes, n: No)",
            "green",
        )
    )
    screenshot_options = screenshot_options.lower()

    if screenshot_options == "y":
        screenshot_options = "y"
        break
    elif screenshot_options == "n":
        screenshot_options = "n"
        break
    else:
        screenshot_options = "error"
        print(colored("error,  y: Yes, n: No", "red"))

if args.verbose is not None:
    onlygreen = "null"
while True and args.verbose is None:
        onlygreen = input(
            colored(
                "[*] Do you want to print only existing URLs? (y: Yes, n: No)", "green"
            )
        )
        onlygreen = onlygreen.lower()
        if onlygreen == "n":
            onlygreen = "null"
            print(colored("Start scanning URL Shorteners:", "red"))
            break
        elif onlygreen == "y":
            onlygreen = "yes"
            print(colored("Start scanning URL Shorteners:", "red"))
            break
        else:
            onlygreen = "error"
            break
            print(colored("error,  y: Yes, n: No", "red"))

# Animations
def animated_marker():

    widgets = ["Loading: ", progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()

    for i in range(100):
        time.sleep(0.1)
        bar.update(i)


# def permutations
def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def calculateCombinations(tokens):
    domain_ilty = []
    for i in range(1, len(tokens) + 1):
        for p in itertools.permutations(tokens, i):
            ps = str(p)
            ps = ps.replace("(", "")
            ps = ps.replace(")", "")
            ps = ps.replace("'", "")
            ps = ps.replace(" ", "")
            ps = ps.replace(",", "")
            domain_ilty.append(str(ps))
    return domain_ilty


# main

if __name__ == "__main__":

    # Driver's code
    animated_marker()
    warnings.filterwarnings("ignore")
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    url = (
        "https://seintpl.github.io/osint/short-links-verification-cheatsheet"
    )  # Create a handle, page, to handle the contents of the website
    page = requests.get(url)  # Store the contents of the website under doc
    if page.status_code != 200:
        print(colored("switching to local html version ...", "red"))
        with open(config.get("path", "backup"), "r") as f:

            rules_page = f.read()
        rules_page = lh.fromstring(rules_page)
    else:
        doc = lh.fromstring(
            page.content
        )  # Parse data that are stored between <tr>..</tr> of HTML
        rules_page = doc

    # Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath("//tr")
    col = []
    i = 0  # For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        col.append((name, []))

    # Since out first row is the header, data is stored on the second row onwards
    for j in range(1, len(tr_elements)):
        # T is our j'th row
        T = tr_elements[j]

        # If row is not of size 10, the //tr data is not from our table
        if len(T) != 3:
            break

        # i is the index of our column
        i = 0

        # Iterate through each element of the row
        for t in T.iterchildren():
            data = t.text_content()
            # Check if row is empty
            if i > 0:
                # Convert any numerical value to integers
                try:
                    data = int(data)
                except:
                    pass
            # Append the data to the empty list of the i'th column
            col[i][1].append(data)
            # Increment i for the next column
            i += 1

    # print([len(C) for (title,C) in col])

    Dict = {title: column for (title, column) in col}
    # Create Dataframe
    df = pd.DataFrame(Dict)
    del df["Example"]

    df1 = df["Service"].str.strip("\n" "(deprecated)").str.replace(" ", "")
    df2 = df["Verification method"].str.extract("([+-@=!])")

    df1_l = df1.values.tolist()
    df2_l = df2.values.tolist()
    # generate urls
    if dictionary_options == "null":
        with open(config.get("path", "i_dict"), "r") as f:
            myDomains = [line.strip() for line in f]

    else:
        with open(config.get("path", "dict"), "r") as f:
            myDomains = [line.strip() for line in f]

    myUrls = calculateCombinations(myDomains)
    x = time.strftime("%Y%m%d-%H%M%S")
    seen = set()
    res = str(seen).replace("'", "")[1:-1]

    # find out active urls and write outfile.txt
    for items in myUrls:
        for i in range(0, len(df1_l)):
            df3 = (
                "https://"
                + ""
                + str(df1_l[i])
                + ""
                + "/"
                + items
                + str(df2_l[i]).strip("[" "]" "'" "nan")
            )
            url = df3
            stamp = url
            try:

                response = requests.get(url, timeout=7)

                if response.status_code == 200:
                    match = "+++" + " " + "Found result:" + stamp
                    print(colored(match, "green"))
                    seen.add(stamp)

                    with open(config.get("path", "infile"), "a+") as infile:
                        infile.write(stamp)
                        infile.write("\n")
                    with open(config.get("path", "outfile"), "w+") as outfile:
                        for stamp in seen:
                            if stamp not in outfile:
                                outfile.write(stamp)
                                outfile.write("\n")
                                seen.add(stamp)
                else:
                    if onlygreen == "null":
                        print(colored("---" + url + " " + "Not found", "red"))
            except Timeout:
                if onlygreen == "null":
                    print(colored("***" + url + " " + "The request timed out", "blue"))
            except gaierror:
                print("oops")
            except requests.exceptions.ConnectionError as e:
                if onlygreen == "null":
                    print(colored("***" + url + " " + "No response", "blue"))
# count newly found results
with open(config.get("path", "outfile"), "r") as fp:
    for count, line in enumerate(fp):
        # pass
        closing = (count + 1, "new results found and reported into out.txt file!")

# take screenshots of outfile.txt
if screenshot_options == "y":
    with open(config.get("path", "outfile"), "r") as outfile:
        n = 0
        message = "Taking awesome screenshots for you ..."
        animated_marker()
        print(colored(message, "yellow"))
        for i in outfile:

            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--headless")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            s = Service("/media/sf_Check_Phone/Short_Em_All/Drivers/chromedriver")
            driver = webdriver.Chrome(
                service=s,
                options=options,
                service_args=["--verbose", "--log-path=/tmp/chromedriver.log"],
            )
            driver.get(i)
            S = lambda X: driver.execute_script(
                "return document.body.parentNode.scroll" + X
            )
            driver.set_window_size(S("Width"), S("Height"))
            screen_name = "".join(c for c in str(i).strip("https") if c in valid_chars)
            driver.find_element_by_tag_name("body").screenshot(
                str(n) + "_" + str(screen_name) + "_.png"
            )
            driver.minimize_window()
            n = n + 1

    # move screenshot to proper folder
main_dir = config.get("path", "screenshot") + str(x)
os.mkdir(main_dir)
old_directory = config.get("path", "home")
new_directory = main_dir
for filename in os.listdir(old_directory):
    if filename.endswith(".png"):
        source = os.path.join(old_directory, filename)
        destination = os.path.join(new_directory, filename)
        dest = shutil.move(source, destination)


new_backup = open(config.get("path", "backup"), "wb").write(
    page.content
)  # download last available version of url HTML to ensure continuity

print(colored("See taken Screenshots on /Screenshots Folder", "yellow"))

with open(config.get("path", "outfile")) as f:

    closing = sum(1 for _ in f), "new results found!"
print(colored(closing, "yellow"))
input(colored("Press any key to end...", "yellow"))
