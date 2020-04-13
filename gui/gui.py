import pygame
import sys

import events
import const


def visualize_journey(grid_size: int):

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
        draw_grid(surface, grid_size)
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == events.UPDATE:
                draw_route(surface, event.route)

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
            draw_line(surface, (step1.row, step1.col), (step2.row, step2.col))

    pygame.display.init()
    tile_size = get_optimal_tile_size(grid_size, const.TILE_SIZE)
    surface = window_init(grid_size)
    game_loop(surface, grid_size)


if __name__ == '__main__':
    visualize_journey(20)
