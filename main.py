#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script, navigate to project in cmd/terminal and:
    #python -m main

Add flags to change game mechanics:
    Number of generations: (eg) -g 100
    World size, size of the grid: (eg) -w 30x70
    Specify patterns: (eg) -s gliders || -s pulsar || -s penta
"""

import argparse
import re
import random
import json
import logging
from itertools import product
import sys
from pathlib import Path
from ast import literal_eval
from time import sleep

import code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """
    _file_path = RESOURCES / f'{_file_name}.json'  # location of seed
    file_path = Path(_file_path).resolve()
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # cast population to tuple, cast value of population to tuple if not null
            _world_size = data['world_size']
            _population = data['population']
        tmp = {}
        for key, value in _population.items():
            #   Evaluate key from _population
            evaluated_key = literal_eval(key)
            tmp[evaluated_key] = value
            if value:
                value['neighbours'] = list(map(tuple, value['neighbours']))
                tmp[evaluated_key] = value
        fetched_data_as_tuple = tmp, tuple(_world_size)
        return fetched_data_as_tuple
    except IOError:
        print(f"File does not exist, make sure flag input ({_file_name}) corresponds to the seed file in question")


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    """Future work needed for this level, IGNORE"""
    log_path = RESOURCES / "gol.log"
    logging.getLogger("gol_logger")
    logging.basicConfig(filename=log_path, filemode="write", level=logging.INFO)
    return create_logger()


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument.
    I opted to use a regular expression to determine if the world size format was correct or not.
    If the regular expression turned out false, i.e (re.search) an Assertion Error is thrown and
    the world size is set to 80 by 40. If the world size conforms with the regular expression
    the last check is done to ensure the world size does not contain any 0 values, i.e 0x0 or 0x40.
    If so a value error is raised.
     """
    assert_message = "World size should contain width and height, separated by ‘x’. Ex: ‘80x40’”"
    size = ()
    regex = re.search("^[0-9]+x[0-9]+$", _arg)
    try:
        assert regex
    except AssertionError:
        size = (80, 40)
        print(f"{assert_message} \nusing default size: {size[0]},{size[1]}")
        return size
    else:
        _arg = _arg.split('x')
        size = (int(_arg[0]), int(_arg[1]))
        try:
            if not size[0] or not size[1]:
                raise ValueError()
        except ValueError:
            size = (80, 40)
            print("Both width and height needs to have positive values above zero")
    finally:
        return size


def populate_world(_world_size: tuple, _seed_pattern: str) -> dict:
    """ Populate the world with cells and initial states.

    The game field is created using a product method with arguments of the range of world size
    width and height. Two check are being done to complete the logic, firstly I make sure to populate the
    rim cells with a state of none. This is done by checking the borders of the game field. The second check
    is done to see if a seed pattern has been passed to the function. If it has, a nested if statement take place,
    otherwise the population is randomized. The nested if statement check weather the current cell exist in the return
    value from cb.get_pattern. If it does it set the state to alive and calculate the neighbours. If it doesn't exist it
    set the state to None as the documentation states (MAP value None to cell coordinate in population)
    """
    population = {}
    width = _world_size[0]
    height = _world_size[1]
    alive_cells_from_seed = cb.get_pattern(_seed_pattern, _world_size)

    #   Create table from parameter _world_size using recommended product method
    for cell in product(range(height), range(width)):

        # Create rim cells, first
        if not (cell[0] and cell[1]) or cell[0] == (height - 1) or cell[1] == (width - 1):
            population[cell] = None
        else:
            if alive_cells_from_seed:
                # populate alive cells based on result from cb.get_pattern
                # Action on cells generated from pattern
                if cell in alive_cells_from_seed:
                    predefined_state = cb.STATE_ALIVE
                    population[cell] = {"state": predefined_state, "neighbours": calc_neighbour_positions(cell)}

                # Action on the rest of the cells not included from pattern
                else:
                    predefined_state = cb.STATE_DEAD
                    population[cell] = {"state": predefined_state, "neighbours": calc_neighbour_positions(cell)}

            # Action on cells if no pattern exists, randomly generated
            else:
                random_state = randomize_initial_state()
                population[cell] = {"state": random_state, "neighbours": calc_neighbour_positions(cell)}

    return population


def randomize_initial_state() -> str:
    """Returns state based on a randomized number
    generates a random number between 0 and 20, if greater than
    16 it returns alive, else dead.
    """
    random_nr = random.randint(0, 20)
    return cb.STATE_ALIVE if random_nr > 16 else cb.STATE_DEAD


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """
    x = _cell_coord[0]
    y = _cell_coord[1]

    # x and y represents the position of cell, for example cell (1,1) is equal to x = 1 and y = 1
    w = (x, y - 1)  # neighbour west of cell (1, 0)-(y=1-1)
    sw = (x + 1, y-1)  # neighbour southwest of cell (2, 0)-(x=1+1)(y=1-1)
    s = (x + 1, y)  # neighbour south of cell (2, 1)-(x=1+1)
    se = (x + 1, y + 1)  # neighbour southeast of cell (2, 2)-(x=1+1)(y=1+1)
    e = (x, y + 1)  # neighbour east of cell (1, 2)-(y=1+1)
    ne = (x - 1, y + 1)  # neighbour northeast of cell (0, 2)-(x=1-1)(y=1+1)
    n = (x - 1, y)  # neighbour north of cell (0, 1)-(x=1-1)
    nw = (x - 1, y - 1)  # neighbour northwest of cell (0, 0)-(x=1-1)(y=1-1)

    neighbours = [w, sw, s, se, e, ne, n, nw]
    return neighbours


