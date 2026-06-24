"""
PawPal+ System Classes
Class skeletons based on UML design
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    """Enum for task priority levels to avoid string typos."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Owner:
    """Represents a pet owner with available time for pet care."""
    name: str
    available_time_minutes: int
    pets: List['Pet'] = field(default_factory=list)
    start_time_hour: int = 8

    def __post_init__(self):
        """Validate that available time and start hour are within acceptable ranges."""
        if self.available_time_minutes < 0:
            raise ValueError("Available time cannot be negative")
        if not 0 <= self.start_time_hour <= 23:
            raise ValueError("Start time hour must be between 0 and 23")

    def get_available_time(self) -> int:
        """Return the owner's total available time in minutes."""
        return self.available_time_minutes

    def add_pet(self, pet: 'Pet') -> None:
        """Append a pet to the owner's list of pets."""
        self.pets.append(pet)


@dataclass
class Pet:
    """Represents a pet with basic information and special needs."""
    name: str
    species: str
    special_needs: str = ""
    tasks: List['CareTask'] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a formatted string describing the pet and its special needs."""
        info = f"{self.name} ({self.species})"
        if self.special_needs:
            info += f" — Special needs: {self.special_needs}"
        return info

    def add_task(self, task: 'CareTask') -> None:
        """Append a care task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class CareTask:
    """Represents a single pet care task with duration and priority."""
    title: str
    duration_minutes: int
    priority: Priority
    pet: Optional['Pet'] = None
    completed: bool = False

    def __post_init__(self):
        """Validate that task duration is a positive number."""
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be positive")

    def mark_complete(self) -> None:
        """Mark this task as completed by setting completed to True."""
        self.completed = True

    def get_priority_score(self) -> int:
        """Return the numeric priority value for use in sorting."""
        return self.priority.value

    def __str__(self) -> str:
        """Return a human-readable string representation of the task."""
        pet_name = self.pet.name if self.pet else "General"
        status = "✅" if self.completed else "⬜"
        return f"{status} [{self.priority.name}] {self.title} ({self.duration_minutes} min) — {pet_name}"


@dataclass
class DailyPlan:
    """Represents a complete daily care plan with scheduled tasks."""
    scheduled_tasks: List[tuple] = field(default_factory=list)
    total_time_used: int = 0
    explanation: str = ""
    unscheduled_tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask, start_time_str: str) -> None:
        """Append a task and its start time to the scheduled tasks list."""
        self.scheduled_tasks.append((task, start_time_str))
        self.total_time_used += task.duration_minutes

    def get_summary(self) -> str:
        """Return a formatted string summarizing all scheduled and unscheduled tasks."""
        lines = ["=" * 40, "       🐾 TODAY'S SCHEDULE — PawPal+", "=" * 40]
        for task, start_time in self.scheduled_tasks:
            pet_name = task.pet.name if task.pet else "General"
            lines.append(
                f"  {start_time}  [{task.priority.name:<6}]  {task.title} ({task.duration_minutes} min) — {pet_name}")
        if self.unscheduled_tasks:
            lines.append("\n  ⚠️  Could not schedule:")
            for task in self.unscheduled_tasks:
                lines.append(f"    - {task.title}")
        lines.append("-" * 40)
        lines.append(f"  Total time used : {self.total_time_used} min")
        if self.explanation:
            lines.append(f"  Note: {self.explanation}")
        lines.append("=" * 40)
        return "\n".join(lines)


class Scheduler:
    """Scheduling engine that creates optimized daily plans."""

    def sort_tasks_by_priority(self, tasks: List[CareTask]) -> List[CareTask]:
        """Sort and return tasks ordered from highest to lowest priority."""
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)

    def create_daily_plan(self, tasks: List[CareTask], owner: Owner) -> DailyPlan:
        """Build and return a DailyPlan by scheduling tasks within the owner's time budget."""
        plan = DailyPlan()
        sorted_tasks = self.sort_tasks_by_priority(tasks)
        current_hour = owner.start_time_hour
        current_min = 0
        time_left = owner.available_time_minutes

        for task in sorted_tasks:
            if task.duration_minutes <= time_left:
                start_time_str = f"{current_hour:02d}:{current_min:02d}"
                plan.add_task(task, start_time_str)
                current_min += task.duration_minutes
                current_hour += current_min // 60
                current_min %= 60
                time_left -= task.duration_minutes
            else:
                plan.unscheduled_tasks.append(task)

        plan.explanation = f"{time_left} min remaining after scheduling."
        return plan
