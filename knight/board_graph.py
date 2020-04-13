from typing import Generator

from field_node import FieldNode
from field import Field


class Graph:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.graph = list()
        for row in range(board_size):
            for col in range(board_size):
                new_node = FieldNode(row, col)
                for move in self.get_legal_moves(new_node.field):
                    new_node.moves.add(move)
                self.graph.append(new_node)

    def get_legal_moves(self, field: Field) -> Generator[Field, None, None]:
        legal_moves = (
            (2, -1), (2, 1),
            (1, 2), (-1, 2),
            (-2, 1), (-2, -1),
            (-1, -2), (1, -2)
        )

        for hor_offset, ver_offset in legal_moves:
            hor_move = field.col + hor_offset
            ver_move = field.row + ver_offset
            if 0 <= hor_move < self.board_size and 0 <= ver_move < self.board_size:
                yield Field(ver_move, hor_move)

    def get_node(self, field: Field) -> FieldNode:
        for node in self.graph:
            if node.field == field:
                return node
        return NotImplemented
