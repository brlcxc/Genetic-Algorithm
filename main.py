from scm import select_parents, crossover, mutate
from fitness import fitness
from initialization import population

def genetic_algorithm(population, generations=100, mutation_rate=0.01):
    for generation in range(generations):
        fitness_scores = [fitness(individual) for individual in population]
        next_generation = []

        # Track fitness improvement
        if generation > 0 and (max(fitness_scores) - previous_best_fitness) < 0.01 * previous_best_fitness:
            break
        previous_best_fitness = max(fitness_scores)
        
        for _ in range(len(population) // 2):
            parent1, parent2 = select_parents(population, fitness_scores)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            
            next_generation.extend([child1, child2])
        
        population = next_generation[:len(population)]
    
    best_schedule = max(population, key=fitness)
    print(f"Best fitness: {fitness(best_schedule)}")
    return best_schedule

best_schedule = genetic_algorithm(population)
