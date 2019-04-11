'''
Python Script that downloads all your messenger media from a selected conversation. @Arland 7/4/19
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from getpass import getuser
import requests
import os
import time

# disables notifications from chrome
options: Options = Options()
prefs: dict = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
# if true enables headless chrome
options.headless = True

path: str = '/Users/arlandtorres/dev/projects/messengerScript/chromedriver'
# path: str = r'C:\Users\AVTORRES\messenger_script\chromedriver.exe'
url: str = 'https://www.facebook.com'
# creates media directory
os.makedirs('media', exist_ok=True)

# get user details
user: str = getuser()
print('Hello ' + user + '!')

email: str = input('Email: ')
password: str = getpass(prompt='Password: ')

# log into facebook
browser: webdriver = webdriver.Chrome(path, options=options)
browser.implicitly_wait(10)
browser.get(url)
try:
    login_form: webdriver = browser.find_element(By.NAME, 'email')
    login_form.send_keys(email)
    print('Login form found, inputting email...')
except:
    print('Was not able to find login form.')
try:
    password_form: webdriver = browser.find_element(By.NAME, 'pass')
    password_form.send_keys(password)
    print('Password form found, inputting password...')
except:
    print('Was not able to find password form.')

password_form.submit()
print('Logging in...')

current_url: str = browser.current_url

if current_url == 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110':
    print('Could not log in.')
else:
    print('Successfully logged in.')

# navigate to messenger
try:
    messenger_icon: webdriver = browser.find_element(By.NAME,
                                                     'mercurymessages')
    messenger_icon.click()
    print('Messenger icon selected...')
except:
    print('Was not able to find messenger icon.')
try:
    messenger_link: webdriver = browser.find_element(By.LINK_TEXT,
                                                     'See all in Messenger')
    messenger_link.click()
    print('Messenger link clicked...')
except:
    print('Could not find messenger link.')

# prints list of conversations
try:
    conversations: list = []
    n: int = 1
    conversation = browser.find_elements(
        By.XPATH, '//*[@aria-label="Conversation list"]/li')

    num_conversation = len(conversation)
    print(f'First {num_conversation} messages found:')

    while n < len(conversation) + 1:
        name = browser.find_element(
            By.XPATH,
            f'//*[@aria-label="Conversation list"]/li[{n}]/div/a/div/div'
        ).get_attribute('data-tooltip-content')
        conversations.append(name)
        n += 1
except:
    print('Conversations not found')

for n in range(len(conversations)):
    print(f'{n + 1}. ' + conversations[n])

prompt = input('Would you like to select from this list? (Y)/(N): ').lower()

if prompt == 'n':
    # find message
    message_input_form = browser.find_element(
        By.XPATH, '//*[@aria-label="Search Messenger"]')

    query = input('Enter your contact name: ')
    message_input_form.send_keys(query)

    def getX(query):
        if len(query) == 1:
            return 1
        elif len(query) > 1:
            return 2

    x = getX(query)
    # print('x = ' + str(x))

    try:
        contacts = []
        n = 1
        ul = browser.find_elements(By.XPATH, f'//*[@class="_29hk"][{x}]/ul/li')
        # print(f'.//*[@class="_29hk"][{x}]')
        # for li in ul:
        #     name = browser.find_element_by_xpath(
        #         f'//*[@class="_29hk"][{x}]/ul/li[{n}]/a/div/div[2]/div/div').text
        #     contacts.append(name)
        #     n += 1
        while n < len(ul) + 1:
            name = browser.find_element(
                By.XPATH,
                f'//*[@class="_29hk"][{x}]/ul/li[{n}]/a/div/div[2]/div/div'
            ).text
            contacts.append(name)
            n += 1
    except:
        print('Failed')

    print(f'Contacts found in \'{query}\':')
    for name in range(len(contacts)):
        print(contacts[name])

    # select message
    selection_query = input('Choose contact from list: ')

    if selection_query in contacts:
        selection = browser.find_element(By.XPATH,
                                         f'//div[text()="{selection_query}"]')
        selection.click()
        print(f'{selection_query} selected...')
    else:
        print('Contact not found')
elif prompt == 'y':
    number = int(
        input('Enter the number of the message you would like to select: '))

    choice = browser.find_element(
        By.XPATH,
        f'//*[@aria-label="Conversation list"]/li[{number}]/div/a/div/div'
    ).get_attribute('data-tooltip-content')

    browser.find_element(
        By.XPATH,
        f'//*[@aria-label="Conversation list"]/li[{number}]/div/a/div/div'
    ).click()

    print(f'{choice} selected...')

# selects first photo
try:
    photo: webdriver = browser.find_element(By.XPATH,
                                            './/*[@aria-label="photo"][1]')
    print('1st instance of media selected...')
    photo.click()
except:
    print('Could not find media.')


# download media
def Download():
    # find src url
    try:
        img: webdriver = browser.find_element(By.XPATH,
                                              '//*[@class="_4-od"]/div/img')
        src: str = img.get_attribute('src')
    except:
        print('Could not find media.')
    # get image name
    ext: str = '.jpg'
    url_part: str = src[:src.find(ext) + len(ext)]
    # returns https://scontent-lht6-1.xx.fbcdn.net/v/t1.15752-9/56669445_426465788110092_783547496742780928_n.jpg
    # url_part_2 = url_part.split('/')
    fwd_slash: str = '/'
    img_name: str = url_part[url_part.rfind(fwd_slash):]
    # print(img_name)
    res = requests.get(src)
    res.raise_for_status()
    print(f'Downloading image: ' + img_name)
    # save media to ./media
    img_file = open(os.path.join('media', os.path.basename(img_name)), 'wb')
    for chunk in res.iter_content(100000):
        img_file.write(chunk)
    img_file.close()
    print(f'Saving image: ' + img_name + ' to /media...')


# download media loop
Download()
time.sleep(1)
is_next = True
while is_next:
    # get the next piece of media
    try:
        next_btn: webdriver = browser.find_element(
            By.XPATH, '//*[@class="_ohf rfloat"]/a')
        next_btn_state: str = next_btn.get_attribute('aria-disabled')
        print(next_btn_state)
    except:
        print('Next button not found.')

    if next_btn_state == 'false':
        next_btn.click()
        print('Next media selected...')
        Download()
    elif next_btn_state == 'true':
        print('Next media not found.')
        is_next = False

print('Done.')
browser.close()
