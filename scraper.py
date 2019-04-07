#!/usr/local/bin/python3

import array
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from constants import players_2018
from shot import Shot
from shot_parser import get_shots_from_inner_html

testing_players = [21209, 34046, 34360, 32102]
players = players_2018

holes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
rounds = [1, 2, 3, 4]


browser = webdriver.Chrome()

url = "http://2018.masters.com/en_US/scores/track/track.html?pid=34046&r=4&h=18&s=1&c="


class element_has_inner_html(object):
    """An expectation for checking that an element has non empty innerHTML

    locator - used to find the element
    returns the element once it has the particular css class
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        # Finding the referenced element
        element = driver.find_element(*self.locator)
        if element.get_attribute("innerHTML") is not "":
            return element
        else:
            return False


# TODO:
# Cleanup
# Make the maps


with open("shots.csv", "w+") as csv_f:
    writer = csv.writer(csv_f, quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    # Since a load of the tracking for the player bulk loads all their shots, for performance
    # reasons we iterate through the players, tracking all of their shots before moving onto the
    # next.
    for p in players:
        url = "http://2018.masters.com/en_US/scores/track/track.html?" + \
            "pid=" + str(p) + "&r=" + str(rounds[0]) + "&h=" + str(holes[0]) + "&s=1&c="
        browser.get(url)

        element = WebDriverWait(browser, 10).until(element_has_inner_html((By.ID, "holePar")))

        for r in rounds:
            # Check if the player played the round
            played = browser.execute_script(
                "return document.getElementsByClassName(\"round\")[" + str(r-1) + "].classList." +
                "contains(\"enabled\")")
            if not played:
                print("No round %d for player %d, skipping" % (r, p))
                continue
            else:
                print("Getting shot data for player %d round %d" % (p, r))

            # Select the round
            browser.execute_script(
                "document.getElementsByClassName(\"round\")[" + str(r-1) + "].click()")

            for h in holes:
                # Select the hole
                browser.execute_script(
                    "document.getElementsByClassName(\"hole\")[" + str(h-1) + "].click()")

                # returns the inner HTML as a string
                inner_html = browser.execute_script(
                    "return document.body.innerHTML").encode("utf-8").decode()

                shots = get_shots_from_inner_html(inner_html, h)

                for shot in shots:
                    shot.round = r
                    shot.player_id = p
                    writer.writerow(shot.csv_dump())

browser.quit()
