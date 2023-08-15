import random

base_hp, base_energy = 100, 50

num_generations = 50
mutation_rate = 1  
genome_length = 9
priority_length = 5
cell_type_length = 4
population_size = 500

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
def update_coordinates(parent_cell, child_cell):
    try:
        print('keepalive')
        x, y = cell_coordinates[tuple(parent_cell)]
        best_prioritet = max(parent_cell[:5])
        index = parent_cell.index(best_prioritet)

        if(cell_data[tuple(child_cell)][2] == 5):
            mult = best_prioritet // 2
        else:
            mult = 1
        if index == 0:  # Stay in the same place
            ox,oy = (x,y)

        elif index == 1:  # Move up
            ox,oy = (x, y+mult)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0

        elif index == 2:  # Move left
            ox,oy = (x-mult, y)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0

        elif index == 3:  # Move right
            ox,oy = (x+mult, y)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0

        elif index == 4:  # Move down
            ox,oy = (x, y-mult)
            if(ox > __ROWS):
                ox = __ROWS
            elif(ox < 0):
                ox = 0
            if(oy > __COLS):
                oy = __COLS
            elif(oy < 0):
                oy = 0
        
        cell_coordinates[tuple(child_cell)] = (ox, oy)
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
    type = int(cell_data[tuple(cell)][2])
    organics = __PARAMS[(alive_x, alive_y)][0]
    energy = __PARAMS[(alive_x, alive_y)][1]
    if(alive_x == __ROWS or alive_y == __COLS):
        if(cell_data[tuple(cell)][0] > 0): cell_data[tuple(cell)][0] = 0
        check_hp_cells()
        return -2
    elif (organics <= 40 and energy <= 30):
        if(cell_data[tuple(cell)][0] != 100): cell_data[tuple(cell)][0] += 5
        if(cell_data[tuple(cell)][1] != 100): cell_data[tuple(cell)][1] += 10
        return 1
    else:
        if(organics >= 40 and energy <= 30 and type == 3):
            if(cell_data[tuple(cell)][1] != 100): cell_data[tuple(cell)][1] += 10
            return 2
        elif(energy >= 30 and organics <= 40  and type == 4):
            if(cell_data[tuple(cell)][1] != 100): cell_data[tuple(cell)][1] += 10
            return 2
        
        cell_data[tuple(cell)][0] -= 10
        cell_data[tuple(cell)][1] -= 20
        return -1

def updateDicts(cell_parent, mutated : bool, cell_child = None, type = None, health = None, energy = None):
    print('keepalive')
    if(cell_child):
        if(not mutated):
            cell_data[tuple(cell_child)] = cell_data[tuple(cell_parent)]
            update_coordinates(cell_parent, cell_child)
        else:
            cell_data[tuple(cell_child)] = cell_data[tuple(cell_parent)]
            cell_coordinates[tuple(cell_child)] = cell_coordinates[tuple(cell_parent)]
            if(cell_child != cell_parent):
                cell_coordinates.pop(tuple(cell_parent))
                population.pop(population.index(cell_parent))
                cell_data.pop(tuple(cell_parent))
                

        if(cell_child not in population):
                population.append(cell_child)

        if(type):
            cell_data[tuple(cell_child)][2] = type    
    else:
        if(type):
            cell_data[tuple(cell_parent)][2] = type
        elif(health):
            cell_data[tuple(cell_parent)][0] = health
        elif(energy):
            cell_data[tuple(cell_parent)][1] = energy
    #sleep(0.2)


def check_hp_cells():
    print('keepalive')
    for cell in population:
        if (cell_data[tuple(cell)][0] <= 0):
            cell_data.pop(tuple(cell))
            cell_coordinates.pop(tuple(cell))
            population.pop(population.index(cell))

def initialize_population(pop_size):
    print('keepalive')
    population = []
    for _ in range(pop_size):
        genome = [random.randint(0, 9) for _ in range(priority_length)] + [random.randint(0, 5) for _ in range(cell_type_length)]
        x = random.randint(0, __ROWS)
        y = random.randint(0, __COLS)
        cell_coordinates[tuple(genome)] = (x, y)
        cell_data[tuple(genome)] = [base_hp, base_energy, 1] # 0 - количество здоровья, 1 - количество энергии, 2 - тип клетки (всего их пока 5. 0 - стебли соединения, 1 - основа, 2 - лист, 3 - корень, 4 - антенна, 5 - семя)
        population.append(genome)
    return population

def create_cell(base_cell):
    type = max(base_cell[5:])
    if(cell_data[tuple(base_cell)][1] >= 10 and cell_data[tuple(base_cell)][2] == 1 or cell_data[tuple(base_cell)][2] == 5):
        cell_data[tuple(base_cell)][1] -= 10
        copy = base_cell.copy()
        index_to_change = random.randint(4, len(base_cell) - 1)
        new_value = random.randint(0, 5)
        copy[index_to_change] = new_value
        new_cell = base_cell[:5] + copy[5:]
        updateDicts(base_cell, False, new_cell, type)
    elif(cell_data[tuple(base_cell)][1] >= 50 and type == 5):
        cell_data[tuple(base_cell)][1] -= 50
        new_cell = base_cell
        updateDicts(base_cell, False, new_cell, type)
        

def mutate(genome):
    print('keepalive')
    mutated_genome = genome.copy()
    index_to_change = random.randint(0, len(mutated_genome) - 1)
    new_value = random.randint(0, 9) if index_to_change <= 4 else random.randint(0, 5)
    mutated_genome[index_to_change] = new_value
    updateDicts(genome, True, mutated_genome)
    return mutated_genome

def genetic_algorithm():
    print('keepalive')
    global population
    population = initialize_population(population_size)
    best_fitness = float('-inf')
    while True:

        if(random.random() < mutation_rate):
            rng = random.randint(0, len(population)-1)
            mutate(population[rng])
            
        check_hp_cells()
        fitness_scores = [fitness_function(cell) for cell in population]
        best_fit_indices = sorted(range(len(population)), key=lambda i: fitness_scores[i], reverse=True)[:2]
        if fitness_scores[fitness_scores.index(max(fitness_scores))] > best_fitness:
            best_fitness = fitness_scores[fitness_scores.index(max(fitness_scores))]
            best_genome = population[best_fit_indices[0]]
        
            