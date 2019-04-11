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
# options.headless = True

# path: str = '/Users/arlandtorres/dev/projects/messengerScript/chromedriver'
path: str = r'C:\Users\AVTORRES\messenger_script\chromedriver.exe'
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

# search messenger
# try:
#     search_form = browser.find_element_by_xpath(
#         '//*[@aria-label="Search Messenger"]')
#     print('Search form found.')
# except:
#     print('Could not find Search form')

# query = input('Input a contact or group chat name: ')
# search_form.send_keys(query)

# def get_contacts():
#     try:
#         if len(query) == 1:
#             xpath: str = '//*[@class="_29hk"][1]'
#             return xpath
#         elif len(query) > 1:
#             xpath: str = '//*[@class="_29hk"][2]'
#             return xpath
#     except:
#         print('Contacts not found.')

# xpath = get_contacts()

# print(xpath + '/ul/li[i]/a/div/div[2]/div/div')

# contacts_list = browser.find_elements_by_xpath(f'{xpath}')
# print('Number of contacts in ' + query + ': ' + str(len(contacts_list)))

# try:
#     contacts = []
#     i: int = 1
#     if len(query) == 1:
#         contact_list = browser.find_element_by_xpath('//*[@class="_29hk"][1]')
#         x = 1
#         print(str(x))
#     elif len(query) > 1:
#         contact_list = browser.find_element_by_xpath('//*[@class="_29hk"][2]')
#         x = 2
#         print(str(x))
#     for c in contact_list:
#         name = c.find_element_by_xpath(
#             f'//*[@class="_29hk"][{str(x)}]/ul/li[{str(i)}]/a/div/div[2]/div/div'
#         ).text
#         contacts.append(name)
#         i += 1
# except:
#     print('Could not find names.')

# print(contacts)

# //*[@class="_29hl"]/li[]

# //*[@class="_29hk"][1]/ul/li[1]/a/div/div[2]/div/div

# selects first photo
try:
    photo: webdriver = browser.find_element_by_xpath(
        './/*[@aria-label="photo"]')
    print('1st instance of media selected...')
    photo.click()
except:
    print('Could not find media.')


# download media
def Download():
    # find src url
    try:
        img: webdriver = browser.find_element_by_xpath(
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
    print(img_name)
    res = requests.get(src)
    res.raise_for_status()
    print(f'Downloading image: ' + img_name)
    # save media to ./media
    img_file = open(os.path.join('media', os.path.basename(img_name)), 'wb')
    for chunk in res.iter_content(100000):
        img_file.write(chunk)
    img_file.close()
    print(f'Saving ' + img_name + ' to /media...')


# download media loop
is_next = True
while is_next:
    Download()
    # get the next piece of media
    try:
        next_btn: webdriver = browser.find_element_by_xpath(
            '//*[@class="_ohf rfloat"]/a')
        next_btn_state: str = next_btn.get_attribute('aria-disabled')
        print('next_btn_state is ' + next_btn_state)
    except:
        print('Next button not found.')
    if next_btn_state == 'true':
        print('Next media not found.')
        is_next = False
    elif next_btn_state == 'false':
        next_btn.click()
        print('Next media selected...')
        Download()

print('Done.')
browser.close()