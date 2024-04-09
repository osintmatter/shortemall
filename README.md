```
   _____ _                _     _ ______                      _ _   _ 
  / ____| |              | |   ( )  ____|               /\   | | | | |
 | (___ | |__   ___  _ __| |_  |/| |__   _ __ ___      /  \  | | | | |
  \___ \| '_ \ / _ \| '__| __|   |  __| | '_ ` _ \    / /\ \ | | | | |
  ____) | | | | (_) | |  | |_    | |____| | | | | |  / ____ \| | | |_|
 |_____/|_| |_|\___/|_|   \__|   |______|_| |_| |_| /_/    \_\_|_| (_)
                                                                    
  by  OSINTMATTER                                                      
                                                                     v3.0_2024
```
---


## Table of Contents

- [Introduction](#introduction)
- [Features](#Main_Features)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Example Usages](#example-usages)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Short'Em All is a Python-based tool that automates the process of scanning URLs. It utilizes various techniques to gather information about short URLs, such as taking screenshots of landing pages, checking for the existence of URLs, and filtering results based on user preferences.

## New_Features_of_Short'Em_All_v3
- **Scanning Specific Short URL Providers:** Users can now target specific short URL providers for scanning, providing more flexibility and efficiency in their investigations.
- **Auto-Configuration for Improved User Experience:** The tool now offers auto-configuration options to streamline the setup process and ensure optimal performance.
- **Enhanced Screenshot Management:** Short'Em All now utilizes Chromedriver and Selenium for screenshot capture, reducing user intervention and ensuring greater stability.
- **Total Code Refactoring:** The codebase has undergone extensive refactoring to improve readability, maintainability, and overall performance
## Main_Features
- **Automated Scanning:** Short'Em All automates the process of scanning URLs, saving time and effort.
- **Screenshot Capture:** It can capture screenshots of landing pages to provide visual insights.
- **Notification System:** Users can receive email notifications about scan results.
- **Customization:** Users can customize scan options based on their requirements.

## Installation

To install Short'Em All, follow these steps:

1. Clone the repository:

```bash
gh repo clone osintmatter/shortemall
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Before You Begin:

- Ensure you have installed Python and pip (at least version 3.8).
- Run the tool on a Linux machine or Linux Virtual Host.
- Obtain the OAuth 2.0 client ID for your Gmail account and save the generated credentials file as `credentials.json` in the main folder - follow this step-by-step guide: https://support.google.com/cloud/answer/6158849?hl=en#zippy=
- Edit the `config.py` file to set variables such as `my_email`, `to_email`.
- After first run, ensure you have the required configuration files (`config.ini` and `gmail.pickle`) in the current directory.

## Usage

To use Short'Em All, follow the steps below:

1. Run the `short_em_all.py` script.
2. Follow the on-screen prompts to configure the scan options.
3. Review the scan results displayed in the terminal and read the output.txt file and Screenshots Scan folder.

## Options

Short'Em All provides several command-line options to customize the scanning process:

- `-t, --target`: Insert the target keyword for this scan.
- `-d, --dictionary`: Use a stable dictionary for this scan.
- `-n, --notifications`: Disable email notifications on found results.
- `-z, --zero`: Disable taking screenshots on URLs landing pages.
- `-f, --found`: Show only found scan results.
- `-r, --singlescan`: Use single scan mode (no data retention).
- `-e, --email`: Receive email notification on the target scan.
- `-s, --screenshot`: Enable taking screenshots on found results.
- `-v, --verbose`: Enable verbose mode.

## Example Usages

1. Perform a scan with default settings:

```bash
python short_em_all.py
```

2. Perform a scan with custom options:

```bash
python short_em_all.py -t example_target -s -e
```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on the GitHub repository.

## Acknowledgements

The URL verification method implemented in Short 'Em All! uses [Short Links Verification Cheatsheet](https://seintpl.github.io/osint/short-links-verification-cheatsheet) as its dynamic source generation.

## Disclaimer

Short'Em All! adopts a preview mode for each individual URL generated to minimize unwanted direct traffic to short URL providers. However, it is recommended to use the tool responsibly and sparingly for educational and research purposes.

## Contact Info

For questions or further information, contact us at info@osintmatter.com.

You can also find us on Twitter: [Osint Matter](https://twitter.com/MatterOsint)

Visit our website: [osintmatter.com](https://osintmatter.com)
