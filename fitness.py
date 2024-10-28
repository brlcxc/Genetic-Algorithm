def fitness(schedule):
    score = 0
    facilitator_activity_count = {}
    facilitator_time_slots = {}

    # Initialize facilitator load tracking
    for activity in schedule.activities:
        facilitator_name = activity.facilitator.name
        if facilitator_name not in facilitator_activity_count:
            facilitator_activity_count[facilitator_name] = 0
            facilitator_time_slots[facilitator_name] = []

        facilitator_activity_count[facilitator_name] += 1
        facilitator_time_slots[facilitator_name].append(activity.time_slot)

    # Check each activity for room constraints, facilitators, and time conflicts
    for activity in schedule.activities:
        facilitator_name = activity.facilitator.name

        # Room constraints
        if activity.room.capacity < activity.expected_enrollment:
            score -= 0.5
        elif activity.room.capacity > 3 * activity.expected_enrollment:
            score -= 0.2 if activity.room.capacity <= 6 * activity.expected_enrollment else 0.4
        else:
            score += 0.3

        # Facilitator constraints
        if activity.name in activity.facilitator.preferred_activities:
            score += 0.5
        elif activity.name in activity.facilitator.other_activities:
            score += 0.2
        else:
            score -= 0.1

        # Facilitator load calculations
        if facilitator_time_slots[facilitator_name].count(activity.time_slot) == 1:
            score += 0.2
        else:
            score -= 0.2

        # Check total facilitator load
        if facilitator_activity_count[facilitator_name] > 4:
            score -= 0.5
        elif 1 <= facilitator_activity_count[facilitator_name] <= 2 and facilitator_name != "Dr. Tyler":
            score -= 0.4

        # Time slot adjacency checks for SLA 191 and SLA 101
        if activity.name in ["SLA 101", "SLA 191"]:
            other_activity = find_related_activity(schedule, activity)
            if other_activity:
                score += check_activity_specific_constraints(activity, other_activity)

    return score

def find_related_activity(schedule, target_activity):
    related_section = None
    for activity in schedule.activities:
        if activity.name == target_activity.name and activity.section != target_activity.section:
            related_section = activity
            break
    return related_section

def check_activity_specific_constraints(activity1, activity2):
    score = 0

    # Assuming time_slot format is "10 AM", convert to hours for calculation
    time1 = convert_time_to_hours(activity1.time_slot)
    time2 = convert_time_to_hours(activity2.time_slot)
    time_difference = abs(time1 - time2)

    if activity1.name == "SLA 101" and activity2.name == "SLA 101":
        # SLA 101 specific rules
        if time_difference > 4:
            score += 0.5
        if activity1.time_slot == activity2.time_slot:
            score -= 0.5
    elif activity1.name == "SLA 191" and activity2.name == "SLA 191":
        # SLA 191 specific rules
        if time_difference > 4:
            score += 0.5
        if activity1.time_slot == activity2.time_slot:
            score -= 0.5
    elif (activity1.name == "SLA 191" and activity2.name == "SLA 101") or \
         (activity1.name == "SLA 101" and activity2.name == "SLA 191"):
        # Rules for SLA 191 and SLA 101 interactions
        if time_difference == 1:
            score += 0.25
        if time_difference == 0:
            score -= 0.25
        if time_difference == 1 or time_difference == 0:
            if is_consecutive_time_slots(activity1.time_slot, activity2.time_slot):
                score += 0.5
                # Check for Roman/Beach building condition
                if (activity1.room.name in ["Roman", "Beach"]) != (activity2.room.name in ["Roman", "Beach"]):
                    score -= 0.4

    return score

def convert_time_to_hours(time_slot):
    hour, period = time_slot.split()
    hour = int(hour)
    if period == "PM" and hour != 12:
        hour += 12
    if period == "AM" and hour == 12:
        hour = 0
    return hour

def is_consecutive_time_slots(time_slot1, time_slot2):
    hour1 = convert_time_to_hours(time_slot1)
    hour2 = convert_time_to_hours(time_slot2)
    return abs(hour1 - hour2) == 1