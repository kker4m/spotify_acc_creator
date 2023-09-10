from src import *

class account_manager():

    def __init__(self,username: Optional[str]=None, password: Optional[str]=None, store_data: bool = False, two_captcha_api: Optional[str] = None):
        self.driver = None
        self.username = username
        self.password = password
        self.store_data = store_data
        self.two_captcha_api = two_captcha_api
        if two_captcha_api != None:
            config = {
            'server':           '2captcha.com',
            'apiKey':           two_captcha_api,
            'softId':            123,
            'defaultTimeout':    120,
            'recaptchaTimeout':  600,
            'pollingInterval':   10,
        }
            self.solver = TwoCaptcha(**config)
            
    def register(self) -> bool:
        print("Register starting")

        if self.driver == None:
            print("Driver is not ready, please prepare driver before register.")
            return False
        
        ##Check if password or username is static
        if self.username == None:
            username = self.random_text_generator()
        else:
            username = self.username
        
        if self.password == None:
            password = self.random_text_generator()
        else:
            password = self.password
        email = self.random_text_generator(is_mail=True)

        ##Getting the page
        self.driver.get("https://www.spotify.com/us/signup")
        
        ##Wait for the first element of the page which is the email input, then send the random generated mail.
        email_input = self.wait_element(self.driver,By.XPATH,"//input[@type='email']",click=True)
        if not email_input: print("Page not loaded correctly, please turn off the headless mode and debug the process."); return False
        email_input.send_keys(email)

        ##Send the password input to the password input.
        password_input = self.wait_element(self.driver,By.XPATH,"//input[@type='password']",click=True,sleep=3)
        if not password_input :
            for i in range(3):
                ##scroll down 75 pixel
                self.driver.execute_script("window.scrollBy(0,75)","")
                password_input = self.wait_element(self.driver,By.XPATH,"//input[@type='password']",click=True,sleep=3)
                if password_input: break

            if not password_input:
                print("Black register page detected, passing by.")
                return False
        password_input.send_keys(password)

        ##Send the username to the username input.
        username_input = self.wait_element(self.driver,By.XPATH,"//input[@id='displayname']",click=True,sleep=10)
        if not username_input:
            for i in range(3):
                ##scroll down 75 pixel
                self.driver.execute_script("window.scrollBy(0,75)","")
                username_input = self.wait_element(self.driver,By.XPATH,"//input[@id='displayname']",click=True,sleep=3)
                if username_input: break
            if not username_input: return False
        username_input.send_keys(username)

        ##Close cookies
        self.wait_element(self.driver,By.XPATH,"//div[@id='onetrust-close-btn-container']",click=True,sleep=5)

        ##Select the born month with select method
        month = Select(self.driver.find_element(By.XPATH,"//select[@id='month']"))
        month.select_by_value("03") ## Making it march because it is my birthday month :sunglasses:.

        ##Select the born day and year
        self.driver.find_element(By.XPATH,"//input[@id='day']").send_keys(str(random.randint(10,28)))
        self.driver.find_element(By.XPATH,"//input[@id='year']").send_keys(str(random.randint(1990,2004)))

        ##Select random gender
        genders = self.driver.find_element(By.XPATH,"//div[@class='InlineGroup-sc-4o5aq4-0 iNKEny']").find_elements(By.TAG_NAME,'div')
        genders[random.randint(0,len(genders)-1)].click()

        ##Click the register button
        self.wait_element(self.driver,By.XPATH,"//button[@type='submit']",click=True,sleep=3)
        
        
        ##Wait till account is created
        while self.driver.current_url.__contains__("download") != True:
            if self.driver.current_url.__contains__("challenge"):
                print("Captcha detected")                
                if self.two_captcha_api == None:
                    return False
                else:
                    print("Solve progress starting.")
                    if self.captcha_solver():
                        break
            time.sleep(1)
        
        ##Second check for captcha
        while self.driver.current_url.__contains__("download") != True:
            time.sleep(1)

        ##Store the data as data.json with appending the data.
        if self.store_data:
            with open("data.json","a") as f:
                f.write(json.dumps({"email":email,"password":password})+"\n")            
            print("Data stored in data.json")
        
        print(f"Account created with username: {email} and password: {password}")

        return True

    def follow_account(self,url: str) -> bool:
        if self.driver == None:
            print("Driver is not ready, please prepare driver before register.")
            return False

        ##Getting the page
        self.driver.get(url)

        result = self.wait_element(self.driver,By.XPATH,'//button[@data-encore-id="buttonSecondary"]',click=True)
        if result: print("Followed the account."); time.sleep(2)
        else: print("Could not follow the account.")
        return result
    
    def like_playlist(self,url: str) -> bool:

        ##Get url
        self.driver.get(url)

        ##Wait for like button and click it
        result = self.wait_element(self.driver,By.XPATH,'//div[@data-testid="action-bar-row"]/button',click=True)
        if result:
            print("Liked the playlist.")
            time.sleep(3.5)

        return result
    
    def captcha_solver(self) -> bool:
        try:
            ##Solve the captcha with API 
            site_key_element = self.wait_element(self.driver,By.XPATH,'//div[@class="g-recaptcha"]',click=False,print_=False)
            site_key = site_key_element.get_attribute("data-sitekey")

            result = self.solver.recaptcha(sitekey=site_key,url=self.driver.current_url)
            print("Two Captcha API solved captcha, sending the response to the page.")
            captcha_element = self.wait_element(self.driver,By.XPATH,'//textarea[@id="g-recaptcha-response"]',click=False)
            
            ##Make textarea visible
            self.driver.execute_script(
                "arguments[0].setAttribute('style','type: text; visibility:visible;');",
                captcha_element)

            ##Send the response to the textarea
            captcha_element.send_keys(result.get("code"))
            
            time.sleep(2)

            ##Switch the iframe and click the checkbox
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH,'//iframe[@title="reCAPTCHA"]'))
            self.wait_element(self.driver,By.XPATH,'//div[@class="recaptcha-checkbox-border"]',click=True)

            time.sleep(3.5)

            ##Switch back to default content and click the next button
            self.driver.switch_to.default_content()
            self.driver.find_element(By.XPATH,"//button[@name='solve']").click()

            print("Captcha solved successfully.")

            ## show 2captcha Balance.
            balance = self.solver.balance()
            print(f'Your 2captcha balance is ${round(balance, 2)}')

            return True
        except ValidationException as e:
            ##invalid parameters passed
            print("Invalid parameters passed: ",e)
        except NetworkException as e:
            ##network error occurred
            print("Network error occurred: ",e)
        except ApiException as e:
            ##api respond with error
            print("API respond with error: ",e)
        except TimeoutException as e:
            ##captcha is not solved so far
            print("Captcha is not solved so far.")

        return False

    def prepare_driver(self,headless: bool = False,page_load_str: str = "normal") -> bool:
        try:
            self.driver = callUcDriver(headless=headless,pageLoadStrategy=page_load_str)
            return True
        except:
            return False

    def quit_driver(self) -> bool:
        try:
            self.driver.quit()
            return True
        except:
            return False

    def random_text_generator(self,is_mail: bool = False,lenght: int = 10) -> str:
        harfler = string.ascii_letters
        kullanici_adi = ''.join(random.choice(harfler) for _ in range(lenght))
        if is_mail:
            kullanici_adi+="@gmail.com"
        return kullanici_adi

    @staticmethod
    def wait_element(driver: webdriver,element_type,element:str,click: bool = False,trys: int = 1,sleep: int = 20,print_: bool = True):
        while trys>0:
            try:
                if click:
                    WebDriverWait(driver, sleep).until(EC.presence_of_element_located((element_type,element))).click()
                else:
                    WebDriverWait(driver, sleep).until(EC.presence_of_element_located((element_type, element)))

                return driver.find_element(element_type, element)
            except:
                    trys-=1
        if print_:
            print(f"Element {element} could not be clicked.")
        return False

