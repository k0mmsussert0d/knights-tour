import pygame
import sys
from multiprocessing import Queue
from . import const


def visualize_journey(grid_size: int, event_queue: Queue = None):

    def get_optimal_tile_size(grid_size: int, initial_tile_size: int):
        info = pygame.display.Info()
        tile_size = initial_tile_size
        # make tiles smaller until all of them will fit into the screen
        while tile_size * grid_size > info.current_h or tile_size * grid_size > info.current_w:
            tile_size = int(tile_size * 0.75)

        return tile_size

    def window_init(grid_size: int):
        surface = pygame.display.set_mode(
            (grid_size * tile_size, grid_size * tile_size),
            flags=pygame.SCALED | pygame.RESIZABLE
        )
        pygame.display.set_caption('Knight\'s Tour Visualization')
        return surface

    def game_loop(surface, grid_size: int):
        poll_events = True
        draw_grid(surface, grid_size)
        while True:
            event = pygame.event.poll() if poll_events else pygame.event.wait()
            if event.type == pygame.NOEVENT:
                if event_queue is not None:
                    if event_queue.qsize() > 0:
                        new_event = event_queue.get()
                        if 'path' in new_event:
                            draw_grid(surface, grid_size)
                            draw_route(surface, new_event.get('path'))
                            pygame.time.wait(10)
                            if len(new_event.get('path')) == grid_size ** 2:
                                poll_events = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_f:
                    if event_queue is not None and event_queue.qsize() > 0:
                        draw_text_msg(surface, 'Discarding steps...')
                        pygame.display.update()
                        last_event = {}
                        while len(last_event.get('path', [])) != grid_size ** 2:  # retrieve the full path
                            last_event = event_queue.get()

                        draw_grid(surface, grid_size)
                        draw_route(surface, last_event.get('path', []))
                        poll_events = False

            pygame.display.update()

    def draw_grid(surface, grid_size: int):
        def get_color_for_tile(row: int, col: int):
            return const.COLOR_TILE_2 if (row + col) % 2 == 0 else const.COLOR_TILE_1

        for row in range(grid_size):
            for col in range(grid_size):
                tile = pygame.Rect(row * tile_size, col * tile_size, tile_size, tile_size)
                pygame.draw.rect(surface, get_color_for_tile(row, col), tile)

    def draw_route(surface, path: list):
        def draw_line(surface, start_tile, end_tile):
            def get_starting_cord(corner_cord):
                return corner_cord * tile_size + tile_size / 2

            start_pos = tuple(map(get_starting_cord, start_tile))
            end_pos = tuple(map(get_starting_cord, end_tile))
            pygame.draw.line(surface, const.COLOR_PATH_LINE, start_pos, end_pos, 5)

        for step1, step2 in zip(path[:-1], path[1:]):
            draw_line(surface, (step1.col, step1.row), (step2.col, step2.row))

    def draw_text_msg(surface: pygame.Surface, text: str):
        text_msg = pygame.font.SysFont('Cantarell', 30)
        text_surface = text_msg.render(text, False, const.COLOR_TEXT_MSG)
        surface.blit(text_surface, (0,0))

    pygame.display.init()
    pygame.font.init()
    tile_size = get_optimal_tile_size(grid_size, const.TILE_SIZE)
    surface = window_init(grid_size)
    game_loop(surface, grid_size)


if __name__ == '__main__':
    visualize_journey(20)
