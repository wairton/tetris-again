import random

import config
import color
import resource
import shapes

# TODO: normalize initialization parameters order

piece_colors = [
    color.BLACK, color.RED, color.ORANGE, color.YELLOW, color.GREEN,
    color.BLUE, color.INDIGO, color.LIGHT_BLUE
]

border_colors = [
    (200, 200, 200), color.DARK_RED, color.DARK_ORANGE, color.DARK_YELLOW,
    color.DARK_GREEN, color.DARK_BLUE, color.DARK_INDIGO, color.DARK_LIGHT_BLUE
]


class Piece:
    def __init__(self, shape, color, position, initial_state):
        self._shape = shape
        self.state = initial_state
        self.color = color
        self.position = position

    def __str__(self):
        return 'Shape: ' + str(self._shape[self.state]) + ' ' + str(self.color)

    @property
    def shape(self):
        return self._shape[self.state]

    def next_rotate(self, clockwise=True):
        """
        return the shape of a next rotation
        """
        if clockwise:
            return self._shape[self.state - 1]
        return self._shape[(self.state + 1) % len(self._shape)]

    def rotate(self, clockwise=True):
        if clockwise:
            if self.state > 0:
                self.state -= 1
            else:
                self.state = len(self._shape) - 1
        else:
            self.state = (self.state + 1) % len(self._shape)


class Block:
    def __init__(self, img_index):
        self.img_index = img_index

    def draw(self, drawer, position):
        drawer.blit(resource.BLOCKS_IMG[self.img_index], position)


class Grid:
    def __init__(self, ncolumns, nlines, draw, valid_colors):
        self.active_pieces = []
        # historical bug! don't remove this commented line by now...
        # self.structure = [[0] * ncolumns] * nlines
        self.structure = [[0 for _ in range(ncolumns)] for _ in range(nlines)]
        self.ncolumns = ncolumns
        self.nlines = nlines
        self.drawer = draw
        self.valid_colors = valid_colors

    def filled(self, color):
        for i, line in enumerate(self.structure):
            for j, col in enumerate(line):
                self.structure[i][j] = color

    def draw(self, position):
        ini_x, ini_y = position
        block_size = config.BLOCK_SIZE
        block_size_and_pad = block_size + config.BLOCK_PAD
        for i, line in enumerate(self.structure):
            for j, c in enumerate(line):
                self.draw_block(
                    c, (ini_x + j * block_size_and_pad, ini_y + i * block_size_and_pad))

    def draw_block(self, color, position):
        block = Block(color)
        block.draw(self.drawer, position)

    def add_piece(self, piece):
        self.active_pieces.append(piece)

    def pop_piece(self):
        self.active_pieces.pop(0)

    def _shape_to_positions(self, shape, base_position):
        x, y = base_position
        shape_pos = list(zip([(l + y, c + x) for l in range(4) for c in range(4)], shape))
        return [a[0] for a in [a for a in shape_pos if a[1] == 1]]

    def get_piece_positions(self, piece):
        return self._shape_to_positions(piece.shape, piece.position)

    def fill_piece_positions(self, blocks, value):
        for linha, coluna in blocks:
            if linha < 0 or coluna < 0:
                continue
            self.structure[linha][coluna] = value

    def try_piece_rotate(self, piece):
        rotated_shape = piece.next_rotate()
        rotated_positions = self._shape_to_positions(rotated_shape, piece.position)
        if self.verify_collision(rotated_positions):
            return None
        return rotated_positions

    def try_piece_down(self, positions):
        """
        if True, returns the next positions, otherwise returns None
        """
        next = positions[:]
        for i in range(len(next)):
            next[i] = next[i][0] + 1, next[i][1]
        if self.verify_collision(next):
            return None
        return next

    def try_piece_right(self, positions):
        """
        if True, returns the next positions, otherwise returns None
        """
        next = positions[:]
        for i in range(len(next)):
            next[i] = next[i][0], next[i][1] + 1
        if self.verify_collision(next):
            return None
        return next

    def try_piece_left(self, positions):
        """
        if True, returns the next positions, otherwise returns None
        """
        next = positions[:]
        for i in range(len(next)):
            next[i] = next[i][0], next[i][1] - 1
        if self.verify_collision(next):
            return None
        return next

    def verify_collision(self, positions):
        for line, column in positions:
            if line < 0 or line > self.nlines:
                continue
            if column >= self.ncolumns:  # right
                return True
            if column < 0:  # left
                return True
            if line == self.nlines or self.structure[line][column] != 0:
                return True
        return False

    def step(self):
        for i, piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.try_piece_down(blocks)
            if next is None:
                self.fill_piece_positions(blocks, piece.color)
                self.pop_piece()
                for l, c in blocks:
                    if l <= 0:
                        return True, True
                return True, False
            else:
                self.fill_piece_positions(next, piece.color)
                px, py = self.active_pieces[i].position
                self.active_pieces[i].position = px, py + 1
                return False, False

    def ground(self):
        colidiu, died = self.step()
        while not colidiu:
            colidiu, died = self.step()
        return colidiu, died

    def rotate(self):
        for i, piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.try_piece_rotate(piece)
            if next is None:
                self.fill_piece_positions(blocks, piece.color)
            else:
                self.fill_piece_positions(next, piece.color)
                self.active_pieces[i].rotate()
            return False, False

    def left(self):
        for i, piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.try_piece_left(blocks)
            if next is None:
                self.fill_piece_positions(blocks, piece.color)
            else:
                self.fill_piece_positions(next, piece.color)
                px, py = self.active_pieces[i].position
                self.active_pieces[i].position = px - 1, py
            return False, False

    def right(self):
        for i, piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.try_piece_right(blocks)
            if next is None:
                self.fill_piece_positions(blocks, piece.color)
            else:
                self.fill_piece_positions(next, piece.color)
                px, py = self.active_pieces[i].position
                self.active_pieces[i].position = px + 1, py
            return False, False

    def remove_lines(self, lines):
        for i in lines:
            self.structure.pop(i)
            self.structure.insert(0, [0] * 10)

    def check_complete_lines(self):
        lines = []
        for i, line in enumerate(self.structure):
            if 0 not in line:
                lines.append(i)
        return lines


