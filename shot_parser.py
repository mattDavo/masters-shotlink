from shot import Shot

import re
import png


MAP_WIDTH = 1024
MAP_HEIGHT = 768
SHOT_MARKER_RADIUS = 10


def get_category(pixel):
    categories = {
        "tee": [255, 50, 255],
        "fairway": [0, 130, 0],
        "rough": [0, 50, 0],
        "sand": [255, 255, 0],
        "green": [0, 255, 0],
        "other": [255, 255, 255],
        "pinestraw": [141, 83, 0]
    }

    for c in categories:
        if abs(pixel[0] - categories[c][0]) + \
                abs(pixel[1] - categories[c][1]) + \
                abs(pixel[2] - categories[c][2]) == 0:
            return c
    return "unknown"


def get_shots_from_inner_html(inner_html, hole, categorize=False):
    shots = {}

    # Now let's get our info
    # Find the hole par
    r = re.search(
        "<div class=\"parTxt\">Par<span id=\"holePar\" class=\"data holePar\">(\\d+)</span></div>",
        inner_html)
    if r:
        par = int(r.group(1))
    else:
        print("Failed to find par")
        print(inner_html)

    # Find the hole length
    r = re.search(
        "<div class=\"yardTxt\">YDS<span id=\"holeYds\" class=\"data holeYds\">(\\d+)</span></div>",
        inner_html)
    if r:
        hole_length = r.group(1) + "yards"

    r = re.search(
        "<canvas id=\"shotCanvas\\d+\" width=\"(\\d+)\" height=\"(\\d+)\" class=\"type1\">",
        inner_html)
    if r:
        canvas_width = int(r.group(1))
        canvas_height = int(r.group(2))

    # Remove some beginning and trailing garbage
    inner_html = inner_html.split("<div class=\"tracker\"", 1)[1]
    inner_html = inner_html.split("overlay error-message", 1)[0]
    inner_html = inner_html.split(r"data-shot=", 1)[1]

    # Find all the coordinates
    for stuff in re.compile("marker(?: plus| hidden)? shot").split(inner_html):
        r = re.search("\\d+", stuff)
        if not r:
            continue
        shot = r.group(0)

        if shot not in shots:
            shots[shot] = Shot()

        r = re.search("style=\"left: (\\d+)px; top: (\\d+)px", stuff)
        if r:
            shots[shot].x = int(MAP_WIDTH * (int(r.group(1)) + SHOT_MARKER_RADIUS) / canvas_width)
            shots[shot].y = int(MAP_HEIGHT * (int(r.group(2)) + SHOT_MARKER_RADIUS) / canvas_height)

    # Find all the distances
    for stuff in inner_html.split("data-shot="):
        r = re.search("\\d+", stuff)
        if not r:
            continue
        shot = r.group(0)

        if shot not in shots:
            shots[shot] = Shot()

        shots[shot].shot = int(shot)
        shots[shot].hole = hole
        shots[shot].par = par

        # Find distance in yards, feet or inches
        r = re.search(
            "<div class=\"distance\">.*?<span>(\\d+)</span>.*?</div>", stuff)
        if r:
            shots[shot].shot_length = r.group(1) + " yards"

        r = re.search(
            "<div class=\"distance\">.*?<span class=\"feet\">(\\d+)</span>.*?</div>", stuff)
        if r:
            shots[shot].shot_length = r.group(1) + " feet"

        r = re.search(
            "<div class=\"distance\">.*?<span class=\"inch\">(\\d+)</span>.*?</div>", stuff)
        if r:
            shots[shot].shot_length = r.group(1) + " inches"

        # Find distance to pin in yards, feet or inches
        r = re.search(
            "<div class=\"topin\">.*?<span>(\\d+)</span>.*?</div>", stuff)
        if r:
            shots[shot].distance_after = r.group(1) + " yards"

        r = re.search(
            "<div class=\"topin\">.*?<span class=\"feet\">(\\d+)</span>.*?</div>", stuff)
        if r:
            shots[shot].distance_after = r.group(1) + " feet"

        r = re.search(
            "<div class=\"topin\">.*?<span class=\"inch\">(\\d+)</span>.*?</div>", stuff)
        if r:
            shots[shot].distance_after = r.group(1) + " inches"

    # Turn dictionary into ordered list of shots
    shots = [shots[shot] for shot in sorted(shots, key=int)]

    # Set distance before:
    shots[0].distance_before = hole_length

    # Link up previous distances for other shots
    for i in range(1, len(shots)):
        shots[i].distance_before = shots[i-1].distance_after

    if categorize:
        # Read in the map
        reader = png.Reader(filename="maps/H%02dW.png" % (hole))
        w, _, pixels, metadata = reader.read_flat()

        pixel_byte_width = 4 if metadata['alpha'] else 3

        # Categorise the positions of the shots based on the map
        for shot in shots:
            pixel_position = shot.x + shot.y * w

            pixel = pixels[pixel_position *
                           pixel_byte_width: (pixel_position + 1) * pixel_byte_width]

            shot.category_after = get_category(pixel)

        shots[0].category_before = "tee"
        shots[len(shots) - 1].category_after = "hole"

        # Link up previous category for other shots
        for i in range(1, len(shots)):
            shots[i].category_before = shots[i-1].category_after

    return shots
