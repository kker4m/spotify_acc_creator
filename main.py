from src import *

class account_manager():

    def __init__(self,username: Optional[str]=None, password: Optional[str]=None, store_data: bool = False):
        self.driver = None
        self.username = username
        self.password = password
        self.store_data = store_data

    def register(self) -> bool:
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

        ##Getting the page
        self.driver.get("https://www.spotify.com/us/signup")
        
        ##Wait for the first element of the page which is the email input, then send the random generated mail.
        email_input = self.wait_element(self.driver,By.XPATH,"//input[@type='email']",click=True)
        if not email_input: print("Page not loaded correctly, please turn off the headless mode and debug the process."); return False
        email_input.send_keys(self.random_text_generator(is_mail=True))

        ##Click if next step button appears         
        self.wait_element(self.driver,By.XPATH,"//button[@data-testid='submit']",click=True,sleep=1,print_=False)

        ##Send the password input to the password input.
        password_input = self.wait_element(self.driver,By.XPATH,"//input[@type='password']",click=True,sleep=10)
        password_input.send_keys(password)

        ##Click if next step button appears         
        self.wait_element(self.driver,By.XPATH,"//button[@data-testid='submit']",click=True,sleep=1,print_=False)

        ##Send the username to the username input.
        username_input = self.wait_element(self.driver,By.XPATH,"//input[@id='displayname']",click=True,sleep=10)
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

        ##Click if next step button appears         
        self.wait_element(self.driver,By.XPATH,"//button[@data-testid='submit']",click=True,sleep=1,print_=False)


        ##Click the register button
        self.wait_element(self.driver,By.XPATH,"//button[@type='submit']",click=True,sleep=3)
        print(f"Account created with username: {username} and password: {password}")
        
        ##Wait till account is created
        while self.driver.current_url.__contains__("download") != True:
            time.sleep(1)
        
        time.sleep(1)

        ##Store the data as data.json with appending the data.
        if self.store_data:
            with open("data.json","a") as f:
                f.write(json.dumps({"username":username,"password":password})+"\n")            
            print("Data stored in data.json")

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
    
    def prepare_driver(self,page_load_str: str = "normal") -> bool:
        try:
            self.driver = callUcDriver(headless=False,pageLoadStrategy=page_load_str)
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
    def wait_element(driver: webdriver,element_type,element:str,click: bool = False,trys: int = 1,sleep: int = 20,print_: bool = True)-> Union[False,webdriver.webelement]:
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
  
if __name__ == "__main__":
    hesap_url = "https://open.spotify.com/user/21omz5k2xd42jsl4u62gmcdyy"
    playlist_url = "https://open.spotify.com/playlist/0xzimMdfGoMBOMTKxIbS59"

    x = account_manager(store_data=True,username="supre yazilimci")
    for i in range(2):
        x.prepare_driver()
        x.register()
        x.follow_account(hesap_url)
        x.like_playlist(playlist_url)
        x.quit_driver()