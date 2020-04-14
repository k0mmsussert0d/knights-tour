from board_graph import Graph
from field import Field
from gui.gui import visualize_journey
from multiprocessing import Process, Queue


def find_path(
        board: Graph, start_field: Field = Field(0, 0),
        heuristic=lambda x: x, events_queue: Queue = None
):
    total_squares = board.board_size ** 2

    def first_true(sequence):
        """Return the first true value in the sequence.
        If no true value is found, returns None.
        """
        return next(filter(None, sequence), None)

    def field_number(field: Field):
        return field.row * board.board_size + 1 + field.col

    def traverse(path: list, current_field: Field):
        if events_queue:
            events_queue.put({'path': path})

        if len(path) + 1 == total_squares:  # end of a journey, all fields visited
            path.append(current_field)
            if events_queue:
                events_queue.close()
            return path

        available_fields = board.get_node(current_field).moves - set(path)
        if not available_fields:  # dead end, backtrack
            return False

        next_fields = sorted(available_fields, key=heuristic)
        return first_true(traverse(path + [current_field], field) for field in next_fields)

    return traverse([], start_field)
