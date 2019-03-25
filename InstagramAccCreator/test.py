#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random


global browser
global accountscreated
seperators = ['.', '', '_', '-']
endings = ['.com', '.it', '.ch', '.de', '.pl', '.fr']
providers = ['@online', '@yahoo', '@gmail', '@gmx', '@outlook', '@web', '@freenet', '@googlemail', '@aol', '@yandex',
             '@protonmail', '@zoho', '@mail', '@tutanota', '@icloud']
useragents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
              'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0']
password = ''


def loadproxies():
    print("Fetching secure proxies...\n")
    browser.get('https://free-proxy-list.net/')
    proxylist = browser.find_element_by_xpath('/html/body/section[1]/div/div[2]/div/div[2]/div/table/tbody').text.split('\n')
    validproxies = []  # Format -> [ [ HOST , PORT ] , [ HOST , PORT ] ]
    for i in range(0, len(proxylist)-1):
        _ = proxylist[i].split()
        validproxies.append([_[0], _[1]])
    return validproxies


def changebrowser(browser):  # host, port
    profile = webdriver.FirefoxProfile()

    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)

    profile.set_preference("general.useragent.override", random.choice(useragents))

    # profile.set_preference("network.proxy.type", 1)
    # profile.set_preference("network.proxy.http", host)
    # profile.set_preference("network.proxy.http_port", port)

    profile.update_preferences()
    browser = webdriver.Firefox(firefox_profile=profile)
    browser.delete_all_cookies()
    return browser


def generatevalidemail(identity):
    forename, surename = identity
    email = forename + random.choice(seperators) + surename + random.choice(providers) + random.choice(endings)
    print("Generate Email:", email)
    return email


def generatevalididentity():
    browser.get('https://fakenamegenerator.com/')
    identity = browser.find_element_by_class_name('address')
    name = identity.text[:int(identity.text.find('\n'))]
    forename, surename = name.split()[0], name.split()[-1]
    print("Generate Identity:", forename, surename)
    return forename, surename


def createaccount():

    identity = generatevalididentity()
    email = generatevalidemail(identity)

    browser.get('https://instagram.com/')

    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.NAME, 'emailOrPhone')))

    input_email = browser.find_element_by_name('emailOrPhone')
    input_name = browser.find_element_by_name('fullName')
    input_username = browser.find_element_by_name('username')
    input_password = browser.find_element_by_name('password')

    input_email.send_keys(email)
    input_name.send_keys(identity[0] + ' ' + identity[1])
    input_username.send_keys('' + Keys.TAB)

    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/span/section/main/article/div[2]/div[1]/div/form/div[5]/div/div[2]/div/button/span')))

    suggestedusername = browser.find_element_by_xpath(
        '/html/body/span/section/main/article/div[2]/div[1]/div/form/div[5]/div/div[2]/div/button/span')
    suggestedusername.click()
    username = browser.find_element_by_name('username').text

    input_password.send_keys(password + Keys.RETURN)

    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.NAME, 'ageRadio')))

    age18 = browser.find_element_by_name('ageRadio')
    age18.click()
    submit = browser.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/button')
    submit.click()

    with open('accounts.txt', 'a+') as file:
        string = 'Forename: {} | Surename: {} | username: {} | email: {} | Password: {} \n'.format(identity[0],
                                                                                                   identity[1],
                                                                                                   username, email,
                                                                                                   password)
        file.write(string)

    print("Account created!")


if __name__ == '__main__':
    try:
        print("Loading...")
        browser = webdriver.Firefox()
        # validproxies = loadproxies()
        password = str(input("Master-Password: "))
        iteration = int(input("Accounts: "))
        accountscreated = 0

        for i in range(iteration):
            try:
                createaccount()
                accountscreated += 1
            except TimeoutException:
                print("Timeout detected!\nDeleting cookies...Changing User-Agent")
                input("Please change your VPN to continue! (Press ENTER to continue botting")
                browser = changebrowser(browser)
                # validproxies.remove(validproxies[0])

    except KeyboardInterrupt:
        print("Closing Browser")
        browser.quit()
        print("Created [{}|{}] accounts".format(accountscreated, iteration))
