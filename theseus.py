import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation


def check_move(x,y, rows, columns):
    '''This function will check if the move is inside the maze bounds'''
    return 0 <= x < rows and 0 <= y < columns

def generate_maze(dimensions):
    rows, columns = dimensions

    ## First, we create a grid with all walls.
    maze = [[1 for _ in range(columns)] for _ in range(rows)]

    def create_path(x,y):

        ##First we define the valid movements
        directions = [(2,0), #right 
                    (0,2), #up
                    (-2,0), #left
                    (0,-2) #down
                    ]
        
        random.shuffle(directions) ##Like this we do not know the order of the directions

        for dx, dy in directions:
            new_x, new_y = x+dx, y+dy

            if check_move(new_x, new_y, rows, columns) and maze[new_x][new_y] == 1:
                maze[(x+new_x)//2][(y+new_y)//2] = 0
                maze[new_x][new_y] = 0
                for row in maze:
                    print(' '.join(str(cell) for cell in row))
                print("************************")
                create_path(new_x, new_y)

    # Choose a random starting point and make it open
    start_x, start_y = random.randrange(0, rows, 2), random.randrange(0, columns, 2)
    maze[start_x][start_y] = 0

    for row in maze:
        print(' '.join(str(cell) for cell in row))
    print("************************")



    # Start carving the maze from the initial position
    create_path(start_x, start_y)

    # Set random start and goal positions
    start = (start_x, start_y)
    goal_x, goal_y = random.randrange(0, rows, 2), random.randrange(0, columns, 2)
    maze[goal_x][goal_y] = 'G'


    return maze, start, (goal_x, goal_y)





def valida_move_theseus(x,y, rows, columns, maze):
    '''This function will check if the move is inside the maze bounds'''
    return 0 <= x < rows and 0 <= y < columns and maze[x][y] != 1


if __name__ == '__main__':
    # Generate a random maze of size 11x11
    rows, cols = 12, 12
    maze, start, goal = generate_maze((rows, cols))

    # Print the generated maze
    for row in maze:
        print(' '.join(str(cell) for cell in row))

    print(f"\nStart position: {start}")
    print(f"Goal position: {goal}")


    visited = set()
    succesful_path = []

    moves = [
        (1,0),
        (0,1),
        (-1,0),
        (0,-1)
    ]

    
    def theseus_brain(start, path_memory, visited_memory):
        x,y = start

        if maze[x][y] == 'G':
            succesful_path.append((x,y))
            path_memory.append((x, y))
            return True
        
        visited.add((x,y))
        # Mark the current cell as visited
        visited_memory.add((x, y))
        path_memory.append((x, y))

        for move in moves:
            new_x, new_y = x + move[0], y + move[1]

            # Check if the new move is valid and not visited
            if valida_move_theseus(new_x, new_y, rows, cols, maze) and (new_x, new_y) not in visited:
                # Recursively search from the new position
                if theseus_brain((new_x, new_y), path_memory, visited_memory):
                    succesful_path.append((x, y))
                    return True
        path_memory.pop()
        return False
    
    path_memory =[]
    visited_memory = set()
    # Run the algorithm starting from the initial mouse position
    if theseus_brain(start, path_memory, visited_memory):
        print("Mouse found the cheese! Path:", succesful_path[::-1])
    else:
        print("Mouse couldn't find the cheese.")


    # Create an animation of the mouse's movement
    fig, ax = plt.subplots()
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    # Draw the maze
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:  # Draw walls
                ax.add_patch(patches.Rectangle((j, rows - i - 1), 1, 1, color='black'))
            elif maze[i][j] == 'G':  # Draw goal
                ax.add_patch(patches.Rectangle((j, rows - i - 1), 1, 1, color='yellow'))

    # Initialize the mouse as a square
    mouse = patches.Rectangle((start[1], rows - start[0] - 1), 1, 1, color='red')
    ax.add_patch(mouse)

    # Function to update the animation
    def update(frame):
        if frame < len(path_memory):
            mouse.set_xy((path_memory[frame][1], rows - path_memory[frame][0] - 1))
        return mouse,

    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(path_memory), interval=300, blit=True)
    # Save the animation as an MP4 video
    anim.save('maze_animation.gif', writer='ffmpeg', fps=3)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()

        



