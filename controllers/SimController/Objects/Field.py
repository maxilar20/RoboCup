class Field:
    def __init__(self, boundaries):
        self.boundaries = boundaries

    def isInside(self, pos, field="field"):
        boundary = self.boundaries[field]
        return (
            pos.x > boundary[0].x
            and pos.x < boundary[1].x
            and pos.y < boundary[0].y
            and pos.y > boundary[1].y
        )
