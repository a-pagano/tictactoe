#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tictactoe.tictactoe import create_3d_grid, has_won


def test_has_won_full_row():
    board = create_3d_grid(3)
    assert has_won(board, 1) is False
    board[0][0] = [1, 1, 1]
    assert has_won(board, 1) is True


def test_has_won_full_column():
    board = create_3d_grid(3)
    assert has_won(board, 1) is False
    board[0][0] = [1, 0, 0]
    board[0][1] = [1, 0, 0]
    board[0][2] = [1, 0, 0]
    assert has_won(board, 1) is True


def test_has_won_2d_diagonal():
    board = create_3d_grid(3)
    assert has_won(board, 1) is False
    board[0][0] = [1, 0, 0]
    board[0][1] = [0, 1, 0]
    board[0][2] = [0, 0, 1]
    assert has_won(board, 1) is True


def test_has_won_3d_diagonal():
    board = create_3d_grid(3)
    assert has_won(board, 1) is False
    board[0][0] = [1, 0, 0]
    board[1][1] = [0, 1, 0]
    board[2][2] = [0, 0, 1]
    assert has_won(board, 1) is True


def test_has_won_3d_diagonal_4x4():
    board = create_3d_grid(4)
    assert has_won(board, 1) is False
    board[0][0] = [0, 0, 0, 1]
    board[1][1] = [0, 0, 1, 0]
    board[2][2] = [0, 1, 0, 0]
    assert has_won(board, 1) is False
    board[3][3] = [1, 0, 0, 0]
    assert has_won(board, 1) is True
