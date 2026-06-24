from diagrams.pawpal_system import Owner, Pet, CareTask, Priority, Scheduler
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "diagrams"))

owner = Owner(name="Love", available_time_minutes=120, start_time_hour=8)
buddy = Pet(name="Buddy", species="Dog", special_needs="Needs daily walk")
whiskers = Pet(name="Whiskers", species="Cat", special_needs="Indoor only")
owner.pets.append(buddy)
owner.pets.append(whiskers)

tasks = [
    CareTask(title="Playtime",         duration_minutes=15,
             priority=Priority.LOW,    pet=buddy),
    CareTask(title="Litter Box Clean", duration_minutes=10,
             priority=Priority.MEDIUM, pet=whiskers),
    CareTask(title="Morning Walk",     duration_minutes=30,
             priority=Priority.HIGH,   pet=buddy),
    CareTask(title="Grooming Session", duration_minutes=20,
             priority=Priority.MEDIUM, pet=buddy, recurring="weekly"),
    CareTask(title="Feeding",          duration_minutes=10,
             priority=Priority.HIGH,   pet=whiskers, recurring="daily"),
]

scheduler = Scheduler()
plan = scheduler.create_daily_plan(tasks, owner)

print("=" * 40)
print("  📋 SORTED BY TIME")
print("=" * 40)
for task, start_time in scheduler.sort_by_time(plan):
    print(
        f"  {start_time}  [{task.priority.name:<6}]  {task.title} — {task.pet.name}")

print()
print("=" * 40)
print("  🔁 COMPLETING RECURRING TASKS")
print("=" * 40)
next_tasks = []
for task in tasks:
    if task.recurring != "none":
        next_task = task.mark_complete()
        print(f"  ✅ '{task.title}' marked complete (due: {task.due_date})")
        if next_task:
            next_tasks.append(next_task)
            print(
                f"  ➕ Next '{next_task.title}' scheduled for: {next_task.due_date}")

tasks.extend(next_tasks)

print()
print("=" * 40)
print("  📅 ALL TASKS WITH DUE DATES")
print("=" * 40)
for t in tasks:
    status = "✅" if t.completed else "⬜"
    print(f"  {status} {t.title} — due: {t.due_date} [{t.recurring}]")
