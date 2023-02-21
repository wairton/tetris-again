import random
import enum

import configuration.config as config
import color
import resource
import shapes

# TODO: normalize initialization parameters order

piece_colors = [
    color.BLACK, color.RED, color.ORANGE, color.YELLOW, color.GREEN,
    color.BLUE, color.INDIGO, color.LIGHT_BLUE
]


class Piece:
    def __init__(self, shape, color, position, initial_state):
        self._shape = shape
        self.state = initial_state
        self.color = color
        self.position = position

    def __str__(self):
        return 'Shape: {} {}'.format(self._shape[self.state], self.color)

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
        inc = -1 if clockwise else 1
        self.state = (self.state + inc) % len(self._shape)

    def get_block_coords(self):
        # FIXME: converting a 16-tuple into a 4 X 4 [list]
        # this is NOT the best approach
        shape = [self.shape[i:i + 4] for i in range(0, 13, 4)]
        sx, sy, ex, ey = 4, 4, 0, 0
        for line_index, line in enumerate(shape):
            for col_index, item in enumerate(line):
                if item == 0:
                    continue
                if line_index < sy:
                    sy = line_index
                if col_index < sx:
                    sx = col_index
                if line_index > ey:
                    ey = line_index
                if col_index > ex:
                    ex = col_index
        return sx, sy, ex, ey


class Block:
    def __init__(self, img_index):
        self.img_index = img_index

    def draw(self, drawer, position):
        drawer.blit(resource.BLOCKS_IMG[self.img_index].surface, position)


class Grid:
    def __init__(self, ncolumns, nlines, draw):
        self.active_pieces = []
        self.structure = [[0] * ncolumns for _ in range(nlines)]
        self.ncolumns = ncolumns
        self.nlines = nlines
        self.drawer = draw

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
        shape_pos = list(zip([(line + y, c + x) for line in range(4) for c in range(4)], shape))
        return [a[0] for a in [a for a in shape_pos if a[1] == 1]]

    def get_piece_positions(self, piece):
        return self._shape_to_positions(piece.shape, piece.position)

    def fill_piece_positions(self, blocks, value):
        for line, column in blocks:
            if line < 0 or column < 0:
                continue
            self.structure[line][column] = value

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
                for line in blocks:
                    if line[0] <= 0:
                        return True, True
                return True, False
            else:
                self.fill_piece_positions(next, piece.color)
                px, py = self.active_pieces[i].position
                self.active_pieces[i].position = px, py + 1
                return False, False

    def ground(self):
        collided, died = self.step()
        while not collided:
            collided, died = self.step()
        return collided, died

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
        block_size, block_pad = config.BLOCK_SIZE, config.BLOCK_PAD
        bsap = block_size + config.BLOCK_PAD
        preview_width = 4 * bsap
        preview_heigh = 12 * block_size + 8 * block_pad
        self.drawer.rect(color.BLACK, (ini_x, ini_y, preview_width, preview_heigh))
        ini_y += 2 * block_pad
        ini_x += 2 * block_pad
        for piece in pieces[:self.num_pieces]:
            shape_pos = list(zip([(c, line) for line in range(4) for c in range(4)], piece.shape))
            sx, sy, ex, ey = piece.get_block_coords()
            piece_width = (ex - sx) * bsap + block_size
            ppos = ini_x + (preview_width - piece_width) / 2
            for pos, block in shape_pos:
                if not block:
                    continue
                x, y = pos
                if block:
                    piece_color = piece.color
                self.draw_block(piece_color, (ppos + (x - sx) * block_size, ini_y + y * block_size))
            ini_y += 4 * block_size + 2 * block_pad

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
    class Action(enum.Enum):
        LEFT = enum.auto()
        RIGHT = enum.auto()
        ROTATE = enum.auto()
        GROUND = enum.auto()
        STEP = enum.auto()
        SCORE = enum.auto()

    def __init__(self, drawer, grid_position):
        self.grid = Grid(config.GRID_WIDTH, config.GRID_HEIGHT, drawer)
        self.preview = PiecePreview((350, 100), 3, drawer)
        drawer.fill(color.WHITE)
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

    def loop(self, action: Action):

        mapping = {
            GameScreen.Action.LEFT: self.grid.left,
            GameScreen.Action.RIGHT: self.grid.right,
            GameScreen.Action.ROTATE: self.grid.rotate,
            GameScreen.Action.GROUND: self.grid.ground,
            GameScreen.Action.STEP: self.grid.step,
        }

        collided, died = mapping[action]()
        self.grid.draw(self.grid_position)
        if died:
            return True, self.score.score
        if collided:
            lines = self.grid.check_complete_lines()
            if len(lines) > 0:
                self.grid.remove_lines(lines)
                self.score.update(len(lines))
            self.grid.add_piece(self.next_pieces.pop(0))
            self.next_pieces.append(self.generate_piece())
            self.preview.draw(self.next_pieces)
        return False, None
