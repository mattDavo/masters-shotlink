#!/usr/local/bin/python3

import array
import csv
import time

from selenium import webdriver

from shot import Shot
from shot_parser import get_shots_from_inner_html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

players = [34046, 34360, 32102]
round_n = 2
hole_n = 1

holes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
rounds = [1, 2, 3, 4]


browser = webdriver.Chrome()

url = "http://2018.masters.com/en_US/scores/track/track.html?" + \
      "pid=" + str(players[0]) + "&r=" + str(round_n) + "&h=" + str(hole_n) + "&s=1&c="


class element_has_inner_html(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)   # Finding the referenced element
        if element.get_attribute("innerHTML") is not "":
            return element
        else:
            return False


with open("shots.csv", "w+") as csv_f:
    writer = csv.writer(csv_f, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for p in players:
        url = "http://2018.masters.com/en_US/scores/track/track.html?" + \
            "pid=" + str(p) + "&r=" + str(rounds[0]) + "&h=" + str(holes[0]) + "&s=1&c="
        browser.get(url)

        element = WebDriverWait(browser, 10).until(element_has_inner_html((By.ID, "holePar")))

        for r in rounds:
            browser.execute_script(
                "document.getElementsByClassName(\"round\")[" + str(r-1) + "].click()")
            for h in holes:
                browser.execute_script(
                    "document.getElementsByClassName(\"hole\")[" + str(h-1) + "].click()")

                # returns the inner HTML as a string
                inner_html = browser.execute_script(
                    "return document.body.innerHTML").encode("utf-8").decode()

                shots = get_shots_from_inner_html(inner_html, h)

                for shot in shots:
                    shot.round = r
                    shot.player = p
                    print(shot)
                    writer.writerow(shot.csv_dump())

browser.quit()
