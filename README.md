 ## **:link: SHORT'EM ALL!:link:** v0.1
 
by OSINTMATTER 
 
## Scope
*Short 'Em All!* is a Python tool that allows analysts to do lookups of URLs generated by almost every Url Shortener Service out there.
You can generate custom URLs based on your custom dictionary or input keywords, check for active links containing one or more words (with any possible permutation automatically generated), and get screenshots of the content on them.
Short' Em All!, finally, allows you to get a .txt report with active url's for single scan and related keywords.

## Prerequisites
Before you begin, ensure you have met the following requirements:

* You have installed Python (at least v. 3.8) 
* You run the tool on Linux machine

## Installing
1. Run config.py to automatically generate path variables
1. Open terminal on /shortemall/ and run: pip install -r requirements.txt
1. Go to: https://chromedriver.chromium.org/downloads, download the driver version of your locally installed chrome - browser version. 
2. Insert the chrome driver file path into the config.ini file on Drivers:" " line.
3. Go to /input folder and populate stable\_dict.txt with one word per line -- these will be the words that will be permutated and appended to the generated custom URLs
4. Go to /Short\_Em\_All, and on terminal run: python3 short\_em\_all.py

## CLI Options

usage: short_em_all.py [-h] [-t TARGET] [-s [SCREENSHOT]] [-v [VERBOSE]]

optional arguments:

  -h, --help            show this help message and exit
  
  -t TARGET, --target TARGET
                        insert target keyword
			
  -s [SCREENSHOT], --screenshot [SCREENSHOT]
                        Take screenshots on found results
			
  -v [VERBOSE], --verbose [VERBOSE]
                        turn on verbose mode

## RUN Options

If you want to execute the script without CLI options:

- python3 shortemall.py 
- 
Then, you con manually configure some scan options: 

* Dictionary options:

  [-] Yes: use the stable\_dict.txt (Short\_Em\_All\Input)
  
  [-] No: insert keyword to run a scan based on single-target
		
* Screenshot options:

  [-] Yes: URLs with HTTP Status Code = 200 are screenshotted and saved into /Screenshot
  
  [-] No: no screenshot taken during the scan process
		
* Results options:

  [-] Yes: only URLs with HTTP Status Code = 200 are printed on-screen
  
  [-] No: all results are printed on-screen

## Acknowledgements

The URL verification method implemented in *Short 'Em All!* uses https://seintpl.github.io/osint/short-links-verification-cheatsheet as its dynamic source generation.     
