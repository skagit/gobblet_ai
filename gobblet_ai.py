#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 16:04:26 2018

@author: matt
"""

import random

class Location:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        if self.row == other.row and self.column == other.column:
            return True
        else:
            return False

    def display(self):
        print( (self.row, self.column) )

class Piece:
    def __init__(self, color, size):
        self.color = color
        self.size = size
        self.position = Location("off", "off")

class Square:
    def __init__(self, location):
        self.stack = []
        self.location = location
        self.lines = []

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False

    def top(self):
        if not self.is_empty():
            return self.stack[-1]

    def color(self):
        if self.is_empty():
            return "none"
        else:
            return self.top().color

    def remove(self):
        if not self.is_empty():
            self.stack.pop()

    def add(self, piece):
        self.stack.append(piece)

class Board:
    rows = [ [ Location(i,j) for j in range(4) ] for i in range(4) ]
    columns = [ [ Location(i,j) for i in range(4) ] for j in range(4) ]
    left_diagonal = [ Location(i,i) for i in range(4) ]
    right_diagonal = [ Location(i, 3-i) for i in range(4) ]
    lines = [ *rows, *columns, left_diagonal, right_diagonal ]
    stack1_i = [0,3,6,9]
    stack2_i = [ n + 1 for n in stack1_i ]
    stack3_i = [ n + 1 for n in stack2_i ]

    def __init__(self):
        self.squares = []
        self.darks = []
        self.lights = []
        self.moves = []

        #Populate Pieces
        for color in ["dark", "light"]:
            for size in [3,2,1,0]:
                for repetition in range(3):
                    if color == "dark":
                        self.darks.append( Piece(color, size) )
                    else:
                        self.lights.append( Piece(color, size) )

        #Populate Squares
        for row_i in range(4):
            next_row = []
            for col_i in range(4):
                next_square = Square( Location(row_i, col_i) )
                for line in Board.lines:
                    if next_square.location in line:
                        next_square.lines.append(line)
                next_row.append( next_square )

            self.squares.append(next_row)


    def get_square(self, location):
        return self.squares[location.row][location.column]

    def get_off_piece(self, color):
        pieces = self.darks
        if color == "light":
            pieces = self.lights

        for piece in pieces:
            if piece.position == Location("off", "off"):
                return [piece]

        return piece


    def get_board_pieces(self, color):
        pieces = []
        for row in self.squares:
            for square in row:
                if square.color() == color:
                    pieces.append(square.top())
        return pieces

    def get_possible_pieces(self, color):
        return [ *self.get_off_piece(color), *self.get_board_pieces(color) ]

    def draw_piece_rowline(self, piece, row):
        size = piece.size
        color = piece.color
        icon = "." if color == "dark" else "#"
        shape = ""
        if row < (3 - size) or row > (3 + size):
            return " " * 7
        else:
            for _ in range(3 - size):
                shape += (" ")
            for _ in range( (size * 2) + 1):
                shape += (icon)
            for _ in range(3 - size):
                shape += (" ")
            return shape

    def draw_row(self, row):
        row_lines = ""
        for scan_line in range(7):
            row_lines += "|"
            for square in self.squares[row]:
                if not square.is_empty():
                    piece = square.top()
                    piece_shape = self.draw_piece_rowline(piece, scan_line)
                    row_lines += piece_shape + "|"
                else:
                    row_lines += " " * 7
                    row_lines += "|"
            row_lines += "\n"
        return row_lines

    def draw_offs(self, pieces):
        row_lines = ""
        for scan_line in range(7):
            row_lines += " " * 3
            for piece in pieces:
                if not piece == "done":
                    piece_shape = self.draw_piece_rowline(piece, scan_line)
                    row_lines += piece_shape + " " * 3
                else:
                    row_lines += " " * 7
                    row_lines += " " * 3
            row_lines += "\n"
        return row_lines

    def display(self):
        output = ""
        output += "|" + ("-" * ((7 * 4) + 3)) + "|" + "\n"
        for row in range(4):
            output += self.draw_row(row)
            output += "|" + ("-" * ((7 * 4) + 3)) + "|" + "\n"
        print(output)

    def count_line(self, locations):
        darks = 0
        lights = 0
        for location in locations:
            color = self.get_square(location).color()
            if color == "dark":
                darks += 1
            elif color == "light":
                lights += 1
        return (darks, lights)

    def has_winner(self):
        for line in Board.lines:
            (darks, lights) = self.count_line(line)
            if lights == 4:
                return (True, "light")
            elif darks == 4:
                return (True, "dark")
        return (False, "none")

    def score(self, color):
        count = 0
        for line in Board.lines:
            (darks, lights) = self.count_line(line)
            (own, other) = (darks, lights) if color == "dark" else (lights, darks)
            if own == 4:
                return 100
            elif other == 4:
                return -100
            elif other < 1:
                count += own
        return count

    def can_move(self, move):
        square = self.get_square(move.destination)
        piece = move.piece
        color = piece.color
        if square.is_empty():
            return True
        elif square.top().size < piece.size and piece.position != Location("off", "off"):
            return True
        elif square.top().size < piece.size and piece.position == Location("off", "off"):
            lines = square.lines
            triple = False
            for line in lines:
                (darks, lights) = self.count_line(line)
                if darks == 3 and color == "light":
                    triple = True
                elif lights == 3 and color == "dark":
                    triple = True
            return triple
        else:
            return False

    def get_moves(self, piece):
        possible_moves = []
        for row in self.squares:
            for square in row:
                next_move = Move(piece, piece.position, square.location)
                if self.can_move( next_move ):
                    possible_moves.append( next_move )
        return possible_moves

    def get_moves_all(self, color):
        possible_moves = []
        pieces = self.get_possible_pieces(color)
        for piece in pieces:
            next_moves = self.get_moves(piece)
            for next_move in next_moves:
                possible_moves.append(next_move)
        return possible_moves


    def make_move(self, move):
        self.get_square(move.destination).add(move.piece)

        if move.origin != Location("off", "off"):
            self.get_square(move.origin).remove()

        move.piece.position = move.destination

        self.moves.append(move)

    def undo_move(self):
        move = self.moves.pop()

        self.get_square(move.destination).remove()

        if move.origin != Location("off", "off"):
            self.get_square(move.origin).add(move.piece)

        move.piece.position = move.origin

class Move:
    def __init__(self, piece, origin, destination):
        self.piece = piece
        self.origin = origin
        self.destination = destination

class Node:
    def __init__(self, move):
        self.move = move
        self.score = "none"
        self.nexts = []

    def expand(self, color, board, n=2):
        if n > 0:
            board.make_move(self.move)
            self.score = board.score(color)
            if self.score == 100 or self.score == -100:
                pass
            else:
                next_color = "dark" if self.move.piece.color == "light" else "light"
                self.nexts = [ Node(move) for move in board.get_moves_all(next_color) ]
                for next_move in self.nexts:
                    next_move.expand(color, board, n-1)
            board.undo_move()
        else:
            board.make_move(self.move)
            self.score = board.score(color)
            board.undo_move()

    def collapse(self, color):
        if len(self.nexts) < 1:
            return self.score

        elif len(self.nexts) > 0:
            collapsed = [node.collapse(color) for node in self.nexts]
            if self.move.piece.color == color:
                return min(collapsed)
            else:
                return max(collapsed)

class Game:
    def __init__(self):
        self.board = Board()

    def get_move(self, color, board, n = 2):
        top_nodes = [ Node(move) for move in self.board.get_moves_all(color) ]
        for node in top_nodes:
            node.expand(color, board, n)
        collapsed = [node.collapse(color) for node in top_nodes]
        highest = max(collapsed)
        trimmed = [ (i, score) for i, score in enumerate(collapsed) if score == highest]
        choice = top_nodes[ random.choice(trimmed)[0] ]
        return choice.move

    def play_ai(self):
        while True:
            move = self.get_move("light", self.board, 2)
            print(move.piece.color + str(move.piece.size), (move.origin.row, move.origin.column), (move.destination.row, move.destination.column))
            self.board.make_move(move)
            self.board.display()
            print()
            win, side = self.board.has_winner()
            if win:
                print(side+" wins!")
                return
            move = self.get_move("dark", self.board, 2)
            print(move.piece.color + str(move.piece.size), (move.origin.row, move.origin.column), (move.destination.row, move.destination.column))
            self.board.make_move(move)
            self.board.display()
            print()
            win, side = self.board.has_winner()
            if win:
                print(side+" wins!")
                return

    def play(self):
        stack1 = [ self.board.lights[i] for i in Board.stack1_i ]
        stack2 = [ self.board.lights[i] for i in Board.stack2_i ]
        stack3 = [ self.board.lights[i] for i in Board.stack3_i ]

        last_op = "\n"

        self.board.display()

        while True:
            p1 = "done"
            p2 = "done"
            p3 = "done"

            for piece in stack1:
                if piece.position == Location("off", "off"):
                    p1 = piece
                    break

            for piece in stack2:
                if piece.position == Location("off", "off"):
                    p2 = piece
                    break

            for piece in stack3:
                if piece.position == Location("off", "off"):
                    p3 = piece
                    break

            p_stacks = [p1,p2,p3]

            print(last_op)
            print()
            print( self.board.draw_offs(p_stacks) )
            print()
            in_str = input("What is your move?: ")
            in_str = in_str.split(" ")
            destination = Location(int(in_str[2]), int(in_str[3]))
            origin = Location("off", "off")
            if in_str[0] != "off":
                origin = Location(int(in_str[0]), int(in_str[1]))

            piece = False
            if in_str[0] == "off":
                piece = p_stacks[int(in_str[1]) - 1]
            else:
                piece = self.board.squares[int(in_str[0])][int(in_str[1])].top()
            move = Move(piece, origin, destination)
            self.board.make_move(move)
            win, side = self.board.has_winner()
            if win:
                print(side+" wins!")
                return

            move = self.get_move("dark", self.board, 2)
            self.board.make_move(move)
            last_op = move.piece.color + str(move.piece.size), (move.origin.row, move.origin.column), (move.destination.row, move.destination.column)
            self.board.display()
            print()
            win, side = self.board.has_winner()
            if win:
                print(side+" wins!")
                return


g = Game()
g.play()
