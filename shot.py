class Shot:

    def __init__(self):
        self.distance_before = None
        self.distance_after = None
        self.shot_length = None
        self.category_before = None
        self.category_after = None
        self.x = None
        self.y = None
        self.player = None
        self.round = None
        self.shot = None
        self.par = None
        self.hole = None

    def csv_dump(self):
        return [self.player,
                self.shot,
                self.round,
                self.par,
                self.hole,
                self.distance_before,
                self.distance_after,
                self.shot_length,
                self.category_before,
                self.category_after,
                self.x,
                self.y]

    def __str__(self):
        return "Shot <" + \
            "player=" + str(self.player) + \
            ",shot=" + str(self.shot) + \
            ",round=" + str(self.round) + \
            ",par=" + str(self.par) + \
            ",hole=" + str(self.hole) + \
            ",distance_before=" + str(self.distance_before) + \
            ",distance_after=" + str(self.distance_after) + \
            ",shot_length=" + str(self.shot_length) + \
            ",category_before=" + str(self.category_before) + \
            ",category_after=" + str(self.category_after) + \
            ",x=" + str(self.x) + \
            ",y=" + str(self.y) + \
            ">"
