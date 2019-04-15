# Masters Shotlink

Note: this project is no longer being worked on, see [Update](#update)

As golf’s majors don’t have shotlink (http://www.shotlink.com/) there is unfortunately no strokes gained statistics at any of the majors. This is unfortunate since strokes gained is one of the most relied upon statistics in golf as it is more telling than traditional statistics. However, tracking strokes gained statistics requires much more tracking information. Until recently we have never gotten an insight to the US Masters through strokes gained statistics however with Joe Peta’s 3 months of manual work (he talks about in this [podcast](https://shotgunstart.libsyn.com/an-analytical-dive-in-to-the-2019-masters-with-the-brilliant-joe-peta)) and the Masters website tracking functionality (http://2018.masters.com/en_US/scores/track/track.html) he was able to provide the first strokes gained statistics for the masters.

I thought this was interesting, so I looked into the tracking feature. After a bit of digging I thought I would be able to extract all the shot data with a bit of clever web scraping. There are 2 main components to scrape:
- The shot distance, distance from the hole, distance the shot was hit, distance to hole after shot
- The type of ground the ball is lying on for each shot.

The second component was clearly harder to determine as the lie is never just written on the page, it is up to the viewer to interpret (which I assume is what Joe Peta when he did this manually). Now since there are points on the graphic showing the positions of the shots I thought it would be useful if we extract them.

<img src="https://raw.githubusercontent.com/mattDavo/masters-shotlink/master/images/track-example.png" width="600"/>

Now that we have the positions of the shot, how do we use this to figure out the lie types of the shots? Well, what we can do (and what I’ve done) is use the images that the Masters website provides to determine what lies we have at the given positions. However, all the arbitrary pixels aren’t _too_ revealing to a program what the lie is like. So what I’ve done is opened up these images in photoshop and turned them into a map where specific RGB values represent a certain lie. Now we take the positions of shots and look at the color of the corresponding pixel and we will know roughly (more on this later) what lie it was.

<img src="https://raw.githubusercontent.com/mattDavo/masters-shotlink/master/2018/maps/H01W.png" width="600"/>

Now combining the simple text scraping, the pixel mapping and a bit of basic WebDriver page navigation we can record pretty much all of the shot data for a single US Masters tournament we require for strokes gained statistics in about 20 minutes.

## Limitations
If all the shots are hit from the centres of large zones of lie types then this approach should be 100% accurate. However, unfortunately this is not the case and shot will be displayed on the screen very close to the borders of 2 or more lie types, which will lead to mischaracterising shot lie types. But this is the best we can do as we are only provided with so much accuracy as the pixels on the screen.



## Definitions of the categories
Shotlink Standard
- tee: RGB(255, 50, 255)
- fairway: RGB(0, 130, 0)
- rough: RGB(0, 50, 0)
- sand: RGB(255, 255, 0)
- green: RGB(0, 255, 0)
- other: RGB(255, 255, 255)

Additional (to provide more insight)
- pinestraw: RGB(141, 83, 0)
- water: RGB(0, 0, 255)

## Example Output
Written to a csv file with the columns as follows:
```
player_id,
player_name,
shot,
round_no,
par,
hole_n,
shot_type (normal or penalty),
distance_before,
distance_after,
shot_length,
category_before,
category_after,
x (position on the map),
y (position on the map)
```

```sh
# After ./scraper.py
34046,"Jordan Spieth",1,1,4,1,"normal","445yards","156 yards","295 yards","","",642,381

# After ./mapper.py
34046,"Jordan Spieth",1,1,4,1,"normal","445yards","156 yards","295 yards","tee","fairway",642,381
```

## Usage
```sh
# Download all the data
./scraper.py

# Not implemented, due to discontinued track feature
./mapper.py
```

## Requirements
- Python 3
- Python 3 package: selenium
- Chrome webdriver installed
- Python3 package: pypng

## Update
Unfortunately for this project, in 2019 the Masters came out with a new state-of-the-art tracking feature which allows users to see video content of ever shot hit in the masters and see the positions of shots in an interactive 3D experience. This has meant the current state of the project cannot scrape the data, and I anticipate that it will be more difficult to extract the data with the new track feature. However this project should work with the legacy masters websites:
- http://2018.masters.com
- http://2017.masters.com
- http://2016.masters.com
