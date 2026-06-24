"""
PawPal+ System Classes
Class skeletons based on UML design
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Owner:
    """Represents a pet owner with available time for pet care."""
    name: str
    available_time_minutes: int

    def get_available_time(self) -> int:
        """Returns the owner's available time in minutes."""
        pass


@dataclass
class Pet:
    """Represents a pet with basic information and special needs."""
    name: str
    species: str
    special_needs: str = ""

    def get_info(self) -> str:
        """Returns a formatted string with pet information."""
        pass


@dataclass
class CareTask:
    """Represents a single pet care task with duration and priority."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"

    def get_priority_score(self) -> int:
        """Converts priority string to numeric score for sorting."""
        pass

    def __str__(self) -> str:
        """Returns a human-readable representation of the task."""
        pass


@dataclass
class DailyPlan:
    """
    Represents a complete daily care plan with scheduled tasks.
    Added during implementation to provide richer scheduling output.
    """
    scheduled_tasks: List[tuple] = field(default_factory=list)  # List of (CareTask, start_time)
    total_time_used: int = 0
    explanation: str = ""
    unscheduled_tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask, start_time: str) -> None:
        """Adds a task to the schedule with its start time."""
        pass

    def get_summary(self) -> str:
        """Returns a formatted summary of the daily plan."""
        pass


class Scheduler:
    """
    Scheduling engine that creates optimized daily plans.
    Takes tasks and owner constraints to produce a DailyPlan.
    """

    def create_daily_plan(self, tasks: List[CareTask], owner: Owner) -> DailyPlan:
        """
        Creates an optimized daily plan based on tasks and available time.

        Args:
            tasks: List of CareTask objects to schedule
            owner: Owner object with available time constraint

        Returns:
            DailyPlan object with scheduled tasks and metadata
        """
        pass

    def sort_tasks_by_priority(self, tasks: List[CareTask]) -> List[CareTask]:
        """Sorts tasks by priority (high to low)."""
        pass
