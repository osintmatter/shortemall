#!/usr/bin/env python
from __future__ import print_function
import itertools
import argparse
from socket import gaierror
import string
import progressbar
from pathlib import Path
import time
import os
import os.path
import warnings
import configparser
import pandas as pd
from datetime import datetime
import lxml.html as lh
import requests
from termcolor import colored
from requests.exceptions import Timeout
import pickle
import os
import base64
import googleapiclient.discovery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.message import EmailMessage
import json
import uuid
from tqdm import tqdm

# config parameters
now = datetime.now()
onlygreen = "zzzz"
config = configparser.ConfigParser()
config.read("config.ini")
settingscfg = config["path"]
dictionary_options = "zzzz"
screenshot_options = "zzzz"
singlescan = "zzzz"
parser = argparse.ArgumentParser(description="URL Shortener Scanner Tool")
parser.add_argument("-t", "--target", help=" insert target keyword for this scan")
parser.add_argument(
    "-d",
    "--dictionary",
    help="use stable_dictionary for this scan",
    nargs="?",
    type=int,
    const=1,
)
parser.add_argument(
    "-n",
    "--notifications",
    help="don't send email notifications on found results ",
    nargs="?",
    type=int,
    const=1,
)
parser.add_argument(
    "-z",
    "--zero",
    help="don't take screenshots on URLs landing pages",
    nargs="?",
    type=int,
    const=1,
)
parser.add_argument(
    "-f", "--found", help="show only found scan results", nargs="?", type=int, const=1
)
parser.add_argument(
    "-r",
    "--singlescan",
    help="use single scan mode (no retention)",
    nargs="?",
    type=int,
    const=1,
)
parser.add_argument(
    "-e",
    "--email",
    help="email notification on target scan",
    nargs="?",
    type=int,
    const=1,
)
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
print(colored("".join([line for line in banner]), "yellow"))

# usage recap banner
usage = """This is an URL Shortener Scanner tool for OSINT and CTI research and monitoring ... 
    usage: short_em_all.py [-h] [-t TARGET] [-d [DICTIONARY]] [-n [NOTIFICATIONS]] [-z [ZERO]] [-a [ALL]] [-r [SINGLESCAN]] [-e [EMAIL]] [-s [SCREENSHOT]] [-v [VERBOSE]]
    optional arguments: 
    -h, --help
    show this help message and exit
    - t, --target
    insert target keyword for this scan
    - d, --dictionary
    use stable_dictionary for this scan
    -n, --notifications
    don't send email notifications on found results
    -z, --zero
    don't take screenshots on URLs landing pages
    -f, --found
    show only found results
    -r, --singlescan
    use single scan mode (no retention)
    -e, --email
    receive email notification on target scan
    -s, --screenshot
    Take screenshots on found results
    -v, --verbose
    turn on verbose mode
    """

print(colored(usage, "magenta"))
# config CLI user options

if args.target is not None:
    dictionary_options = str(args.target)
    scanname = "scan name: {0}".format(dictionary_options)
    with open(config.get("path", "i_dict"), "w+") as dict:
        contents = dict.write(dictionary_options)
        dictionary_options = "null"
        print(colored("start scanning on target keyword:", "yellow"))
else:
    print(colored("UI config options:", "yellow"))
while True and args.target is None and args.dictionary is None:
    dictionary_options = input(
        colored(
            "[*] Do you want to use the dict.txt file to generate URLs? (y: Yes, n: No)",
            "cyan",
        )
    )
    dictionary_options = dictionary_options.lower()

    if dictionary_options == "y":
        dictionary_options = "yes"

        print(colored("Generating URLs based on the following inputs:", "yellow"))
        with open(config.get("path", "dict"), "r") as stable_dict:
            contents = stable_dict.read()
            print(colored(contents, "green"))
            iname = input(colored("insert scan name:", "cyan"))
            scanname = "scan name:" + str(iname)
            break
    elif dictionary_options == "n":
        dictionary_options = "null"
        with open(config.get("path", "i_dict"), "w+") as dict:
            print("Insert a keyword:")
            contents = dict.write(input())
            iname = input(colored("insert scan name:", "cyan"))
            scanname = "scan name:" + str(iname)

            break
    else:

        dictionary_options = "error"
        print(colored("error,  y: Yes, n: No", "red"))

if args.dictionary is not None:
    dictionary_options = str(args.dictionary)
    dictionary_options = "yes"
if args.zero is not None:
    screenshot_options = "n"
if args.screenshot is not None:
    screenshot_options = "y"
