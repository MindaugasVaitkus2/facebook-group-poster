#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import requests
import time
import random
import json
import sys
import urllib3
import bs4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.action_chains import ActionChains

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

from config import *
from modules.helpers import *
from modules.translate.google_translate import *

user_login = ''  ## Your facebook user login
user_pass = ''  ## Your facebook user pass
username = ''  ## Your facebook user name

text = """
Your message to be posted on your groups
"""

media_01 = '/media/xxx.mp4'  # Your media 01
media_02 = '/media/xxx.jpg'  # Your media 01
media_03 = '/media/xxx.jpg'  # Your media 01
media_03 = '/media/xxx.jpg'  # Your media 01

CHROME_PATH = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
CHROMEDRIVER_PATH = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

### DO NOT TOUCH BELOW ####

link_main = 'http://facebook.com/'

WINDOW_SIZE = "1920,1080"

options = webdriver.ChromeOptions()

# options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary' ## Local
options.binary_location = CHROME_PATH

# /usr/lib64/chromium-browser/headless_shell

prefs = {"profile.managed_default_content_settings.images": 2,
         "profile.default_content_setting_values.notifications": 2,
         "profile.managed_default_content_settings.popups": 1,
         "profile.managed_default_content_settings.plugins": 1,
         "profile.managed_default_content_settings.geolocation": 2,
         "profile.managed_default_content_settings.media_stream": 2,
         }
options.add_argument('--ignore-certificate-errors')
# options.add_argument("headless")
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
    # executable_path=CHROMEDRIVER_PATH,
    chrome_options=options
)

driver.get(link_main)

input_email = driver.find_element_by_xpath("//input[@name='email']")
input_pass = driver.find_element_by_xpath("//input[@name='pass']")

input_email.send_keys(user_login)
input_pass.send_keys(user_pass)

input_pass.submit()

link_groups_page = format(link_main + '/' + username + '/groups')

driver.get(link_groups_page)

try:
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
finally:
    print("scrolling is done")

groups = driver.find_elements_by_css_selector('ul > li > div > div > div > div > div > a')

links_groups_all = []

iterator = 1

groups = groups[20:]

for group in groups:
    link = group.get_attribute("href")
    links_groups_all.append(link)

for group in links_groups_all:

    driver.get(group)
    time.sleep(30)
    ## Decide What to Translate

    try:
        description_more = driver.find_element_by_css_selector(
            'span.text_exposed_hide > span.text_exposed_link > a.see_more_link').click()
        description_text = driver.find_element_by_css_selector('div.groupsEditDescriptionArea > div:nth-child(2)')
        time.sleep(30)
        description_text = description_text.text
    except Exception as e:
        description_text = None
        print('desc')
        # print(e)
        pass

    try:
        group_title = driver.find_element_by_css_selector('h1#seo_h1_tag').text
        time.sleep(30)
    except Exception as e:
        group_title = None
        print('title')
        # print(e)
        pass

    # Translate Text

    if (description_text != None):
        text_to_analize = description_text
        lang = detectLang(text_to_analize)
    elif (group_title != None):
        text_to_analize = group_title
        lang = detectLang(text_to_analize)
    else:
        lang = "en"
        # Translate depend on text
    try:
        translated_text = translateText(text, lang)
    except Exception as e:
        # print(e)
        translated_text = text
        pass

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    ## Write Post
    try:
        try:
            post = driver.find_element_by_xpath("//*[text()='Write Post']")
            time.sleep(30)
            post.click()
            layout = 'write'
        except:
            post = driver.find_element_by_xpath("//*[text()='Start Discussion']")
            time.sleep(30)
            post.click()
            layout = 'start'
            pass
        finally:
            print(layout)

        try:
            if (layout == 'start'):

                try:
                    form = WebDriverWait(driver, 60,
                                         ignored_exceptions=ignored_exceptions).until(
                        expect.presence_of_element_located(
                            (By.CSS_SELECTOR, 'div[data-testid="status-attachment-mentions-input"]')))

                    # form = WebDriverWait(driver, 30).until(
                    #     expect.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="status-attachment-mentions-input"]')[iterator])
                    # )
                except KeyError as e:
                    print(e)
                    pass
                finally:
                    form.click()
                    time.sleep(10)
                    form.send_keys(translated_text)
                    time.sleep(10)

            elif (layout == 'write'):
                try:
                    form = WebDriverWait(driver, 60,
                                         ignored_exceptions=ignored_exceptions).until(
                        expect.presence_of_element_located((By.CSS_SELECTOR, 'textarea.navigationFocus')))

                    # form = WebDriverWait(driver, 30).until(
                    #     expect.presence_of_element_located((By.CSS_SELECTOR, 'textarea.navigationFocus')[iterator])
                    # )
                except KeyError as e:
                    print(e)
                    pass
                finally:
                    form.click()
                    time.sleep(10)
                    form.send_keys(translated_text)
                    time.sleep(10)
                    # else:
                    #     form = driver.find_element_by_xpath('//*[@data-testid="status-attachment-mentions-input" OR @class="navigationFocus"] ')

        except KeyError as e:
            print(e)
            print('layout')
            pass

        upload = driver.find_element_by_css_selector("div#pagelet_group_composer")
        driver.execute_script("arguments[0].scrollIntoView();", upload)

        first = driver.find_element_by_css_selector("div > input[type='file']").send_keys(
            os.getcwd() + media_01)  ## Video here
        time.sleep(15)
        second = driver.find_element_by_css_selector("div > input[type='file']").send_keys(
            os.getcwd() + media_02)  ## Image
        time.sleep(15)
        third = driver.find_element_by_css_selector("div > input[type='file']").send_keys(
            os.getcwd() + media_03)  ## Image
        time.sleep(15)
        fourth = driver.find_element_by_css_selector("div > input[type='file']").send_keys(
            os.getcwd() + media_04)  ## Image
        time.sleep(15)

        time.sleep(150)

        submit = driver.find_element_by_css_selector('button[data-testid="react-composer-post-button"]')
        time.sleep(15)
        submit.click()
        time.sleep(15)

        status = True
    except Exception as e:
        print(e)
        status = False
        pass
    finally:
        iterator += 1
        # driver.back()
        print("%s > %s : %s" % (group_title, lang, status))

driver.quit()
