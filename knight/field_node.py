from .field import Field


class FieldNode:
    def __init__(self, row: int, col: int):
        self.field = Field(row, col)
        self.moves = set()