while True and args.screenshot is None and args.zero is None:
    screenshot_options = input(
        colored(
            "[*] Do you want to take screenshot for found URLs? (y: Yes, n: No)",
            "cyan",
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
if args.found is not None:
    onlygreen = "yes"
while True and args.verbose is None and args.found is None:
    onlygreen = input(
        colored("[*] Do you want to print only existing URLs? (y: Yes, n: No)", "cyan")
    )
    onlygreen = onlygreen.lower()
    if onlygreen == "n":
        onlygreen = "null"
        break
    elif onlygreen == "y":
        onlygreen = "yes"
        break
    else:
        onlygreen = "error"
        break
        print(colored("error,  y: Yes, n: No", "red"))
if args.email is not None:
    send_mail = "yes"
if args.notifications is not None:
    send_mail = "null"
while True and args.email is None and args.notifications is None:
    send_mail = input(
        colored(
            "[*] Do you want to receive email notification on target scan results? (y: Yes, n: No)",
            "cyan",
        )
    )
    send_mail = send_mail.lower()
    if send_mail == "n":
        send_mail = "null"
        break
    elif send_mail == "y":
        send_mail = "yes"
        print(colored("email notification activated on target scan!", "yellow"))
        break
    else:
        send_mail = "error"
        break
        print(colored("error,  y: Yes, n: No", config.get("path", "outfile2"), "red"))

if args.singlescan is not None:
    singlescan = "yes"

while True and args.singlescan is None:
    singlescan = input(
        colored(
            "[*] Do you want to use single scan mode with no data retention? (y: Yes, n: No)",
            "cyan",
        )
    )
    singlescan = singlescan.lower()
    if singlescan == "n":
        singlescan = "null"
        break
    elif singlescan == "y":
        singlescan = "yes"
        print(colored("single-scan mode tuned on", "yellow"))
        break
    else:
        singlescan = "error"
        print(colored("error,  y: Yes, n: No", "red"))
        break


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

    url = "https://seintpl.github.io/osint/short-links-verification-cheatsheet"  # Create a handle, page, to handle the contents of the website

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

    df1 = df["Service"].str.strip("\n").str.strip(" ")
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
            try:

                response = requests.get(url, timeout=7)

                if response.status_code == 200:
                    stamp = url
                    match = "+++" + " " + "Found result:" + stamp
                    # res = str(seen).replace("'", "")[1:-1]
                    print(colored(match, "green"))
                    seen = set()

                    seen.add(stamp)

                    with open(config.get("path", "infile"), "a+") as infile:

                        infile.seek(0)
                        lines_i = infile.read().splitlines()

                        if stamp not in lines_i:

                            if singlescan != "yes":

                                infile.write(stamp)
                                infile.write("\n")

                                with open(
                                    config.get("path", "outfile"), "a+"
                                ) as outfile:

                                    outfile.write(stamp)
                                    outfile.write("\n")

                            else:

                                with open(
                                    config.get("path", "outfile"), "a+"
                                ) as outfile:

                                    outfile.write(stamp)
                                    outfile.write("\n")

                else:
                    if onlygreen == "null":
                        print(colored("---" + url + " " + "Not found", "red"))
            except Timeout:
                if onlygreen == "null":
                    print(colored("***" + url + " " + "The request timed out", "cyan"))
            except gaierror:
                print("oops")
            except requests.exceptions.ConnectionError as e:
                if onlygreen == "null":
                    print(colored("***" + url + " " + "No response", "blue"))


# take screenshots of outfile.txt
if screenshot_options == "y":
    path = config.get("path", "outfile")
    check = os.path.isfile(path)
    if check == True:
        with open(config.get("path", "outfile"), "r") as outfile:
            message = "Taking awesome screenshots for you ..."
            animated_marker()
            print(colored(message, "yellow"))
            os.chdir(config.get("path", "screenshot"))
            scna_dir = str(scanname) + str(uuid.uuid1())
            os.mkdir(scna_dir)
            os.chdir(f"{scna_dir}")
            lines_out = []
            for line in outfile:
                lines_out.append(line.strip())

            for element in tqdm(lines_out, colour="green"):

                try:
                    yoururl = element  # [:-1]
                    url = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run"

                    screen_name = f'{scanname}{datetime.now().strftime("%H:%M:%S")}.png'

                    # Set the headers
                    api_key = config.get("variables", "api_key")
                    params = {
                        "url": yoururl,
                        "requestScreenshot": "true",
                        "key": api_key,
                    }
                    x = requests.post(url, data=params)
                    data = json.loads(x.text)

                    with open(screen_name, "wb") as fh:

                        fh.write(base64.b64decode(data["screenshot"]["data"]))

                        print(
                            "Screenshot from "
                            + str(params["url"])
                            + " is taken and downloaded."
                        )

                except:
                    print(
                        "Problem with "
                        + str(params["url"])
                        + ". "
                        + str(x)[len(str(x)) - 5 : len(str(x)) - 2]
                        + " Response Code."
                    )
                    os.chdir(config.get("path", "home"))

    os.chdir(config.get("path", "home"))

# download last available version of url HTML to ensure continuity
new_backup = open(config.get("path", "backup"), "wb").write(page.content)

# notify if new result found

if send_mail == "yes":

    out_file = Path(config.get("path", "outfile"))
    if out_file.is_file():

        msg = EmailMessage()
        # Get the path to the pickle file
        home_dir = config.get("path", "home")
        pickle_path = os.path.join(home_dir, "gmail.pickle")

        # Load our pickled credentials
        creds = pickle.load(open(pickle_path, "rb"))

        # Build the service
        service = googleapiclient.discovery.build("gmail", "v1", credentials=creds)
        message = EmailMessage()
        my_email = config.get("variables", "my_email")
        to_email = config.get("variables", "to_email")
        msg = MIMEMultipart("alternative")
        message["Subject"] = "Short_em_all notifications- Scan" + f"{scanname}"
        message["From"] = f"{my_email}"
        message["To"] = f"{to_email}"
        messageHtml = "<b>New Short Urls found on target, see attached file!</b>"
        file_path = config.get("path", "outfile")
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type, mime_subtype = mime_type.split("/")
        with open(file_path, "rb") as file:
            message.add_attachment(
                file.read(),
                maintype=mime_type,
                subtype=mime_subtype,
                filename="outfile.txt",
            )
        message.attach(MIMEText(messageHtml, "html"))
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        body = {"raw": raw}
        message1 = body
        # service.send(my_email, to_email, text)
        message = service.users().messages().send(userId="me", body=message1).execute()

        print("E-mail Notification Sent")
        os.remove(config.get("path", "outfile"))

    else:
        print(colored("0 new URLs found from last scan! No e-mail sent...", "red"))

print(colored("Congrats! Short em All has successfully terminated the scan", "yellow"))
input(colored("Press Enter key to end...", "blue"))
