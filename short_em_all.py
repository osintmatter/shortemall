#!/usr/bin/env python
import argparse
import base64
import binascii
import configparser
import googleapiclient
import itertools
import json
import mimetypes
import os
import pandas as pd
import pathlib
import pickle
import progressbar
import requests
import shutil
import string
import time
import urllib.parse
import uuid
import textwrap
from datetime import datetime
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from termcolor import colored
from tqdm import tqdm
import validators
from urllib.parse import urlparse
from requests.exceptions import Timeout
import warnings
import lxml.html as lh
from googleapiclient.discovery import build


# ASCII Art Banner
def banner():
    print(""" 
   _____ _                _     _ ______                      _ _   _ 
  / ____| |              | |   ( )  ____|               /\   | | | | |
 | (___ | |__   ___  _ __| |_  |/| |__   _ __ ___      /  \  | | | | |
  \___ \| '_ \ / _ \| '__| __|   |  __| | '_ ` _ \    / /\ \ | | | | |
  ____) | | | | (_) | |  | |_    | |____| | | | | |  / ____ \| | | |_|
 |_____/|_| |_|\___/|_|   \__|   |______|_| |_| |_| /_/    \_\_|_| (_)
                                                                    
  by  OSINTMATTER                                                      
                                                                     v3.0_2024        
 

Designed by  OSINTMATTER """)



# Function to handle input

