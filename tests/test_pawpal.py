import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "diagrams"))
from datetime import date, timedelta
from pawpal_system import Owner, Pet, CareTask, Priority, Scheduler, DailyPlan

def make_owner():
    return Owner(name="Love", available_time_minutes=120, start_time_hour=8)

def make_pet():
    return Pet(name="Buddy", species="Dog")

def make_tasks(pet):
    return [
        CareTask(title="Playtime",     duration_minutes=15, priority=Priority.LOW,    pet=pet),
        CareTask(title="Morning Walk", duration_minutes=30, priority=Priority.HIGH,   pet=pet),
        CareTask(title="Feeding",      duration_minutes=10, priority=Priority.HIGH,   pet=pet),
    ]

def test_mark_complete_changes_status():
    task = CareTask(title="Walk", duration_minutes=30, priority=Priority.HIGH)
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True

def test_add_task_increases_pet_task_count():
    pet = make_pet()
    task = CareTask(title="Feeding", duration_minutes=10, priority=Priority.MEDIUM)
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1

def test_sort_tasks_by_priority_order():
    pet = make_pet()
    tasks = make_tasks(pet)
    scheduler = Scheduler()
    sorted_tasks = scheduler.sort_tasks_by_priority(tasks)
    assert sorted_tasks[0].priority == Priority.HIGH
    assert sorted_tasks[-1].priority == Priority.LOW

def test_sort_by_time_chronological():
    pet = make_pet()
    owner = make_owner()
    tasks = make_tasks(pet)
    scheduler = Scheduler()
    plan = scheduler.create_daily_plan(tasks, owner)
    sorted_by_time = scheduler.sort_by_time(plan)
    times = [t for _, t in sorted_by_time]
    assert times == sorted(times)

def test_sort_priority_then_duration():
    pet = make_pet()
    tasks = [
        CareTask(title="Long High",  duration_minutes=30, priority=Priority.HIGH, pet=pet),
        CareTask(title="Short High", duration_minutes=10, priority=Priority.HIGH, pet=pet),
    ]
    scheduler = Scheduler()
    sorted_tasks = scheduler.sort_tasks_by_priority(tasks)
    assert sorted_tasks[0].title == "Short High"

def test_filter_by_pet_name():
    buddy = Pet(name="Buddy", species="Dog")
    whiskers = Pet(name="Whiskers", species="Cat")
    tasks = [
        CareTask(title="Walk",    duration_minutes=30, priority=Priority.HIGH, pet=buddy),
        CareTask(title="Feeding", duration_minutes=10, priority=Priority.HIGH, pet=whiskers),
    ]
    scheduler = Scheduler()
    result = scheduler.filter_tasks(tasks, pet_name="Buddy")
    assert len(result) == 1
    assert result[0].pet.name == "Buddy"

def test_filter_by_completed_status():
    pet = make_pet()
    tasks = make_tasks(pet)
    tasks[0].mark_complete()
    scheduler = Scheduler()
    done = scheduler.filter_tasks(tasks, completed=True)
    assert len(done) == 1
    assert done[0].title == "Playtime"

def test_filter_pet_with_no_tasks():
    pet = make_pet()
    tasks = [CareTask(title="Walk", duration_minutes=30, priority=Priority.HIGH, pet=pet)]
    scheduler = Scheduler()
    result = scheduler.filter_tasks(tasks, pet_name="Whiskers")
    assert result == []

def test_daily_recurring_creates_next_task():
    task = CareTask(title="Feeding", duration_minutes=10, priority=Priority.HIGH, recurring="daily")
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert next_task.completed == False

def test_weekly_recurring_creates_next_task():
    task = CareTask(title="Grooming", duration_minutes=20, priority=Priority.MEDIUM, recurring="weekly")
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(weeks=1)

def test_non_recurring_returns_none():
    task = CareTask(title="One-off", duration_minutes=10, priority=Priority.LOW)
    result = task.mark_complete()
    assert result is None

def test_no_conflicts_in_sequential_plan():
    pet = make_pet()
    owner = make_owner()
    tasks = make_tasks(pet)
    scheduler = Scheduler()
    plan = scheduler.create_daily_plan(tasks, owner)
    assert plan.conflicts == []

def test_owner_with_no_time_skips_all_tasks():
    pet = make_pet()
    owner = Owner(name="Busy", available_time_minutes=0)
    tasks = make_tasks(pet)
    scheduler = Scheduler()
    plan = scheduler.create_daily_plan(tasks, owner)
    assert len(plan.scheduled_tasks) == 0
    assert len(plan.unscheduled_tasks) == len(tasks)

def test_pet_with_no_tasks_filters_empty():
    tasks = [CareTask(title="Walk", duration_minutes=30, priority=Priority.HIGH,
                      pet=Pet(name="Buddy", species="Dog"))]
    scheduler = Scheduler()
    result = scheduler.filter_tasks(tasks, pet_name="Ghost")
    assert result == []
