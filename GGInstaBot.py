from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time
import random
import getpass


ascii_art = """
  ________  ________  .___ _______    _________________________
 /  _____/ /  _____/  |   |\\      \\  /   _____/\\__    ___/  _  \\
/   \\  ___/   \\  ___  |   |/   |   \\ \\_____  \\   |    |/  /_\\  \\
\\    \\_\\  \\    \\_\\  \\ |   /    |    \\/        \\  |    /    |    \\
 \\______  /\\______  / |___\\____|__  /_______  /  |____|\\____|__  /
        \\/        \\/              \\/        \\/                 \\/
"""

print(ascii_art)


print(f'Please Enter Your Instagram Username: ')
username_input = input()

def get_hidden_input(prompt="Enter password: "):
    return getpass.getpass(prompt)

#Basic password security feature:
pw_input = get_hidden_input()

print(f'Provide the link to the Instagram post you would like to comment on\n Ex. https://www.instagram.com/p/C313XrCL6fN/?img_index=1')
page_input = input()


file_path = 'username.txt'
random_username = []

with open(file_path, 'r') as file:
    for line in file:
        # Append each line to the list (removing newline characters)
        random_username.append(line.strip())

print(f'The username list you are using is: ')
print(random_username)


randomtime = random.randint(1, 7) #Whenever this variable is called it is to try to avoid Instagram's bot detection

browser = webdriver.Firefox()

browser.get('http://www.instagram.com')

browser.implicitly_wait(10) # wait up to 10 seconds for elements to become available
elem = browser.find_element(By.NAME, 'username')  # Find the search box

elem.send_keys(username_input + Keys.RETURN)

time.sleep(randomtime)
elem = browser.find_element(By.NAME, 'password')  # Find the search box

elem.send_keys(pw_input + Keys.RETURN)

time.sleep(25)
browser.get(page_input)
time.sleep(5)
elem = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/textarea')
browser.implicitly_wait(2)
elem.click()
browser.implicitly_wait(10)

max_retries = 3 

#For loop to run through every username provided in "username.txt"
for i in random_username:                       
    for attempt in range(max_retries):
        try:
            elem = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/textarea')
            time.sleep(randomtime)
            elem.send_keys(i + Keys.RETURN)  # send each username individually
            break
        except StaleElementReferenceException: #This is to fix Selenium's StaleElementRefrence error (Sometimes instagram updates page and bricks the script due to the element being updated)
            if attempt == max_retries - 1:
                raise
            else:
                print("Retrying...")


 #Instagram limits comments to 180 per day, if you recieve the "Couldn't Post comment." error you have been flagged as a bot or reached the limit
    get_source = browser.page_source
    search_text = "Couldn't post comment."
if search_text in get_source:
    print("Comment Error = True")      
    browser.implicitly_wait(10)
    elem.clear()
    time.sleep(10) # loop every 10 seconds