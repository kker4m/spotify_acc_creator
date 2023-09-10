## Spotify Account Creator Bot

Creates Spotify accounts with **selenium** for you.

## Why selenium instead of requests

Accounts that you create and process with requests will be deleted from your account or playlist you like in about 2 weeks. To avoid this, I decided to use **selenium**, which is a much **slower** but permanent way.

If it is used with **threads** in **headless** mode, it is possible to create 5-10 accounts in a **minute**.

Another disadvantage of using Selenium is encountering **captcha**. I used [twocaptcha](https://2captcha.com/?from=13790483 "twocaptcha") service to solve captcha.

## Usage

- After logging in to **Google Chrome** (If not, download it), go to the **chrome://version** URL. In the first line you can see the version of your **Google Chrome**. Download the **chromedriver.exe** appropriate for your version from [this](https://chromedriver.chromium.org/downloads) url: . Place the **chromedriver.exe** file you downloaded into the **src** folder.
- Run **install.bat** to install all the libraries you need. ( Or you can use manual installation too. )

#### Manual Installation

After downloading the **chromedriver.exe**, clone the **repository** and run this command in CMD, terminal or PowerShell ( Make sure you have **Python **in your machine )

> pip install -r requirements.txt

## Legal Notice

This is illegal if you use this without the consent of the owners (in this case, the Spotify team). I am not accountable for anything you get into, this was just a speedrun to demonstrate how account creators work. This is 100% educational, please do not misuse this tool.
