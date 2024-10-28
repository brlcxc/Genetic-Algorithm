import random

# creating data structures for the room, activity, and schedule
class Facilitator:
    def __init__(self, name, preferred_activities=None, other_activities=None):
        self.name = name
        self.preferred_activities = preferred_activities or []
        self.other_activities = other_activities or []

class Room:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

class Activity:
    def __init__(self, name, section, expected_enrollment, preferred_facilitators, other_facilitators):
        self.name = name
        self.section = section
        self.expected_enrollment = expected_enrollment
        self.preferred_facilitators = preferred_facilitators
        self.other_facilitators = other_facilitators
        # None fields are assigned during scheduling
        self.facilitator = None
        self.room = None
        self.time_slot = None

class Schedule:
    def __init__(self):
        self.activities = []
        self.rooms = []
        self.time_slots = []
        self.facilitators = []

    def initialize(self):
        # Initialize facilitators
        facilitators = [
            "Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"
        ]
        self.facilitators = [Facilitator(name) for name in facilitators]

        # initialize rooms with their name and expected enrollment
        self.rooms = [
            Room("Slater 003", 45),
            Room("Roman 216", 30),
            Room("Loft 206", 75),
            Room("Roman 201", 50),
            Room("Loft 310", 108),
            Room("Beach 201", 60),
            Room("Beach 301", 75),
            Room("Logos 325", 450),
            Room("Frank 119", 60)
        ]

        # initialize time slots
        self.time_slots = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

        # initialize activities, with their name, section, expected enrollment, preferred  facilitators, and other facilitators 
        self.activities = [
            Activity("SLA100", "A", 50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
            Activity("SLA100", "B", 50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
            Activity("SLA191", "A", 50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
            Activity("SLA191", "B", 50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
            Activity("SLA201", None, 50, ["Glen", "Banks", "Zeldin", "Shaw"], ["Numen", "Richards", "Singer"]),
            Activity("SLA291", None, 50, ["Lock", "Banks", "Zeldin", "Singer"], ["Numen", "Richards", "Shaw", "Tyler"]),
            Activity("SLA303", None, 60, ["Glen", "Zeldin", "Banks"], ["Numen", "Singer", "Shaw"]),
            Activity("SLA304", None, 25, ["Glen", "Banks", "Tyler"], ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"]),
            Activity("SLA394", None, 20, ["Tyler", "Singer"], ["Richards", "Zeldin"]),
            Activity("SLA449", None, 60, ["Tyler", "Singer", "Shaw"], ["Zeldin", "Uther"]),
            Activity("SLA451", None, 100, ["Tyler", "Singer", "Shaw"], ["Zeldin", "Uther", "Richards", "Banks"])
        ]

        # Assign preferred and other activities to facilitators
        for activity in self.activities:
            for facilitator in self.facilitators:
                if facilitator.name in activity.preferred_facilitators:
                    facilitator.preferred_activities.append(activity.name)
                elif facilitator.name in activity.other_facilitators:
                    facilitator.other_activities.append(activity.name)

    def generate_random_schedule(self):
        # the rooms, time, and facilitator of each activity is randomly assigned
        for activity in self.activities:
            activity.room = random.choice(self.rooms)
            activity.time_slot = random.choice(self.time_slots)
            activity.facilitator = random.choice(self.facilitators)

        return self  # return the schedule object itself

def generate_initial_population(size=500):
    population = []
    base_schedule = Schedule()
    base_schedule.initialize()

    for _ in range(size):
        new_schedule = Schedule()
        new_schedule.activities = [activity for activity in base_schedule.activities]  # Copy activities
        new_schedule.rooms = base_schedule.rooms  # Use the same room setup
        new_schedule.time_slots = base_schedule.time_slots  # Use the same time slots
        new_schedule.facilitators = base_schedule.facilitators  # Use the same facilitators

        # Randomize the schedule
        random_schedule = new_schedule.generate_random_schedule()
        population.append(random_schedule)

    return population

# Example usage
population = generate_initial_population(2000)
