import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "diagrams"))
from pawpal_system import Pet, CareTask, Priority


def test_mark_complete_changes_status():
    task = CareTask(title="Walk", duration_minutes=30, priority=Priority.HIGH)
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog")
    task = CareTask(title="Feeding", duration_minutes=10, priority=Priority.MEDIUM)
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
