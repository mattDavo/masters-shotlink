import re
from selenium import webdriver
import png, array

player_id = 34046
round_n = 2
hole_n = 1


browser = webdriver.Chrome()

url = "http://2018.masters.com/en_US/scores/track/track.html?" + \
      "pid=" + str(player_id)  +"&r=" + str(round_n) + "&h=" + str(hole_n) + "&s=1&c="

# navigate to the page
browser.get(url)

# returns the inner HTML as a string
innerHTML = browser.execute_script("return document.body.innerHTML").encode("utf-8")

browser.quit()

class Shot:
    
    def __init__(self):
        self.distance_before = None
        self.distance_after = None
        self.shot_length = None
        self.category_before = None
        self.category_after = None
        self.x = None
        self.y = None
        
    

shots = {}

# Now let's get our info
innerHTML = innerHTML.split("<div class=\"tracker\"", 1)[1]

innerHTML = innerHTML.split("overlay error-message", 1)[0]

innerHTML = innerHTML.split(r"data-shot=", 1)[1]

r = re.search("<div class=\"parTxt\">Par<span id=\"holePar\" class=\"data holePar\">(\d+)</span></div>", innerHTML)
if r:
    par = int(r.group(1))
r = re.search("<div class=\"yardTxt\">YDS<span id=\"holeYds\" class=\"data holeYds\">(\d+)</span></div>", innerHTML)
if r:
    hole_length = int(r.group(1))

for stuff in re.compile("marker(?: plus| hidden)? shot").split(innerHTML):
    r = re.search("\d+", stuff)
    if not r:
        continue
    shot = r.group(0)
    
    if shot not in shots:
        shots[shot] = Shot()
    
    r = re.search("style=\"left: (\d+)px; top: (\d+)px", stuff)
    if r:
        shots[shot].x = int(1024 * (int(r.group(1)) + 10) / 681)
        shots[shot].y = int(768 * (int(r.group(2)) + 10) / 511)
        
for stuff in innerHTML.split("data-shot="):
    r = re.search("\d+", stuff)
    if not r:
        continue
    shot = r.group(0)
    
    if shot not in shots:
        shots[shot] = Shot()
    
    r = re.search("<div class=\"distance\">.*?<span>(\d+)</span>.*?</div>", stuff)
    if r:
        shots[shot].shot_length = r.group(1) + " yards"
        
    r = re.search("<div class=\"distance\">.*?<span class=\"feet\">(\d+)</span>.*?</div>", stuff)
    if r:
        shots[shot].shot_length = r.group(1) + " feet"
        
    r = re.search("<div class=\"topin\">.*?<span>(\d+)</span>.*?</div>", stuff)
    if r:
        shots[shot].distance_after = r.group(1)
    
    r = re.search("<div class=\"topin\">.*?<span class=\"feet\">(\d+)</span>.*?</div>", stuff)
    if r:
        shots[shot].distance_after = r.group(1) + " feet"



reader = png.Reader(filename='maps/H01W.png')
w, h, pixels, metadata = reader.read_flat()

categories = {
    "tee": [255, 50, 255],
    "fairway": [0, 130, 0],
    "rough": [0, 50, 0],
    "sand": [255, 255, 0],
    "green": [0, 255, 0],
    "other": [255, 255, 255],
    "pinestraw": [141, 83, 0]
}


def get_category(pixel):
    for c in categories:
        if abs(pixel[0] - categories[c][0]) + abs(pixel[1] - categories[c][1]) + abs(pixel[2] - categories[c][2]) == 0:
            return c
    return "unknown"


pixel_byte_width = 4 if metadata['alpha'] else 3

shots = [shots[shot] for shot in sorted(shots, key=int)]

for shot in shots:
    pixel_position = shot.x + shot.y * w
    
    pixel = pixels[pixel_position * pixel_byte_width: (pixel_position + 1) * pixel_byte_width]
    
    shot.category_after = get_category(pixel)
    
shots[0].category_before = "tee"
shots[len(shots) - 1].category_after = "hole"
shots[0].distance_before = hole_length
    
for i in range(1, len(shots)):
    shots[i].category_before = shots[i-1].category_after
    shots[i].distance_before = shots[i-1].distance_after
    
for shot in shots:
    print("Shot (distance_before="+str(shot.distance_before) + ",distance_after=" + str(shot.distance_after) + ",shot_length=" + str(shot.shot_length) + ",category_before=" + str(shot.category_before) + ",category_after=" + str(shot.category_after) + ",x=" + str(shot.x) + ",y=" + str(shot.y))

