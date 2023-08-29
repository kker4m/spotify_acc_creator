from src import *


if __name__ == "__main__":
    driver = callUcDriver(headless=False,data_directory="/home/kerem/.config/chromium/Default")
    driver.get("https://www.google.com/")
    print("Done")
    input("")