def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations.
    I decided to go for the recursive implementation where the next population is
    calculated in iterations of every nth generation of the _generation passed to the function.
    The base case is set to 0, when the base case is hit, the stack frame or state of each recursive call is popped of
    the stack in order and update the world with the next generation based on each-others local state.
    """
    def recursive_implementation(_nth_generation, population):
        #  base case return population
        if _nth_generation <= 0:
            return population
        #  calls itself recursivly and calculates the next generation
        else:
            cb.clear_console()
            next_generation = update_world(population, _world_size)
            sleep(0.2)
            return recursive_implementation(_nth_generation - 1, next_generation)

    return recursive_implementation(_generations, _population)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation.
    This function returns the next generation. It loops through all key value pairs in the curren generation
    and based on the value determines outcome. If the iteration (each key value pair) does not contain a value it
    is equal to a rim cell and therefor no changes is made other than printing out the # character. If it does have
    a value (a state and neighbours) it prints out the state using the "cb.progress" function. Next thing I did was
    check how many neighbours it has to determine the future state. After the number of alive neighbours has been stored
    in a variable the new state is based on the value of that variable. this is done by another function as I thought
    it would enhance the code readability. Lastly the declared nex_gen dictionary keys value is updated with the new or
    same state and neighbours. This is done for rim cells as well just that not extra is done to it's value
    """
    next_gen = {}  # copy current gen
    for key, value in _cur_gen.items():
        if not value:
            cb.progress(cb.get_print_value(cb.STATE_RIM))
            next_gen[key] = value
            if key[1] == _world_size[0] - 1:
                sys.stdout.write("\n")
        else:
            cb.progress(cb.get_print_value(value.get('state')))
            alive_neighbours = count_alive_neighbours(value.get('neighbours'), _cur_gen)
            new_state = change_state(alive_neighbours, _cur_gen[key])

            next_gen[key] = {'state': new_state, 'neighbours': value.get('neighbours')}
    return next_gen


def change_state(alive_neighbours: int, cell_props: dict) -> str:
    """Returns the state of the cell based on alive neighbours in the current generation
    parameters is number of alive neighbours and the cells key value pair. First thing I decided
    to do was to store the old state (dead or alive) in a variable "cell_state_was" to use in my control structure.
    If the cell passed to the function was alive and the number of alive neighbours is  lesser than two but greater than
    three,the function returns the string cb.STATE_DEAD( i.e character -). Otherwise it returns cb.STATE_ALIVE, meaning
    the cell was alive and had exactly three alive neighbours. Now if the cell passed to the function was dead, the
    control structure remains basically the same, it checks if the number of alive neighbours is equal to three and
    returns the state alive using cb.STATE_ALIVE, if not it return dead. All according to the rules specified by
    J.Conway 1970 and the project documentation.
    """
    cell_state_was = cell_props['state']
    if cell_state_was == cb.STATE_ALIVE:
        if alive_neighbours < 2 or alive_neighbours > 3:
            return cb.STATE_DEAD
        else:
            return cb.STATE_ALIVE
    if cell_state_was == cb.STATE_DEAD:
        if alive_neighbours == 3:
            return cb.STATE_ALIVE
        else:
            return cb.STATE_DEAD


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """
    This function simply loops through the list of neighbours for the cell passed to the function and increment the
    alive_neighbours variable by one each time the state is equal to cb.STATE_ALIVE then returns the result.
    """
    alive_neighbours = 0
    for neighbour in _neighbours:
        current_gen_props = _cells[neighbour]
        if current_gen_props:
            if current_gen_props['state'] == cb.STATE_ALIVE:
                alive_neighbours += 1
    return alive_neighbours


def main():
    epilog = "ConwaysGameOfLife" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=10,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
