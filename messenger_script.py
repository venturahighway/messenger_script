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
        path = os.getcwd() + 'drivers\\chromedriver.exe'
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        return path, desktop
    else:
        path = os.getcwd() + 'drivers/chromedriver'
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        return path, desktop

def get_credentials():
    '''Get Facebook credentials.'''
    email = input('Email: ')
    password = getpass(prompt='Password: ')
    return email, password

def setup(email, password):
    '''Opens Chrome in headless mode and nagivates to Facebook messenger.'''
    driver.get('https://www.facebook.com')
    try:
        driver.find_element_by_name('email').send_keys(email)
        logger.debug('Login form found, sending email')
    except NoSuchElementException:
        logger.error('Unable to locate login form')
    try:
        elm_passform = driver.find_element_by_name('pass')
        elm_passform.send_keys(password)
        elm_passform.submit()
        logger.debug('Password form found, sending password')
    except NoSuchElementException:
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

def find_conversations():
    '''Prints to console a list of conversations found.'''
    elm_conversations = driver.find_elements_by_xpath('//*[@aria-label="Conversation list"]/li')
    names = []
    n = 1

    logger.debug(str(len(elm_conversations)) + ' Conversations found')

    while n < len(elm_conversations) + 1:
        elm_name = driver.find_element_by_xpath(f'//*[@aria-label="Conversation list"]/li[{n}]/div/a/div/div'
            ).get_attribute('data-tooltip-content')
        names.append(elm_name)
        n += 1

    for index, name in enumerate(names, start=1):
        print(index, name)

def get_selection():
    '''Prompt the user to choose whether or not he wants to choose from the list of conversations or if he wants to search a specific contact.
    
    1 = select
    2 = search
    Returns an int for selection.'''
    while True:
        try:
            selection = int(input('Would you like to select from this list or search for a conversation? Enter 1 to select or 2 to search: '))
        except ValueError:
            print('Sorry, I didn\'t understand that')
            continue
        if selection < 0 or selection > 2:
            print('Sorry, please enter 1 or 2')
        else:
            break
    return selection

def check_selection(selection):
    '''Selects or searches a conversation depending on selection given.

    Returns name of conversation.'''
    contacts = []
    if selection == 1:
        n = input('Please select the number that corresponds to the conversation you want to access: ')
        driver.find_element_by_xpath(f'//*[@aria-label="Conversation list"]/li[{n}]/div/a/div/div').click()
        return driver.find_element_by_xpath(f'//*[@aria-label="Conversation list"]/li[{n}]/div/a/div/div'
        ).get_attribute('data-tooltip-content')
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
            for index, name in enumerate(contacts, start=1):
                print(index, name)
            n = input('Please select the number that corresponds to the conversation you want to access: ')
            driver.find_element_by_xpath(f'//*[@class="_29hl"]/li[{n}]/a/div/div[2]/div/div').click()
            return driver.find_element_by_xpath(f'//*[@class="_29hl"]/li[{n}]/a/div/div[2]/div/div').text
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
            n = input('Please select the number that corresponds to the conversation you want to access: ')
            driver.find_element_by_xpath(f'//*[@class="_11_d _705p _4p-s"]/div[2]/ul/li[{n}]/a/div/div[2]/div/div').click()
            return driver.find_element_by_xpath(f'//*[@class="_11_d _705p _4p-s"]/div[2]/ul/li[{n}]/a/div/div[2]/div/div').text

def create_folder():
    '''Creates a folder with the name of the conversation on the desktop.

    If the folder already exists it will create another folder of the same name with (n) appended.

    Returns folder path.'''
    folder = desktop + '\\' + name_media
    n = 1
    if os.path.isdir(folder) == True:
        while True:
            try:
                os.mkdir(os.path.join(desktop, name_media + '(' + str(n) + ')'))
                break
            except OSError:
                n += 1
                continue
        return os.path.join(desktop, name_media + '(' + str(n) + ')')
    else:
        os.mkdir(os.path.join(desktop, name_media))
        return os.path.join(desktop, name_media)
        
def check_media_type():
    '''Checks whether if the media selected is an image or video.
    
    Returns 1 for image, 2 for video.'''
    try:
        if driver.find_element_by_xpath('//*[@class="_4-od"]/div/img').get_attribute('src') != None:
            return 1
    except:
        if driver.find_element_by_xpath('//*[@class="_4-od"]/div/div/video').get_attribute('src') != None:
            return 2

def scrape(media_type):
    '''Downloads the image or video and saves it to the conversation folder.'''
    if media_type == 1:
        try:
            # find source URL
            src = driver.find_element_by_xpath('//*[@class="_4-od"]/div/img').get_attribute('src')
            # get file name
            ext = '.jpg'
            url_part = src[:src.find(ext) + len(ext)]
            file_name = url_part[url_part.rfind('/'):]
            res = requests.get(src)
            res.raise_for_status()
            # save file to Messenger Media folder
            file = open(os.path.join(folder_path, os.path.basename(file_name)),'wb')
            for chunk in res.iter_content(100_000):
                file.write(chunk)
            file.close()
            logger.debug(f'Saving image: {file_name} to desktop')
        except NoSuchElementException:
            logger.error('Could not locate image')
    elif media_type == 2:
        try:
            src = driver.find_element_by_xpath('//*[@class="_4-od"]/div/div/video').get_attribute('src')
            ext = '.mp4'
            url_part = src[:src.find(ext) + len(ext)]
            file_name = url_part[url_part.rfind('/'):]
            res = requests.get(src)
            res.raise_for_status()
            file = open(os.path.join(folder_path, os.path.basename(file_name)),'wb')
            for chunk in res.iter_content(100_000):
                file.write(chunk)
            file.close()
            logger.debug(f'Saving video: {file_name} to desktop')
        except NoSuchElementException:
            logger.error('Could not locate video')

t_start = timer()
path, desktop = check_platform()
options = Options()
prefs = {'profile.default_content_setting_values.notifications': 2}
options.add_experimental_option('prefs', prefs)
options.headless = True
driver = webdriver.Chrome(path, options=options)
driver.maximize_window()
driver.implicitly_wait(2)
email, password = get_credentials()
setup(email, password)
find_conversations()
selection = get_selection()
name_media = check_selection(selection)

# Selects the first instance of media on the selected conversation
try:
    driver.find_element_by_xpath('.//*[@aria-label="photo"][1]').click()
except NoSuchElementException:
    logger.error('Could not locate media')

folder_path = create_folder()

while True:
    media_type = check_media_type()
    scrape(media_type)
    # If next arrow is enabled, click() otherwise break loop
    if driver.find_element_by_xpath('//*[@class="_ohf rfloat"]/a').get_attribute('aria-disabled') == 'false': 
        driver.find_element_by_xpath('//*[@class="_ohf rfloat"]/a').click()
    else:
        logger.error('Reached last photo/video')
        logger.debug(f'Files saved in {folder_path}')
        break

driver.close()
t_end = timer()
logger.debug('\nRan script in ' + str(t_end - t_start) + 's')
