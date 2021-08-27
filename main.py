import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

FB_EMAIL = 'email@gmail.com'
FB_PASSWORD = 'password'
SEARCH_ACCOUNT = 'instagram'     # should be public

chrome_driver_path = '/Applications/chromedriver'
driver = webdriver.Chrome(chrome_driver_path)


def login():
    # open instagram
    driver.get('https://www.instagram.com/')
    time.sleep(2)
    # login using facebook
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[5]/button').click()
    time.sleep(2)

    # sending facebook login credentials
    driver.find_element_by_id('email').send_keys(FB_EMAIL)
    driver.find_element_by_id('pass').send_keys(FB_PASSWORD)
    time.sleep(1)
    driver.find_element_by_id('loginbutton').click()
    time.sleep(10)

    # dismiss 'allow notifications' popup. if it doesn't exist, wait 5s and try again
    try:
        driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
    except NoSuchElementException:
        time.sleep(5)
        driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
    time.sleep(2)

    print('Logged in to Instagram...')


def search_account():
    # search for an account
    search_box = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
    search_box.send_keys(SEARCH_ACCOUNT)
    time.sleep(3)
    search_box.send_keys(Keys.ENTER)
    search_box.send_keys(Keys.ENTER)
    time.sleep(10)

    print(f'Found account {SEARCH_ACCOUNT}...')


def find_followers():
    # find the number of followers of the account
    follower_count = int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace(',', ''))
    print(f'Account followers: {follower_count}')

    # open the followers of the account
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(5)
    # find the number of followers that have loaded on the screen
    loaded_followers_count = len(driver.find_elements_by_xpath('/html/body/div[6]/div/div/div[2]/ul/div/li'))
    print(f'Loaded {loaded_followers_count} followers...')

    # ##### use 'for i in range(10):' instead of the below match, for accounts with huge followers, to reduce load time #####
    while loaded_followers_count < follower_count:
        # scroll the follower window to fetch and load all followers, not just top few which are loaded by default
        follower_window = driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]')
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follower_window)
        time.sleep(2)
        # update the number of followers that have loaded on the screen
        loaded_followers_count = len(driver.find_elements_by_xpath('/html/body/div[6]/div/div/div[2]/ul/div/li'))
        print(f'Loaded {loaded_followers_count} followers...')

    print('Loaded all followers...')


def follow_all():
    # get all followers
    all_buttons = driver.find_elements_by_css_selector("li button")
    for button in all_buttons:
        # if you are not following the user, then click button
        if button.text.lower() == 'follow':
            button.click()
        time.sleep(1)
    print('Followed all followers...')


def unfollow_all():
    # get all followers
    all_buttons = driver.find_elements_by_css_selector("li button")
    for button in all_buttons:
        # if you are following the user, then click button and confirm unfollow
        if button.text.lower() != 'follow':
            button.click()
            driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button[1]').click()
        time.sleep(1)
    print('Unfollowed all followers...')


login()
search_account()
find_followers()

follow_all()
time.sleep(10)
# unfollow_all()
# time.sleep(10)

driver.quit()