##Version checker
def checkVersion() -> bool:
    r = httpx.get('https://raw.githubusercontent.com/linuxkerem/spotify_acc_creator/master/src/__version__.py')
    if r.status_code == 200:
        global_data = dict()
        local_data = dict()

        exec(r.text, global_data)

        with open('src/__version__.py', 'r', encoding='utf-8') as f:
            exec(f.read(), local_data)

        if local_data['__version__'] == global_data['__version__']:
            return True
        else:
            return False
    else:
        return True



if __name__ == "__main__":
    if not checkVersion():
        print('Found some updates on the project! Download the latest version from https://github.com/linuxkerem/spotify_acc_creator to use the tool!')
        exit()

    account_urls = []
    playlist_urls = []
    two_captcha_api = None
    while True:
        print(f"Current accounts to follow: {account_urls}\nCurrent playlists to like: {playlist_urls}\nCurrent 2captcha api: {two_captcha_api}\n")
        choice = input("1-) Add account to follow\n2-) Add playlist to like\n3-) Add 2captcha api\n4-) Start the process\n5-) Exit\n\n")
        if choice == "1":
            account_urls.append(input("Account url: "))
        elif choice == "2":
            playlist_urls.append(input("Playlist url: "))
        elif choice == "3":
            two_captcha_api = input("2captcha api: ")
        elif choice == "4":
            count = int(input("How many accounts do you want to create: "))
            headless_choice = input("Do you want to run the process in headless mode? (y/n) ( Not working correctly ): ")
            if headless_choice == "y":
                headless = True
            else:
                headless = False
            break
        
        elif choice == "5":
            exit()
        else:
            print("Wrong choice, please try again.")

    x = account_manager(store_data=True,username="Super bot",two_captcha_api=two_captcha_api)
    
    while count > 0:
        x.prepare_driver(headless=False)
        result = x.register()

        if result:
            for account_url in account_urls:
                x.follow_account(account_url)
                
            for playlist_url in playlist_urls:
                x.like_playlist(playlist_url)
            
            count-=1
        
        x.quit_driver()