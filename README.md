# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
========================================
       🐾 TODAY'S SCHEDULE — PawPal+
========================================
Owner : Love
Pets  : Buddy, Whiskers
Budget: 120 mins

  08:00  [HIGH  ]  Morning Walk (30 min) — Buddy
  08:30  [HIGH  ]  Feeding (10 min) — Whiskers
  08:40  [MEDIUM]  Grooming Session (20 min) — Buddy
  09:00  [MEDIUM]  Litter Box Clean (10 min) — Whiskers
  09:10  [LOW   ]  Playtime (15 min) — Buddy
----------------------------------------
  Total time used : 85 min
  Time remaining  : 35 min
========================================
```

## 🧪 Testing PawPal+

```bash
python3 -m pytest tests/test_pawpal.py -v
```

### What the tests cover

- **Task completion** — `mark_complete()` sets `completed` to `True`
- **Pet task list** — `add_task()` increases pet's task count
- **Sorting by priority** — HIGH priority tasks come before LOW
- **Sorting by time** — `sort_by_time()` returns tasks in chronological HH:MM order
- **Priority + duration sort** — shorter tasks first within same priority level
- **Filter by pet** — only tasks for the named pet are returned
- **Filter by status** — completed/incomplete tasks filtered correctly
- **Edge case: no matching pet** — filter returns empty list
- **Daily recurring** — completing a daily task creates next task due tomorrow
- **Weekly recurring** — completing a weekly task creates next task due next week
- **Non-recurring** — completing a one-off task returns `None`
- **No conflicts** — sequential tasks produce no conflict warnings
- **Zero time budget** — owner with 0 minutes skips all tasks
- **Empty pet filter** — pet with no tasks returns empty list

### Sample test output

## 📐 Smarter Scheduling

| Feature                     | Method(s)                               | Notes                                                                             |
| --------------------------- | --------------------------------------- | --------------------------------------------------------------------------------- |
| Sort by priority + duration | `Scheduler.sort_tasks_by_priority()`    | High priority first; shorter tasks first within same priority                     |
| Sort by time                | `Scheduler.sort_by_time()`              | Sorts scheduled tasks by HH:MM start time using lambda key                        |
| Filter by pet               | `Scheduler.filter_tasks(pet_name=...)`  | Returns only tasks assigned to a specific pet                                     |
| Filter by status            | `Scheduler.filter_tasks(completed=...)` | Returns only completed or incomplete tasks                                        |
| Conflict detection          | `Scheduler.detect_conflicts()`          | Flags tasks where start time falls before previous task ends                      |
| Recurring tasks             | `CareTask.mark_complete()`              | Returns a new CareTask due tomorrow (daily) or next week (weekly) using timedelta |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
