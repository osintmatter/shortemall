```
   _____ _                _     _ ______                      _ _   _ 
  / ____| |              | |   ( )  ____|               /\   | | | | |
 | (___ | |__   ___  _ __| |_  |/| |__   _ __ ___      /  \  | | | | |
  \___ \| '_ \ / _ \| '__| __|   |  __| | '_ ` _ \    / /\ \ | | | | |
  ____) | | | | (_) | |  | |_    | |____| | | | | |  / ____ \| | | |_|
 |_____/|_| |_|\___/|_|   \__|   |______|_| |_| |_| /_/    \_\_|_| (_)
                                                                    
  by  OSINTMATTER                                                      
                                                                     v1.0
```
## Scope
*Short 'Em All!* is a Python tool that allows analysts to do lookups of URLs generated by almost every Url Shortener Service out there.
You can generate custom URLs based on your custom dictionary or input keywords, check for active links containing one or more words (with any possible permutation automatically generated), and get screenshots of the content on them.
Short' Em All!, finally, allows you to get a .txt report with active url's for single scan and related keywords.

## Prerequisites
Before you begin, ensure you have met the following requirements:

* You have installed Python - pip (at least v. 3.8) 
* You run the tool on Linux machine
* Google Chrome installed (only for screenshots feature)

## Installing
1. Run config.py to automatically generate path variables
1. Open terminal on /shortemall/ and run: pip install -r requirements.txt
1. Go to: https://chromedriver.chromium.org/downloads, download the driver version of your locally installed chrome - browser version. 
2. Insert the chrome driver file path into the config.ini file on Drivers = " " and Service = "" lines.
3. Go to /input folder and populate stable\_dict.txt with one word per line -- these will be the words that will be permutated and appended to the generated custom URLs
4. Go to /Short\_Em\_All, and on terminal run: python3 short\_em\_all.py

## CLI Options

usage: short_em_all.py [-h] [-t TARGET] [-s [SCREENSHOT]] [-v [VERBOSE]]

optional arguments:

  -h, --help            show this help message and exit
  
  -t TARGET, --target TARGET
                        insert target keyword
			
```
python3 short_em_all.py -t hello 
```
			
  -s [SCREENSHOT], --screenshot [SCREENSHOT]
                        Take screenshots on found results

```
python3 short_em_all.py -t hello -s 
```
		
  -v [VERBOSE], --verbose [VERBOSE]
                        turn on verbose mode

```
python3 short_em_all.py -t hello -s -v 
```

## RUN Options

If you want to execute the script without CLI options:

```
python3 shortemall.py 
```

Then, you con manually configure some scan options: 

```
[*] Do you want to use the dict.txt file to generate URLs? (y: Yes, n: No)
```

  [-] Yes: use the stable\_dict.txt (Short\_Em\_All\Input)
  
  [-] No: insert keyword to run a scan based on single-target
		
```
[*] Do you want to take screenshot for found URLs? (y: Yes, n: No)
```

  [-] Yes: URLs with HTTP Status Code = 200 are screenshotted and saved into /Screenshot
  
  [-] No: no screenshot taken during the scan process
		
```
[*] Do you want to see only existing URLs? (y: Yes, n: No)
```

  [-] Yes: only URLs with HTTP Status Code = 200 are printed on-screen
  
  [-] No: all results are printed on-screen
  

## Notes
Due to presence of false postivies on found URLs, I strongly suggest to enable the screenshots option. This way you can visually filter the results once the scan is terminated. 

## Acknowledgements

The URL verification method implemented in *Short 'Em All!* uses https://seintpl.github.io/osint/short-links-verification-cheatsheet as its dynamic source generation.     
## Contact Info

for any question or further information write to me at: osintmatter@protonmail.com


