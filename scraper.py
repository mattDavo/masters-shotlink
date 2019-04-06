#!/usr/local/bin/python3

import array

from shot_parser import get_shots_from_inner_html

from selenium import webdriver

from shot import Shot

player_id = 34046
round_n = 2
hole_n = 1


browser = webdriver.Chrome()

url = "http://2018.masters.com/en_US/scores/track/track.html?" + \
      "pid=" + str(player_id) + "&r=" + str(round_n) + "&h=" + str(hole_n) + "&s=1&c="

# navigate to the page
browser.get(url)

# returns the inner HTML as a string
inner_html = browser.execute_script("return document.body.innerHTML").encode("utf-8").decode()

browser.quit()

get_shots_from_inner_html(inner_html, hole_n)