class PiecePreview:
    def __init__(self, position, num_pieces, drawer):
        self.position = position
        self.num_pieces = num_pieces
        self.drawer = drawer

    def draw(self, pieces):
        ini_x, ini_y = self.position
        block_size = config.BLOCK_SIZE
        block_size_and_pad = block_size + config.BLOCK_PAD
        bsap = block_size_and_pad
        print("-" * 20)
        for piece in pieces[:self.num_pieces]:
            shape_pos = list(zip([(l, c) for l in range(4) for c in range(4)], piece.shape))
            for pos, block in shape_pos:
                print(pos, block)
                x, y = pos
                color = 0
                if block:
                    color = piece.color
                self.draw_block(color, (ini_x + x * bsap, ini_y + y * bsap))
            ini_y += 100

    def draw_block(self, color, position):
        block = Block(color)
        block.draw(self.drawer, position)


class Score:
    def __init__(self, drawer, grid_position, show_score=True, show_lines=True):
        self.position = grid_position
        self.line_score = config.LINE_VALUE  # default value
        self.score = 0
        self.lines = 0
        self.show_score = show_score
        self.show_lines = show_lines
        self.font = resource.GAME_FONT
        self.drawer = drawer

    def update(self, num_lines=0):
        self.lines += num_lines
        if num_lines > 0:
            self.score += self.line_score[num_lines - 1]
        self.draw()

    def draw(self):
        x, y = self.position
        self.drawer.rect(color.BLACK, (x, y, 150, 100))
        text = self.font.render("lines: %s" % self.lines, 1, color.WHITE2)
        self.drawer.blit(text, (x, y))
        text = self.font.render("score: %s" % self.score, 1, color.WHITE2)
        self.drawer.blit(text, (x, y + 50))


class GameScreen:
    def __init__(self, drawer, grid_position):
        self.grid = Grid(
            config.GRID_WIDTH, config.GRID_HEIGHT, drawer, piece_colors)
        self.preview = PiecePreview((350, 100), 3, drawer)
        drawer.fill(color.BEATIFUL_BLUE)
        self.grid.draw(grid_position)
        self.grid_position = grid_position
        # we humans don't like real randomness...
        self.color_choices = list(range(1, len(piece_colors)))
        random.shuffle(self.color_choices)
        drawer.display()
        self.drawer = drawer
        # TODO: remove the hard-coded value in the next line!
        self.next_pieces = [self.generate_piece() for _ in range(6)]
        self.grid.add_piece(self.next_pieces.pop(0))
        self.preview.draw(self.next_pieces)
        self.score = Score(self.drawer, (300, 450))
        self.score.update()

    def generate_piece(self):
        if len(self.color_choices) == 0:
            self.color_choices = list(range(1, len(piece_colors)))
            random.shuffle(self.color_choices)
        new_shape = random.choice(shapes.ALL_SHAPES)
        new_color = self.color_choices.pop()
        initial_position = random.randint(0, len(new_shape) - 1)
        return Piece(new_shape, new_color, (3, -4), initial_position)

    def loop(self, action=None):
        if action == 'left':
            collided, died = self.grid.left()
        elif action == 'right':
            collided, died = self.grid.right()
        elif action == 'rotate':
            collided, died = self.grid.rotate()
        elif action == 'ground':
            collided, died = self.grid.ground()
        else:
            collided, died = self.grid.step()
        self.grid.draw(self.grid_position)
        if died:
            return True
        if collided:
            lines = self.grid.check_complete_lines()
            if len(lines) > 0:
                self.grid.remove_lines(lines)
                self.score.update(len(lines))
            self.grid.add_piece(self.next_pieces.pop(0))
            self.next_pieces.append(self.generate_piece())
            self.preview.draw(self.next_pieces)
        return False
