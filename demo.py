from knight.knight import find_path
from knight.board_graph import Graph
from knight.field import Field
from gui.gui import visualize_journey
from multiprocessing import Process, Queue
from typing import Callable


def knights_tour(
        board_size: int, start_row: int = 0, start_col: int = 0,
        visualize: bool = False, heuristic_override: Callable = None
):
    """
    @param board_size: size of a chess board
    @param start_row: row of a starting point square
    @param start_col: column of a starting point square
    @param visualize: display graphic representation of search process using pygame library
    @param heuristic_override: comparator function used to determine which routes (squares) should be checked first
    @return:
    """
    board = Graph(board_size)
    if visualize:
        q = Queue()
        visualization = Process(target=visualize_journey, args=(board_size, (q),))
        visualization.daemon = True
        visualization.start()
    else:
        q = None

    def warnsdorrfs(x):
        return len(board.get_node(x).moves)

    heuristic_func = heuristic_override if heuristic_override is not None else warnsdorrfs
    res = find_path(board, start_field=Field(start_row, start_col),heuristic=heuristic_func, events_queue=q)

    if visualize:
        visualization.join()

    return res


if __name__ == '__main__':
    # find path on 8-size chess board, starting from square (0, 0), visualize the process
    print(knights_tour(8, 0, 0, True))
