import random

import config
import color
import shapes

piece_colors = [color.BLACK, color.RED, color.ORANGE, color.YELLOW, color.GREEN, 
                color.BLUE, color.INDIGO, color.LIGHT_BLUE]
border_colors = [(200,200,200), color.DARK_RED, color.DARK_ORANGE, color.DARK_YELLOW, 
                color.DARK_GREEN, color.DARK_BLUE, color.DARK_INDIGO, color.DARK_LIGHT_BLUE]

class Piece(object):
    def __init__(self, shape, color, position, initial_state):
        self._shape = shape
        self.state = initial_state
        self.color = color
        self.position = position

    def __str__(self):
        return 'Shape: ' + str(self.shape[self.state]) + str(self.color)
    
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


class Block(object):
    def __init__(self, color, border_color):
        self.color = color
        self.border_color = border_color

    def draw(self, drawer, position):
        block_size = config.BLOCK_SIZE
        x, y = position
        rect = x, y, block_size, block_size
        drawer.rect(self.color, rect)
        drawer.line(self.border_color, (x,y),(x, y + block_size), 2)
        drawer.line(self.border_color, (x + block_size,y), 
                    (x + block_size, y + block_size), 2)
        drawer.line(self.border_color, (x,y),(x + block_size, y), 2)
        drawer.line(self.border_color, (x,y + block_size),(x + block_size, y + block_size), 2)


class Grid(object):
    def __init__(self, ncolumns, nlines, draw, valid_colors):
        self.active_pieces = []
        #self.structure = [[0] * ncolumns] * nlines
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
            for j, color in enumerate(line):
                self.draw_block(color, (ini_x + j * block_size_and_pad, 
                                            ini_y + i * block_size_and_pad))

    def draw_block(self, color, position):
        block = Block(piece_colors[color], border_colors[color])
        block.draw(self.drawer, position)
        
    def add_piece(self, piece):
        print piece
        self.active_pieces.append(piece)

    def pop_piece(self):
        self.active_pieces.pop(0)

    def _shape_to_positions(self, shape, base_position):
        print base_position, shape
        x, y = base_position 
        shape_pos = zip([(l+y,c+x) for l in range(4) for c in range(4)], shape)
        return map(lambda a:a[0],filter(lambda a:a[1] == 1, shape_pos))

    def get_piece_positions(self, piece):
        return self._shape_to_positions(piece.shape, piece.position)
                        
    def fill_piece_positions(self, blocks, value):
        for linha, coluna in blocks:
            if linha < 0 or coluna < 0:
                continue
            self.structure[linha][coluna] = value
    
    def can_piece_rotate(self, piece):
        rotated_shape = piece.next_rotate()
        print '@', rotated_shape
        rotated_positions = self._shape_to_positions(rotated_shape, piece.position)
        if self.verify_collision(rotated_positions):
            return None
        return rotated_positions
        
        
    def can_piece_down(self, positions):
        """
        if True, returns the next positions, otherwise returns None
        """
        next = positions[:]
        for i in xrange(len(next)):
            next[i] = next[i][0]+1, next[i][1]
        if self.verify_collision(next):
            return None
        return next
    
    def can_piece_right(self, positions):
        """
        if True, returns the next positions, otherwise returns None
        """
        next = positions[:]
        for i in xrange(len(next)):
            next[i] = next[i][0], next[i][1]+1
        if self.verify_collision(next):
            return None
        return next
    
    def can_piece_left(self, positions):
        """
        if True, returns the next positions, otherwise returns None
        """
        next = positions[:]
        for i in xrange(len(next)):
            next[i] = next[i][0], next[i][1]-1
        if self.verify_collision(next):
            return None
        return next
    
    def verify_collision(self, positions):
        for line, column in positions:
            if line < 0 or line > self.nlines:
                continue
            if column >= self.ncolumns: #right
                return True
            if column < 0: #left
                return True
            if line == self.nlines or self.structure[line][column] != 0:
                return True
        return False
                
    def step(self):
        for i,piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.can_piece_down(blocks)
            if next == None:
                self.fill_piece_positions(blocks, piece.color)
                self.pop_piece()
                for l,c in blocks:
                    if l <= 0:
                        return True, True
                return True, False
            else:
                self.fill_piece_positions( next, piece.color)
                px, py = self.active_pieces[i].position
                self.active_pieces[i].position = px, py+1
                return False, False
    
    def rotate(self):
        for i,piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.can_piece_rotate(piece)
            print '@', blocks, next
            if next == None:
                self.fill_piece_positions(blocks, piece.color)
            else:
                self.fill_piece_positions( next, piece.color)
                self.active_pieces[i].rotate()
            return False, False

    def left(self):
        for i,piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.can_piece_left(blocks)
            if next == None:
                self.fill_piece_positions(blocks, piece.color)
            else:
                self.fill_piece_positions( next, piece.color)
                px, py = self.active_pieces[i].position
                self.active_pieces[i].position = px-1, py
            return False, False
    
    def right(self):
        for i,piece in enumerate(self.active_pieces):
            blocks = self.get_piece_positions(piece)
            self.fill_piece_positions(blocks, 0)
            next = self.can_piece_right(blocks)
            if next == None:
                self.fill_piece_positions(blocks, piece.color)
            else:
                self.fill_piece_positions( next, piece.color)
                px, py = self.active_pieces[i].position
                self.active_pieces[i].position = px+1, py
            return False, False
    
    def remove_lines(self, lines):
        for i in lines:
            self.structure.pop(i)
            self.structure.insert(0,[0] * 10)
    
    def check_complete_lines(self):
        lines = []
        for i,line in enumerate(self.structure):
            if not 0 in line:
                lines.append(i)
        return lines
        
class GameScreen(object):
    def __init__(self, drawer, grid_position):
        self.grid = Grid(config.GRID_WIDTH, config.GRID_HEIGHT, drawer, piece_colors)
        #self.grid.filled(0)
        drawer.fill((121,159,190))
        self.grid.draw(grid_position)
        self.grid_position = grid_position
        drawer.display()
        self.drawer = drawer
        self.grid.add_piece(self.generate_piece())
        
    def generate_piece(self):
        new_shape = random.choice(shapes.ALL_SHAPES)
        new_color = random.randint(1,len(piece_colors)-1)
        initial_position = random.randint(0,len(new_shape)-1)
        return Piece(new_shape, new_color, (3,-4), initial_position)
        
    def loop(self, action=None):
        if action == 'left':
            colide, morreu = self.grid.left()
        elif action == 'right':
            colide, morreu = self.grid.right()
        elif action == 'rotate':
            colide, morreu = self.grid.rotate()
        else:    
            colide, morreu = self.grid.step()
        self.grid.draw(self.grid_position)
        #time.sleep(0.1)
        if morreu:
            return True
        if colide:
            lines = self.grid.check_complete_lines()
            if len(lines) > 0:
                self.grid.remove_lines(lines)
            self.grid.add_piece(self.generate_piece())
        return False
