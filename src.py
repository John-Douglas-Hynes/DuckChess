import copy

def dist(n, m):
    x1 = n % 8
    x2 = m % 8
    y1 = n//8
    y2 = m//8
    return (x1-x2)**2 + (y1-y2)**2

def piece_convert(s):
    if s == 0:
        return '0 '
    elif s == 7:
        return 'DU'
    elif s < 0:
        return chr(0x265F + s + 1)
    elif s > 0:
        return chr(0x2659 - s + 1)
    else:
        return None

class piece_move:
    def __init__(self, start, end, piece, capture = 0, ep = False, castle = False, promotion = None):
        self.piece = piece
        self.capture = capture
        self.en_passent = ep
        self.castle = castle
        self.start = start
        self.end = end
        self.promotion = promotion

    def __str__(self):
        letters = 'abcdefgh'
        promos = 'nbrq'
        start_row = str(8 - self.start//8)
        start_letter = letters[self.start % 8]
        end_row = str(8 - self.end//8)
        end_letter = letters[self.end % 8]
        extra = ''
        if self.promotion != None:
            extra = promos[self.promotion - 2]
        if self.castle:
            extra = ' (castles)'
        if self.en_passent:
            extra = ' (en passent)'
        return start_letter + start_row + end_letter + end_row + extra

    def __repr__(self):
        return [self.start, self.end, self.piece, self.capture, self.en_passent, self.castle, self.promotion]
    
    def __lt__(self, pmove):
        return (abs(self.capture) - abs(self.piece)) < (abs(pmove.capture) - abs(pmove.piece))
        

class chess_board:
    
    initial_position = [0 for i in range(64)]
    for i in range(8):
        initial_position[8+i] = -1
    for i in range(8):
        initial_position[48+i] = 1
    initial_position[57] = initial_position[62] = 2
    initial_position[6] = initial_position[1] = -2
    initial_position[58] = initial_position[61] = 3
    initial_position[2] = initial_position[5] = -3
    initial_position[56] = initial_position[63] = 4
    initial_position[0] = initial_position[7] = -4
    initial_position[59] = 5
    initial_position[3] = -5
    initial_position[60] = 6
    initial_position[4] = -6
    
    def __init__(self, board_position = initial_position, bQ = True, bK = True, wQ = True, wK = True, ep = None, to_play = 1):
        self.squares = board_position
        self.b_can_castleQ = bQ
        self.b_can_castleK = bK
        self.w_can_castleQ = wQ
        self.w_can_castleK = wK
        self.en_passent = ep
        self.to_play = to_play
        self.history = []
        
    def print_board(self):
        board = []
        for i in range(8):
            for j in range(8):
                print(' ' + piece_convert(self.squares[8*i + j])+' ',end = ' ')
            print('\n')
            
    def move_a_piece(self, pmove):
        #check for castling:
        if pmove.castle:
            self.squares[pmove.end] = self.squares[pmove.start]
            self.squares[pmove.start] = 0
            if self.to_play == -1:
                if pmove.end == 2:
                    self.squares[3] = -4
                    self.squares[0] = 0
                else:
                    self.squares[5] = -4
                    self.squares[7] = 0
            else:
                if pmove.end == 62:
                    self.squares[61] = 4
                    self.squares[63] = 0
                else:
                    self.squares[59] = 4
                    self.squares[56] = 0
        #check for pawn promotion:
        elif pmove.promotion != None:
            self.squares[pmove.end] = pmove.promotion
            self.squares[pmove.start] = 0
        #check for en passent:
        elif pmove.en_passent:
            self.squares[pmove.end] = self.squares[pmove.start]
            self.squares[pmove.start] = 0
            self.squares[self.en_passent] = 0
        #normal moves:
        else:
            self.squares[pmove.end] = self.squares[pmove.start]
            self.squares[pmove.start] = 0
            
        #if the king or rook has moved, remove castling rights:
        if pmove.piece == -6:
            self.b_can_castleQ = self.b_can_castleK = False
        elif pmove.piece == 6:
            self.w_can_castleQ = self.w_can_castleK = False
        elif pmove.start == 0:
            self.b_can_castleQ = False
        elif pmove.start == 7:
            self.b_can_castleK = False
        elif pmove.start == 56:
            self.w_can_castleQ = False
        elif pmove.start == 63:
            self.w_can_castleK = False
            
        #if a pawn moved two squares, make an en passent flag. Otherwise, remove en passent
        if pmove.piece == 1 and dist(pmove.start, pmove.end) == 4:
            self.en_passent = pmove.end
        else:
            self.en_passent = None
        
    def move_duck(self, dmove):
        for i in range(64):
            if self.squares[i] == 7:
                self.squares[i] = 0
        self.squares[dmove] = 7

    def increment_turn(self):
        self.to_play = self.to_play*(-1)
        cop = copy.deepcopy(self.squares)
        self.history.append(cop)

    def undo_turn(self):
        pass

    def legal_down_moves(self, pos, colour):
        moves = []
        while pos < 56:
            pos += 8
            if self.squares[pos] == 0:
                moves.append(pos)        
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_up_moves(self, pos, colour):
        moves = []
        while pos > 7:
            pos -= 8
            if self.squares[pos] == 0:
                moves.append(pos)        
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_right_moves(self, pos, colour):
        moves = []
        while pos % 8 < 7:
            pos += 1
            if self.squares[pos] == 0:
                moves.append(pos)        
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_left_moves(self, pos, colour):
        moves = []
        while pos % 8 > 0:
            pos -= 1
            if self.squares[pos] == 0:
                moves.append(pos)        
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_upright_moves(self, pos, colour):
        moves = []
        while pos > 7 and pos % 8 < 7:
            pos -= 7
            if self.squares[pos] == 0:
                moves.append(pos)
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_upleft_moves(self, pos, colour):
        moves = []
        while pos > 7 and pos % 8 > 0:
            pos -= 9
            if self.squares[pos] == 0:
                moves.append(pos)
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_downright_moves(self, pos, colour):
        moves = []
        while pos < 56 and pos % 8 < 7:
            pos += 9
            if self.squares[pos] == 0:
                moves.append(pos)
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_downleft_moves(self, pos, colour):
        moves = []
        while pos < 56 and pos % 8 > 0:
            pos += 7
            if self.squares[pos] == 0:
                moves.append(pos)
            elif abs(self.squares[pos] - colour) > abs(self.squares[pos]) and self.squares[pos] != 7:
                moves.append(pos)
                break
            else:
                break
        return moves

    def legal_pawn_moves(self, pos, colour):
        moves = []
        #white promotions:
        if pos < 16 and colour == 1:
            forward = pos - 8
            diags = [pos -7, pos - 9]
            if self.squares[forward] == 0:
                for i in range(2, 6):
                    moves.append(piece_move(start = pos, end = forward, piece = self.squares[pos], promotion = i))
            for d in diags:
                if d >= 0:
                    if self.squares[d] < 0 and dist(pos, d) == 2:
                        for i in range(2, 6):
                            moves.append(piece_move(start = pos, end = d, piece = self.squares[pos], promotion = i, capture = self.squares[d]))
        #black promotions:
        elif pos >= 48 and colour == -1:
            forward = pos + 8
            diags = [pos +7, pos + 9]
            if self.squares[forward] == 0:
                for i in range(2, 6):
                    moves.append(piece_move(start = pos, end = forward, piece = self.squares[pos], promotion = i))
            for d in diags:
                if d < 64:
                    if 7 > self.squares[d] > 1 and dist(pos, d) == 2:
                        for i in range(2, 6):
                            moves.append(piece_move(start = pos, end = d, piece = self.squares[pos], promotion = i, capture = self.squares[d]))
        #regular and double moves forward:
        else:
            forward = pos - colour*8
            if self.squares[forward] == 0:
                moves.append(piece_move(start = pos, end = forward, piece = self.squares[pos]))
                if colour == -1:
                    if pos > 7 and pos < 16:
                        forward2 = forward + 8
                        if self.squares[forward2] == 0:
                            moves.append(piece_move(start = pos, end = forward2, piece = self.squares[pos]))
                if colour == 1:
                    if pos > 47 and pos < 56:
                        forward2 = forward - 8
                        if self.squares[forward2] == 0:
                            moves.append(piece_move(start = pos, end = forward2, piece = self.squares[pos]))
        #diagonal capturing moves:
            diag1 = pos - 8*colour - 1
            diag2 = pos - 8*colour + 1
            diags = [diag1, diag2]
            for d in diags:
                if self.squares[d]*colour < 0 and self.squares[d] != 7 and dist(pos, d) == 2:
                    moves.append(piece_move(start = pos, end = d, piece = self.squares[pos], capture = self.squares[d]))
        #en passent nonsense:
            LR_possibly = [pos-1, pos+1]
            LR = [i for i in LR_possibly if dist(i, pos) == 1]
            if self.en_passent in LR:
                target = self.en_passent - colour*8
                if self.squares[target] != 7:
                    moves.append(piece_move(start = pos, end = target, piece = self.squares[pos], capture = -colour, ep = True))
        return moves

    def legal_knight_moves(self, pos, colour):
        candidates = [pos+15, pos+17, pos-15, pos-17, pos+10, pos+6, pos-10, pos-6]
        moves = []
        for i in candidates:
            if 0 <= i and i < 64 and dist(i, pos) <= 5:
                if self.squares[i] == 0:
                    moves.append(piece_move(start = pos, end = i, piece = self.squares[pos]))
                elif self.squares[i]*colour < 0 and self.squares[i] != 7:
                    moves.append(piece_move(start = pos, end = i, piece = self.squares[pos], capture = self.squares[i]))
        return moves

    def legal_bishop_moves(self, pos, colour):
        moves = []
        ends = self.legal_upright_moves(pos, colour) + self.legal_upleft_moves(pos, colour)+self.legal_downright_moves(pos, colour)+self.legal_downleft_moves(pos, colour)
        for e in ends:
                moves.append(piece_move(start = pos, end = e, piece = 3, capture = self.squares[e]))
        return moves

    def legal_rook_moves(self, pos, colour):
        moves = []
        ends = self.legal_up_moves(pos, colour) + self.legal_down_moves(pos, colour) + self.legal_right_moves(pos, colour) + self.legal_left_moves(pos, colour)
        for e in ends:
                moves.append(piece_move(start = pos, end = e, piece = self.squares[pos], capture = self.squares[e]))
        return moves

    def legal_queen_moves(self, pos, colour):
        moves = []
        ends = self.legal_upright_moves(pos, colour)+self.legal_upleft_moves(pos, colour)+self.legal_downright_moves(pos, colour)+self.legal_downleft_moves(pos, colour) + self.legal_up_moves(pos, colour) + self.legal_down_moves(pos, colour) + self.legal_right_moves(pos, colour) + self.legal_left_moves(pos, colour)
        for e in ends:
            moves.append(piece_move(start = pos, end = e, piece = self.squares[pos], capture = self.squares[e]))
        return moves
    
    def legal_king_moves(self, pos, colour):
        #normal king moves:
        moves = []
        candidates = [pos + 1, pos -1, pos + 8, pos - 8, pos +7, pos - 7, pos +9,pos - 9]
        for i in candidates:
            if 0 <= i and i < 64 and dist(i, pos) <= 1 and (abs(self.squares[i] - colour) > abs(self.squares[i])) and self.squares[i] != 7:
                moves.append(piece_move(start = pos, end = i, piece = self.squares[pos], capture = self.squares[i]))
        #castling moves:
        if colour == -1:
            if self.b_can_castleK:
                if all(self.squares[i] == 0 for i in range(5, 7)):
                    moves.append(piece_move(start = pos, end = 6, piece = -6, castle = True))
            if self.b_can_castleQ:
                if all(self.squares[i] == 0 for i in range(1, 4)):
                    moves.append(piece_move(start = pos, end = 2, piece = -6, castle = True))
        if colour == 1:
            if self.w_can_castleK:
                if all(self.squares[i] == 0 for i in range(61,63)):
                    moves.append(piece_move(start = pos, end = 62, piece = 6, castle = True))
            if self.w_can_castleQ:
                if all(self.squares[i] == 0 for i in range(57, 60)):
                    moves.append(piece_move(start = pos, end = 58, piece = 6, castle = True))
        return moves

    def legal_duck_moves(self):
        return [i for i in range(64) if self.squares[i] == 0]

    def generate_legal_moves(self):
        moves = []
        for i in range(64):
            if self.squares[i]*self.to_play == 1:
                moves += self.legal_pawn_moves(i, self.to_play)
            elif self.squares[i]*self.to_play == 2:
                moves += self.legal_knight_moves(i, self.to_play)
            elif self.squares[i]*self.to_play == 3:
                moves += self.legal_bishop_moves(i, self.to_play)
            elif self.squares[i]*self.to_play == 4:
                moves += self.legal_rook_moves(i, self.to_play)
            elif self.squares[i]*self.to_play == 5:
                moves += self.legal_queen_moves(i, self.to_play)
            elif self.squares[i]*self.to_play == 6:
                moves += self.legal_king_moves(i, self.to_play)
        return sorted(moves)

    def result(self):
        if not(6 in self.squares):
            return -1
        elif not(-6 in self.squares):
            return 1
        if len(self.generate_legal_moves()) == 0:
            return self.to_play
        repetitions = 0
        for i in self.history:
            if self.squares == i:
                repetitions += 1
        if repetitions > 2:
            return 0
        else:
            return None