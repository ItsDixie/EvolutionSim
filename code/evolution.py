import random
from time import sleep
num_generations = 50
mutation_rate = 1  
genome_length = 9
priority_length = 5
cell_type_length = 4
population_size = 100

cell_coordinates = {}
cell_data = {}
def import_from_canvas(size, rows, cols, params):
    global __SIZE, __ROWS, __COLS, __PARAMS
    __SIZE = size
    __ROWS = rows-1
    __COLS = cols-1
    __PARAMS = params

def cells_coord():
    return cell_coordinates
def cells_data():
    return cell_data
def update_coordinates(cell):
    try:
        print('keepalive')
        x, y = cell_coordinates[tuple(cell)]
        best_prioritet = max(cell[:5])
        index = cell.index(best_prioritet)

        if index == 0:  # Stay in the same place
            ox,oy = (x,y)

        elif index == 1:  # Move up
            ox,oy = (x, y+1)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0

        elif index == 2:  # Move left
            ox,oy = (x-1, y)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0

        elif index == 3:  # Move right
            ox,oy = (x+1, y)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0

        elif index == 4:  # Move down
            ox,oy = (x, y-1)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0
        
        cell_coordinates[tuple(cell)] = (ox, oy)
        return (ox, oy)
    
    except Exception:
        print(Exception)

def fitness_function(cell):
    print('keepalive')
    create_cell(cell)
    overall_fitness = cell_data[tuple(cell)][0] + cell_data[tuple(cell)][1]
    health_param = calculate_health_parameter(cell)
    overall_fitness *= health_param


    return overall_fitness

def calculate_health_parameter(cell):
    print('keepalive')
    alive_x = int(cell_coordinates[tuple(cell)][0])
    alive_y = int(cell_coordinates[tuple(cell)][1])
    if(alive_x == __ROWS or alive_y == __COLS):
        if(cell_data[tuple(cell)][0] > 0): cell_data[tuple(cell)][0] = 0
        check_hp_cells()
        return -2
    elif (__PARAMS[(alive_x, alive_y)][0] <= 40 and __PARAMS[(alive_x, alive_y)][1] <= 30):
        if(cell_data[tuple(cell)][0] != 100): cell_data[tuple(cell)][0] += 5
        if(cell_data[tuple(cell)][1] != 100): cell_data[tuple(cell)][1] += 10
        return 2
    else:
        if(cell_data[tuple(cell)][0] > 0): 
            cell_data[tuple(cell)][0] -= 10
        if(cell_data[tuple(cell)][1] > 0): 
            cell_data[tuple(cell)][1] -= 20
        return -1

def check_hp_cells():
    print('keepalive')
    for cell in population:
        if (cell_data[tuple(cell)][0] <= 0):
            cell_data.pop(tuple(cell))
            cell_coordinates.pop(tuple(cell))
            population.pop(population.index(cell))

def initialize_population(pop_size, genome_len):
    print('keepalive')
    population = []
    for _ in range(pop_size):
        genome = [random.randint(0, 9) for _ in range(priority_length)] + [random.randint(0, 4) for _ in range(cell_type_length)]
        x = random.randint(0, __ROWS)
        y = random.randint(0, __COLS)
        cell_coordinates[tuple(genome)] = (x, y)
        cell_data[tuple(genome)] = [100, 50, 1] # 0 - количество здоровья, 1 - количество энергии, 2 - тип клетки (всего их пока 5. 0 - стебли соединения, 1 - основа, 2 - лист, 3 - корень, 4 - антенна)
        population.append(genome)
    return population

def create_cell(base_cell):
    if(cell_data[tuple(base_cell)][1] >= 10):
        cell_data[tuple(base_cell)][1] -= 10
        type = max(base_cell[5:])
        cell_data[tuple(base_cell)][2] = type
        new_cell = base_cell[:5] + [random.randint(0, 4) for _ in range(cell_type_length)]
        population.append(new_cell)
        cell_coordinates.update({tuple(new_cell) : cell_coordinates[tuple(base_cell)]})
        cell_data.update({tuple(new_cell) : cell_data[tuple(base_cell)]})
        sleep(0.2)
        update_coordinates(new_cell)

def mutate(genome):
    print('keepalive')
    mutated_genome = genome.copy()
    for i in range(priority_length, priority_length + 4):
        mutated_genome[i] = random.randint(0, 9)
    cell_coordinates.update({tuple(mutated_genome) : cell_coordinates[tuple(genome)]})
    cell_data.update({tuple(mutated_genome) : cell_data[tuple(genome)]})
    cell_data.pop(tuple(genome))
    cell_coordinates.pop(tuple(genome), None)
    sleep(0.2)
    return mutated_genome

def crossover(parent1, parent2):
    print('keepalive')
    crossover_point = random.randint(1, genome_length - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    cell_coordinates[tuple(child1)] = cell_coordinates[tuple(parent1)]
    cell_coordinates[tuple(child2)] = cell_coordinates[tuple(parent2)]
    cell_coordinates.pop(tuple(parent1), None)
    cell_coordinates.pop(tuple(parent2), None)
    return child1, child2


def select_parents(population, num_parents):
    print('keepalive')
    parents = []
    fitness_scores = [fitness_function(cell) for cell in population]
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    for _ in range(num_parents):
        selected_index = random.choices(range(len(population)), probabilities)[0]
        parents.append(population[selected_index])
    return parents

def genetic_algorithm():
    print('keepalive')
    global population
    population = initialize_population(population_size, genome_length)
    best_genome = None
    best_fitness = float('-inf')
    while True:

        if(random.random() < mutation_rate):
            rng = random.randint(0, len(population)-1)
            mutated = mutate(population[rng])
            population.append(mutated)
            population.pop(rng)
        '''    
        p1,p2 = select_parents(population, 2)           # fix keyerror bug
        child1, child2 = crossover(p1, p2)
        population.append(child1)
        population.append(child2)
        population.pop(population.index(p1))
        population.pop(population.index(p2))'''

        check_hp_cells()
        fitness_scores = [fitness_function(cell) for cell in population]
        best_fit_indices = sorted(range(len(population)), key=lambda i: fitness_scores[i], reverse=True)[:2]
        if fitness_scores[fitness_scores.index(max(fitness_scores))] > best_fitness:
            best_fitness = fitness_scores[fitness_scores.index(max(fitness_scores))]
            best_genome = population[best_fit_indices[0]]
        
            