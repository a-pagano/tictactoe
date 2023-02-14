#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from ast import literal_eval as make_tuple
from typing import Optional

import click
import matplotlib.pyplot as plt
import numpy as np

PLAYER_1_COLOR = [1, 0, 0, 1]  # red
PLAYER_2_COLOR = [0, 0, 1, 1]  # blue


def create_3d_grid(size: int) -> np.ndarray:
    return np.zeros((size, size, size))


def play_move(
    board: np.ndarray, current_player: int, x: int, y: int, z: int
) -> Optional[np.ndarray]:
    if board[x, y, z] > 0:
        print(
            f"The square {x=},{y=},{z=} is already taken, please choose another one"
        )
        return None
    else:
        board[x, y, z] = current_player
    return board


def product_slices(n):
    """
    Taken from https://stackoverflow.com/a/39185702
    """
    for i in range(n):
        yield (
            np.index_exp[np.newaxis] * i
            + np.index_exp[:]
            + np.index_exp[np.newaxis] * (n - i - 1)
        )


def get_lines(n, k):
    """
    Taken from https://stackoverflow.com/a/39185702
    """
    forward_seq = np.arange(k)
    backward_seq = forward_seq[::-1]
    repeat_seq = forward_seq[:, None].repeat(k, axis=1)

    all_seq = np.concatenate(
        (forward_seq[None], backward_seq[None], repeat_seq), axis=0
    )

    index = tuple(all_seq[s] for s in product_slices(n))

    mask = np.zeros((all_seq.shape[0],) * n, dtype=bool)
    sl = np.index_exp[0]
    for i in range(n):
        mask[sl] = True
        sl = np.index_exp[2:] + sl

    return index, mask


def has_won(board: np.ndarray, current_player: int) -> bool:
    index, mask = get_lines(board.ndim, board.shape[0])
    lines = board[index][mask]
    longest_line = max(
        map(
            len,
            (
                list(g)
                for l in lines
                for k, g in itertools.groupby(l)
                if k == current_player
            ),
        ),
        default=0,
    )
    return longest_line >= board.shape[0]


def plot_board(board: np.ndarray) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    x, y, z = np.indices(np.array(board.shape) + 1)
    colors = np.empty(list(board.shape) + [4])
    colors[board == 1] = PLAYER_1_COLOR
    colors[board == 2] = PLAYER_2_COLOR
    ax.voxels(x, y, z, board, facecolors=colors)
    plt.show()


@click.command()
@click.option("--size", help="Size of the 3D cubic board (x,y,z)", type=int)
@click.option("--plot", help="Whether to plot the board in 3D", is_flag=True)
def game_loop(size: int, plot: bool) -> None:
    board = create_3d_grid(size)
    move_counter = 1
    while True:
        if move_counter % 2 == 0:
            current_player = 2
        else:
            current_player = 1
        choice = input(
            f"Player {current_player}, pick your next move in the range (0,0,0) to ({size-1},{size-1},{size-1}) or type "
            f"'exit' to quit the game\n"
            f">>> "
        )
        if choice == "exit":
            exit(0)
        updated_board = play_move(board, current_player, *make_tuple(choice))
        if updated_board is None:
            continue
        if has_won(updated_board, current_player):
            print(f"Player {current_player} has won! Congrats!")
            break
        if plot:
            plot_board(updated_board)
        move_counter += 1
        board = updated_board
    if plot:
        plot_board(board)


if __name__ == "__main__":
    game_loop()
