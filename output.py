from main import best_schedule

def save_schedule_to_file(schedule, filename="best_schedule.txt"):
    with open(filename, "w") as f:
        for activity in schedule.activities:
            f.write(f"{activity.name} - Room: {activity.room.name}, Time: {activity.time_slot}, Facilitator: {activity.facilitator.name}\n")

save_schedule_to_file(best_schedule)