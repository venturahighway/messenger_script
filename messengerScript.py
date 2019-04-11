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

# email: str = input('Email: ')
# password: str = getpass(prompt='Password: ')
email = 'arland.torres@outlook.com'
password = 'AFgt9597*'

# log into facebook
browser: webdriver = webdriver.Chrome(path, options=options)
browser.implicitly_wait(10)
browser.get(url)
try:
    login_form: webdriver = browser.find_element_by_name('email')
    login_form.send_keys(email)
    print('Login form found, inputting email...')
except:
    print('Was not able to find login form.')
try:
    password_form: webdriver = browser.find_element_by_name('pass')
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
    messenger_icon: webdriver = browser.find_element_by_name('mercurymessages')
    messenger_icon.click()
    print('Messenger icon selected...')
except:
    print('Was not able to find messenger icon.')
try:
    messenger_link: webdriver = browser.find_element_by_link_text(
        'See all in Messenger')
    messenger_link.click()
    print('Messenger link clicked...')
except:
    print('Could not find messenger link.')

# prints list of conversations
# conversations: list = []
# n: int = 1
# conversation = browser.find_elements_by_xpath(
#     '//*[@aria-label="Conversation list"]/li')

# num_conversation = len(conversation)
# print('Number of conversations found: ' + str(num_conversation))

# try:
#     for c in conversation:
#         name = c.find_element_by_xpath(
#             f'//*[@aria-label="Conversation list"]/li[{str(n)}]/div/a/div/div'
#         ).get_attribute('data-tooltip-content')
#         conversations.append(name)
#         n += 1
# except:
#     print('Conversations not found')

# print(conversations)

# find message
message_input_form = browser.find_element_by_xpath(
    '//*[@aria-label="Search Messenger"]')

query = input('Enter your contact\'s name: ')
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
    ul = browser.find_elements_by_xpath(f'//*[@class="_29hk"][{x}]/ul/li')
    # print(f'.//*[@class="_29hk"][{x}]')
    for li in ul:
        name = browser.find_element_by_xpath(
            f'//*[@class="_29hk"][{x}]/ul/li[{n}]/a/div/div[2]/div/div').text
        contacts.append(name)
        n += 1
except:
    print('Failed')

print(f'Contacts found in \'{query}\':')
for name in range(len(contacts)):
    print(contacts[name])

# select message
selection_query = input('Enter contact name: ')

if selection_query in contacts:
    selection = browser.find_element_by_xpath(
        f'//div[text()="{selection_query}"]')
    selection.click()
    print(f'{selection_query} selected...')
else:
    print('Contact not found')

print('Done.')
browser.close()