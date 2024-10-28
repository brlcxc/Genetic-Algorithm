import numpy as np
import random
from initialization import Schedule

# converts values into probability distribution
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

# top parents are chosen for the crossover step
def select_parents(population, fitness_scores):
    probabilities = softmax(fitness_scores)
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

# top parents are recombined
def crossover(parent1, parent2):
    # Create a new empty Schedule
    child = Schedule()
    
    # Copy the rooms, facilitators, and time slots from parents
    child.rooms = parent1.rooms
    child.time_slots = parent1.time_slots
    child.facilitators = parent1.facilitators

    # Initialize activities based on parents with a crossover point
    child.activities = parent1.activities[:]  # Copy from parent1 initially
    crossover_point = random.randint(0, len(child.activities) - 1)
    child.activities[:crossover_point] = parent2.activities[:crossover_point]  # Crossover with parent2

    return child


# new information being added into the algorithm
def mutate(schedule, mutation_rate=0.01):
    for activity in schedule.activities:
        if random.random() < mutation_rate:
            activity.room = random.choice(schedule.rooms)
            activity.time_slot = random.choice(schedule.time_slots)
            activity.facilitator = random.choice(schedule.facilitators)
