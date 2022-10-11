from concurrent.futures.process import _chain_from_iterable_of_lists
import tkinter
from GUI.Simulation_Data import Simulation_Data
from colour import Color
import math
import numpy as np

red = Color("red")
colors = list(red.range_to(Color("violet"),70))

# Returns a table containing the coords of the cell based on the shape of the table
def Get_Cell_Coord(cell_id, shape):
    cell_ratio = cell_id / shape[0]
    cell_coords = ( math.floor(cell_ratio),
                    round((cell_ratio - math.floor(cell_ratio)) * shape[0])
                  )
    return cell_coords

def Solve(sim_data: Simulation_Data, editor, maze: np.array):
    print("Solving Maze...")
    dict_output = {}
    count = 0


    """ Generate a dictionnary with key being coordinates and values being cell data """
    for x in range(0, maze.shape[0]):
        for y in range(0, maze.shape[1]):
            dict_output[Get_Cell_Coord(maze[x][y][0], maze.shape)] = maze[x][y]
            count += 1

    print(f"Length of dict : {len(dict_output)} ; expected length : {count}")

    entrance_cell_coords = Get_Cell_Coord(sim_data.entrance_cell.cell_id, maze.shape)
    exit_cell_coords = Get_Cell_Coord(sim_data.exit_cell.cell_id, maze.shape)
    direction_to_process = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    coords_to_process = [exit_cell_coords]
    next_process = []
    processed_coords = []
    is_searching = True

    while is_searching:
        for coord in coords_to_process:
            for direction in direction_to_process:
                current_tile = (coord[0] + direction[0], coord[1] + direction[1])

                # If it is out of bounds
                if (current_tile[0] < 0 or current_tile[0] > 37) or (current_tile[1] < 0 or current_tile[1] > 50): continue

                # If the surrounding tile is a wall
                if dict_output[current_tile][1] == 1: continue

                # If it as already been processed
                if current_tile in processed_coords: continue

                # If it has already been processed by an other tile
                if current_tile in next_process: continue

                # If current tile is the exit
                if current_tile == entrance_cell_coords:
                    is_searching = False
                    break

                # Mark the distance from the arrived
                dict_output[current_tile][4] = dict_output[coord][4] + 1
                next_process.append(current_tile)

                # Update the canvas 
                editor.main_canvas.itemconfigure(dict_output[current_tile][2], fill=colors[dict_output[current_tile][4]], outline=colors[dict_output[current_tile][4]])

                # Update the GUI
                editor.main_canvas.update()
                editor.update()
            
            if is_searching == False:
                break

            processed_coords.append(coord)

        coords_to_process = next_process.copy()
        next_process.clear()

    current_tile = entrance_cell_coords

    while True:
        dict_output[current_tile][4] = 0
        current_process = {}

        for direction in direction_to_process:
            next_tile = (current_tile[0] + direction[0], current_tile[1] + direction[1])
            print(next_tile)

            # Check if the tile is out of bound
            if (next_tile[0] < 0 or next_tile[0] > 37) or (next_tile[1] < 0 or next_tile[1] > 50): continue

            # Checks if the tile is a wall
            if dict_output[next_tile][1] == 1: continue

            # If the tile has not been processed by the searcher
            if dict_output[next_tile][4] == 0: continue

            current_process[next_tile] = dict_output[next_tile][4]
        
        current_process_sorted = {k: v for k, v in sorted(current_process.items(), key=lambda item: item[1])}
        current_tile = list(current_process_sorted.keys())[0]
        editor.main_canvas.itemconfigure(dict_output[current_tile], fill='pink', outline='pink')
        editor.main_canvas.update()
        editor.update()
    print("Solved !")
    
    