def get_input(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ['y', 'n']:
            return choice
        else:
            print("Invalid input. Please enter 'y' for Yes or 'n' for No.")

# Check if the 'config.ini' file exists in the current directory
if not os.path.isfile('config.ini'):
    print("'config.ini' file not found!")
    os.system('python config.py')

screenshot_options = ''  # Setting screenshot_options to 'error' outside the loop

if not os.path.isfile('gmail.pickle'):
    exclude_gmail = get_input("'gmail.pickle' file not found. Do you want to exclude this configuration? (y/n): ")
    if exclude_gmail == 'y':
        print("Excluding 'gmail.pickle' configuration...")
        screenshot_options = 'error'  # Set screenshot_options to 'error' if exclude_gmail is 'y'
    elif exclude_gmail == 'n':
        print("Obtain the OAuth 2.0 client ID for your Gmail account and save the generated credentials file as credentials.json in the main folder - follow this step-by-step guide: https://support.google.com/cloud/answer/6158849?hl=en#zippy=")
        os.system('python gmailconfig.py')

# If both files exist, proceed with the script
if os.path.isfile('config.ini') and os.path.isfile('gmail.pickle'):
    pass
# Insert the rest of the script code here
else:
    print("Error: Configuration files not found. Exiting...")

# Config Parameters
now = datetime.now()
onlygreen = "zzzz"
config = configparser.ConfigParser()
config.read("config.ini")
settingscfg = config["path"]
dictionary_options = "zzzz"
singlescan = "zzzz"
outfile_path = config.get("path", "outfile")
tempfile_path = config.get("path", "tempfile")
api_key = config.get("variables", "api_key")
seen_urls = set()

# Initialize ArgumentParser
parser = argparse.ArgumentParser(description="URL Shortener Scanner Tool")
parser.add_argument(
    "-t", "--target", help="Insert target keyword for this scan", action="store_true"
)

parser.add_argument(
    "-d",
    "--dictionary",
    help="Use stable_dictionary for this scan",
    action="store_true",
)
parser.add_argument(
    "-v", "--verbose", help="Turn on verbose mode", action="store_true"
)
parser.add_argument(
    "-n",
    "--notifications",
    help="Don't send email notifications on found results",
    action="store_true",
)
parser.add_argument(
    "-z",
    "--zero",
    help="Don't take screenshots on URLs landing pages",
    action="store_true",
)
parser.add_argument(
    "-f",
    "--found",
    help="Show only found scan results",
    action="store_true",
)
parser.add_argument(
    "-r",
    "--singlescan",
    help="Use single scan mode (no retention)",
    action="store_true",
)
parser.add_argument(
    "-e",
    "--email",
    help="Email notification on target scan",
    action="store_true",
)
parser.add_argument(
    "-s",
    "--screenshot",
    help="Take screenshots on found results",
    action="store_true",
)
args = parser.parse_args()

# Set default values
dictionary_options = onlygreen = send_mail = singlescan = "null"

# Check if args.target is provided
if args.target:
    dictionary_options = str(args.target)
    scanname = f"Scan Name: {dictionary_options}"
    with open(config.get("path", "i_dict"), "w+") as dict_file:
        dict_file.write(dictionary_options)
    print(colored("Start scanning on target keyword:", "yellow"))
else:
    print(colored("UI config options:", "yellow"))

banner()
# Ask the user if they want to use the dict.txt file to generate URLs
if not args.target and not args.dictionary:
    while True:
        dictionary_options = input(
            colored(
                "[*] Do you want to use the dict.txt file to generate URLs? (y: Yes, n: No)",
                "cyan",
            )
        ).lower()

        if dictionary_options in {"y", "n"}:
            dictionary_options = "yes" if dictionary_options == "y" else "null"
            if dictionary_options == "yes":
                print(colored("Generating URLs based on the following inputs:", "yellow"))
                with open(config.get("path", "dict"), "r") as stable_dict:
                    contents = stable_dict.read()
                    print(colored(contents, "green"))
                    iname = input(colored("Insert scan name:", "cyan"))
                    scanname = f"{iname}"
            else:
                with open(config.get("path", "i_dict"), "w+") as dict_file:
                    print("Insert a keyword:")
                    contents = dict_file.write(input())
                    iname = input(colored("Insert scan name:", "cyan"))
                    scanname = f"{iname}"
            break
        else:
            print(colored("Error, y: Yes, n: No", "red"))

# Set dictionary_options based on args.dictionary
if args.dictionary:
    dictionary_options = str(args.dictionary)
    dictionary_options = "yes"

# Set screenshot_options based on args.screenshot
if args.zero:
    screenshot_options = "n"
if args.screenshot:
    screenshot_options = "y"

# Ask the user if they want to take screenshots for found URLs
if not args.screenshot and not args.zero and screenshot_options != 'error':
    while True:
        screenshot_options = input(
            colored(
                "[*] Do you want to take screenshot of found URLs? (y: Yes, n: No)",
                "cyan",
            )
        ).lower()

        if screenshot_options in {"y", "n"}:
            screenshot_options = "y" if screenshot_options == "y" else "n"
            break
        else:
            print(colored("Error, y: Yes, n: No", "red"))


# Set onlygreen based on args.verbose and args.found
if args.verbose:
    onlygreen = "null"
if args.found:
    onlygreen = "yes"

# Ask the user if they want to print only existing URLs
if not args.verbose and not args.found:
    while True:
        onlygreen = input(
            colored(
                "[*] Do you want to print only existing URLs? (y: Yes, n: No)",
                "cyan",
            )
        ).lower()

        if onlygreen in {"y", "n"}:
            onlygreen = "null" if onlygreen == "n" else "yes"
            break
        else:
            print(colored("Error, y: Yes, n: No", "red"))


# Set singlescan based on args.singlescan
if args.singlescan:
    singlescan = "yes"

# Ask the user if they want to use single scan mode with no data retention
if not args.singlescan:
    while True:
        singlescan = input(
            colored(
                "[*] Do you want to save the scan results ? (y: Yes, n: No)",
                "cyan",
            )
        ).lower()

        if singlescan in {"y", "n"}:
            singlescan = "null" if singlescan == "y" else "yes"
            if singlescan == "null":
                print(colored("Single-scan mode turned on", "yellow"))
            break
        else:
            print(colored("Error, y: Yes, n: No", "red"))
# Set send_mail based on args.email and args.notifications
if args.email:
    send_mail = "yes"
elif args.notifications:
    send_mail = "null"
else:
    send_mail = None

# Ask the user if they want to receive email notification on target scan results
if send_mail is None:
    while True:
        send_mail_input = input(
            colored(
                "[*] Do you want to receive email notification on target scan results? (y: Yes, n: No)",
                "cyan",
            )
        ).lower()

        if send_mail_input in {"y", "n"}:
            send_mail = "yes" if send_mail_input == "y" else "null"
            if send_mail == "yes":
                print(colored("Email notification activated on target scan!", "yellow"))
            break
        else:
            print(colored("Error, y: Yes, n: No", "red"))

# Ask the user if they want to filter the results for Bit.ly
is_bitly_url_input = input("Do you want to filter the results for Bit.ly URLs? (y/n): ").lower()

# Validate the user's input
while is_bitly_url_input not in {'y', 'n'}:
    print("Invalid input. Please enter 'y' for yes or 'n' for no.")
    is_bitly_url_input = input("Do you want to filter the results for Bitly? (y/n): ").lower()

# Set the is_bitly_url variable based on the user's input
is_bitly_url = True if is_bitly_url_input == 'y' else False

# Animations
def animated_marker():
    widgets = ["Loading: ", progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()

    for i in range(100):
        time.sleep(0.1)
        bar.update(i)

# Definition of permutation logic
def find_occurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def calculate_combinations(tokens):
    domain_ilty = []
    for i in range(1, len(tokens) + 1):
        for p in itertools.permutations(tokens, i):
            ps = "".join(p)
            domain_ilty.append(ps)
    return domain_ilty


def capture_screenshot(url, output_filename):
    
    try:
        # ChromeDriver config
        
        path = Path(__file__).parent.resolve()
        chromedriver_path = str(path / "Input/chromedriver")
        options = Options()
        options.add_argument('--headless')

        # ChromeDriver Init
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

        # load URL
        if validators.url(url):
    
            driver.get(url)

            # Sync
            driver.implicitly_wait(5)

            # Take Screenshot and save it 
            driver.save_screenshot(output_filename)
            print(f"Screenshot di {url} salvato come {output_filename}")

            # Close Chromedriver
            driver.quit()
        else:
            print(f"Invalid URL: {url}")

    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")

# Process URLs
def process_url(url):
    try:
            response = requests.get(url, timeout=7)
            if response.status_code == 200:
                stamp = url
                match = "+++" + " " + "Found result:" + stamp
                print(colored(match, "green"))
                seen = set()
                seen.add(stamp)

                with open(config.get("path", "infile"), "a+") as infile:
                    infile.seek(0)
                    lines_i = infile.read().splitlines()

                    if stamp not in lines_i:
                        if singlescan == "null":
                            infile.write(stamp)
                            infile.write("\n")

                            with open(config.get("path", "outfile"), "a+") as outfile:
                                outfile.write(stamp)
                                outfile.write("\n")
                        else:
                            with open(config.get("path", "tempfile"), "a+") as tempfile:
                                tempfile.write(stamp)
                                tempfile.write("\n")
            else:
                if onlygreen == "null":
                    print(colored("---" + url + " " + "Not found", "red"))
    except Timeout:
            if onlygreen == "null":
                print(colored("***" + url + " " + "The request timed out", "cyan"))
    except requests.exceptions.ConnectionError as e:
            if onlygreen == "null":
                print(colored("***" + url + " " + "No response", "blue"))


if __name__ == "__main__":

    

    if args.help:
        print("""
        Short Url Scanning Tool trusted by CTI Analysts and Security Researchers

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
        """)
        exit()
    # Driver's code
    animated_marker()
    warnings.filterwarnings("ignore")

    # Define valid characters for URLs
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # URL to scrape data from
    url = "https://seintpl.github.io/osint/short-links-verification-cheatsheet"

    # Fetching the page content
    page = requests.get(url)
    if page.status_code != 200:
        print(colored("Switching to local HTML version ...", "red"))
        with open(config.get("path", "backup"), "r") as f:
            rules_page = f.read()
        rules_page = lh.fromstring(rules_page)
    else:
        doc = lh.fromstring(page.content)
        rules_page = doc

    # Parsing data from HTML
    tr_elements = doc.xpath("//tr")
    col = [(t.text_content(), []) for t in tr_elements[0]]

    for j in range(1, len(tr_elements)):
        T = tr_elements[j]
        if len(T) != 3:
            break
        for i, t in enumerate(T.iterchildren()):
            data = t.text_content() if i > 0 else t.text_content()
            col[i][1].append(data)

    Dict = {title: column for title, column in col}
    df = pd.DataFrame(Dict)
    del df["Example"]

    df1 = df["Service"].str.strip("\n").str.strip(" ")
    df2 = df["Verification method"].str.extract("([+-@=!])")

    df1_l = df1.values.tolist()
    df2_l = df2.values.tolist()
# Load domains from specified dictionary or default one
if dictionary_options == "null":
    with open(config.get("path", "i_dict"), "r") as f:
        myDomains = [line.strip() for line in f]
else:
    with open(config.get("path", "dict"), "r") as f:
        myDomains = [line.strip() for line in f]
# Calculate combinations of domains
myUrls = calculate_combinations(myDomains)
x = time.strftime("%Y%m%d-%H%M%S")
# Lista per tenere traccia degli URL già trovati
seen_urls = set()

# Iterate over myUrls and construct URLs
for items in myUrls:
    for i in range(0, len(df1_l)):
        df3 = (
            "https://"
            + ""
            + str(df1_l[i])
            + ""
            + "/"
            + items
            + str(df2_l[i]).strip("[]'\"nan")
        )
        url = df3
        parsed_url = urlparse(df3)
        domain = parsed_url.netloc

        try:
            # Check if the URL should be filtered for bit.ly URLs
            if is_bitly_url and "bit.ly" not in domain:
                continue  # Skip this iteration if it's not a bit.ly URL
            response = requests.get(url, timeout=7)
            if response.status_code == 200:
                stamp = url
                if stamp not in seen_urls:  # Check if URL is new
                    match = "+++" + " " + "Found result:" + stamp
                    print(colored(match, "green"))
                    seen_urls.add(stamp)  # Add the URL to the seen URLs list

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

                    # Take screenshots if enabled
                    if screenshot_options == "y":
                        yoururl = url.rstrip()
                        screen_name = f'{scanname}{datetime.now().strftime("%H%M%S")}.png'
                        response = capture_screenshot(yoururl, screen_name)

                        if response:
                            try:
                                response.raise_for_status()
                                data = response.json()["screenshot"]["data"]

                                if len(data) % 4 == 1:
                                    data += "=" * (4 - len(data) % 4)

                                decoded_data = base64.b64decode(data)

                                with open(screenshot_path, "wb") as fh:
                                    fh.write(decoded_data)

                                print(f"Screenshot from {yoururl} taken and downloaded.")
                            except binascii.Error as e:
                                print("Error decoding screenshot data.")

                else:
                    continue

            else:
                if onlygreen == "null":
                    print(colored("---" + url + " " + "Not found", "red"))


        except Timeout:
            if onlygreen == "null":
                print(colored("***" + url + " " + "The request timed out", "cyan"))
        except requests.exceptions.ConnectionError as e:
            if onlygreen == "null":
                print(colored("***" + url + " " + "No response", "blue"))
# Get file paths from config
tempfile_path = config.get("path", "tempfile")
outfile_path = config.get("path", "outfile")

# Check if outfile.txt exists
if os.path.isfile(outfile_path):
    try:
        # Load pickled credentials
        pickle_path = os.path.join(config.get("path", "home"), "gmail.pickle")
        with open(pickle_path, "rb") as file:
            creds = pickle.load(file)

        # Build the Gmail service
        service = googleapiclient.discovery.build("gmail", "v1", credentials=creds)

        # Prepare email message
        message = MIMEMultipart("alternative")
        my_email = config.get("variables", "my_email")
        to_email = config.get("variables", "to_email")
        message["Subject"] = f"Short_em_all notifications - Scan {scanname}"
        message["From"] = my_email
        message["To"] = to_email
        message_html = "<b>New Short URLs found on target, see attached file!</b>"

        # Add attachment
        with open(outfile_path, "rb") as file:
            mime_type, _ = mimetypes.guess_type(outfile_path)
            mime_type, mime_subtype = mime_type.split("/")
            attachment = MIMEBase(mime_type, mime_subtype)
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(outfile_path)}",
            )
            message.attach(attachment)

        message.attach(MIMEText(message_html, "html"))
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {"raw": raw_message}

        # Send email
        try:
            message = service.users().messages().send(userId="me", body=message_body).execute()
            print("Email notification sent successfully.")
        except Exception as e:
            print("Error sending email notification:", e)
    except Exception as e:
        print("Error processing email notification:", e)
else:
    print(colored("0 new URLs found from last scan! No e-mail sent...", "red"))

# Move screenshots to the dedicated folder
screenshots_dir = os.path.join(os.getcwd(), "Screenshots", scanname)
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png"):
        shutil.move(filename, os.path.join(screenshots_dir, filename))

# Rename and copy infile.txt and outfile.txt
try:
    if os.path.isfile(outfile_path):
        shutil.copy(outfile_path, os.path.join("Output", f"{scanname}_results.txt"))
    if os.path.isfile(tempfile_path):
        shutil.copy(tempfile_path, os.path.join("tempfile", "permanent_URLs_Collection.txt"))
    print("Find the scan report on the /Output folder")
except Exception as e:
    print("Error copying and renaming files:", e)

print(colored("Congrats! Short em All has successfully terminated the scan", "yellow"))
input(colored("Press Enter key to end...", "blue"))
