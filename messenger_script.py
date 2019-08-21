import os
import requests
import sys
import time
from getpass import getpass
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from timeit import default_timer as timer

def check_platform():
    '''Checks OS and returns the correct driver and desktop path.'''
    platform = sys.platform
    if platform == 'win32': 
        path = os.getcwd() + '\\chromedriver.exe'
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        return path, desktop
    else:
        path = os.getcwd() + '/chromedriver'
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        return path, desktop

def get_selection():
    '''Prompt the user to choose whether or not he wants to choose from the list of conversations or if he wants to search a specific contact.
    
    1 = select
    2 = search'''
    while True:
        try:
            selection = int(input('Would you like to select from this list or search for a conversation? Enter 1 to select or  2 to search: '))
        except ValueError:
            print('Sorry, I didn\'t understand that')
            continue
        if selection < 0 or selection > 2:
            print('Sorry, please enter 1 or 2')
        else:
            break
    return selection

path, _ = check_platform()
# email = input('Email: ')
# password = getpass(prompt='Password: ')
email = 'arland.torres@outlook.com'
password = 'AFgt9597*'
t_start = timer()
options = Options()
prefs = {'profile.default_content_setting_values.notifications': 2}
options.add_experimental_option('prefs', prefs)
# options.headless = True
driver = webdriver.Chrome(path, options=options)
driver.maximize_window()
driver.implicitly_wait(3)
driver.get('https://www.facebook.com')

try:
    driver.find_element_by_name('email').send_keys(email)
    logger.debug('Login form found, sending email')
except:
    logger.error('Unable to locate login form')
try:
    elm_passform = driver.find_element_by_name('pass')
    elm_passform.send_keys(password)
    elm_passform.submit()
    logger.debug('Password form found, sending password')
except:
    logger.error('Unable to locate password form')

current_url = driver.current_url
if current_url == 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110':
    logger.error('Log in unsuccessful')
else:
    logger.debug('Log in successful')

try:
    driver.find_element_by_name('mercurymessages').click()
    driver.find_element_by_link_text('See all in Messenger').click()
except:
    logger.error('Could not navigate to messenger')

elm_conversations = driver.find_elements_by_xpath('//*[@aria-label="Conversation list"]/li')
names = []
contacts = []
n = 1

logger.debug(str(len(elm_conversations)) + ' Conversations found')

while n < len(elm_conversations) + 1:
    elm_name = driver.find_element_by_xpath(f'//*[@aria-label="Conversation list"]/li[{n}]/div/a/div/div'
        ).get_attribute('data-tooltip-content')
    names.append(elm_name)
    n += 1

for index, name in enumerate(names, start=1):
    print(index, name)

selection = get_selection()

if selection == 1:
    n = input('Please select the number that corresponds to the conversation you want to access: ')
    driver.find_element_by_xpath(f'//*[@aria-label="Conversation list"]/li[{n}]/div/a/div/div').click()
elif selection == 2:
    search = input('Enter the name of the conversation you would like to find (Case Sensitive): ')
    elm_search = driver.find_element_by_xpath('//*[@aria-label="Search Messenger"]')
    elm_search.send_keys(search)
    if len(search) == 1: 
        n = 1
        while n < 6:
            contact = driver.find_element_by_xpath(f'//*[@class="_29hl"]/li[{n}]/a/div/div[2]/div/div').text
            contacts.append(contact)
            n += 1
    elif len(search) > 1:
        n = 1
        elm_contacts = driver.find_elements_by_xpath('//*[@class="_11_d _705p _4p-s"]/div[2]/ul/li')
        while n < len(elm_contacts) + 1:
            contact = driver.find_element_by_xpath(f'//*[@class="_11_d _705p _4p-s"]/div[2]/ul/li[{n}]/a/div/div[2]/div/div').text
            separator = '\n'
            if 'mutual friends' in contact:
                contact = contact.split(separator, 1)[0]
            contacts.append(contact)
            n += 1
    for index, name in enumerate(contacts, start=1):
        print(index, name)

driver.close()
t_end = timer()
logger.debug('\nRan script in ' + str(t_end - t_start) + 's')
