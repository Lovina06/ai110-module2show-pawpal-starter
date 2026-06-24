"""
PawPal+ System Classes
Class skeletons based on UML design
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import date, timedelta


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
    recurring: str = "none"  # "none", "daily", "weekly"
    due_date: date = field(default_factory=date.today)

    def __post_init__(self):
        """Validate that task duration is a positive number."""
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be positive")

    def mark_complete(self) -> Optional['CareTask']:
        """Mark task complete and return a new instance if recurring, else None."""
        self.completed = True
        if self.recurring == "daily":
            return CareTask(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                pet=self.pet,
                recurring=self.recurring,
                due_date=self.due_date + timedelta(days=1)
            )
        elif self.recurring == "weekly":
            return CareTask(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                pet=self.pet,
                recurring=self.recurring,
                due_date=self.due_date + timedelta(weeks=1)
            )
        return None

    def get_priority_score(self) -> int:
        """Return the numeric priority value for use in sorting."""
        return self.priority.value

    def __str__(self) -> str:
        """Return a human-readable string representation of the task."""
        pet_name = self.pet.name if self.pet else "General"
        status = "✅" if self.completed else "⬜"
        recur = f" [{self.recurring}]" if self.recurring != "none" else ""
        return f"{status} [{self.priority.name}] {self.title} ({self.duration_minutes} min) — {pet_name}{recur}"


@dataclass
class DailyPlan:
    """Represents a complete daily care plan with scheduled tasks."""
    scheduled_tasks: List[tuple] = field(default_factory=list)
    total_time_used: int = 0
    explanation: str = ""
    unscheduled_tasks: List[CareTask] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)

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
        if self.conflicts:
            lines.append("\n  ❌ Conflicts detected:")
            for c in self.conflicts:
                lines.append(f"    - {c}")
        lines.append("-" * 40)
        lines.append(f"  Total time used : {self.total_time_used} min")
        if self.explanation:
            lines.append(f"  Note: {self.explanation}")
        lines.append("=" * 40)
        return "\n".join(lines)


class Scheduler:
    """Scheduling engine that creates optimized daily plans."""

    def sort_tasks_by_priority(self, tasks: List[CareTask]) -> List[CareTask]:
        """Sort tasks by priority (high to low), then by duration (short to long)."""
        return sorted(tasks, key=lambda t: (-t.priority.value, t.duration_minutes))

    def sort_by_time(self, plan: DailyPlan) -> List[tuple]:
        """Sort scheduled tasks by their start time in HH:MM format."""
        return sorted(plan.scheduled_tasks, key=lambda x: x[1])

    def filter_tasks(self, tasks: List[CareTask], pet_name: str = None, completed: bool = None) -> List[CareTask]:
        """Filter tasks by pet name and/or completion status."""
        result = tasks
        if pet_name is not None:
            result = [t for t in result if t.pet and t.pet.name == pet_name]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def detect_conflicts(self, plan: DailyPlan) -> List[str]:
        """Detect overlapping tasks and return a list of conflict descriptions."""
        conflicts = []
        tasks_with_times = plan.scheduled_tasks
        for i in range(len(tasks_with_times)):
            task_a, start_a = tasks_with_times[i]
            end_a = self._time_to_minutes(start_a) + task_a.duration_minutes
            for j in range(i + 1, len(tasks_with_times)):
                task_b, start_b = tasks_with_times[j]
                start_b_min = self._time_to_minutes(start_b)
                if start_b_min < end_a:
                    conflicts.append(
                        f"'{task_a.title}' and '{task_b.title}' overlap at {start_b}")
        return conflicts

    def _time_to_minutes(self, time_str: str) -> int:
        """Convert HH:MM string to total minutes since midnight."""
        h, m = map(int, time_str.split(":"))
        return h * 60 + m

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

        plan.conflicts = self.detect_conflicts(plan)
        plan.explanation = f"{time_left} min remaining after scheduling."
        return plan
