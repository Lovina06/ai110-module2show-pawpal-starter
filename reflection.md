# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

**Core user actions:**

1. **Add and manage pet/owner information** - Users can enter basic details about themselves (name, available time) and their pet(s) (name, species, special needs).
2. **Create and edit care tasks** - Users can add specific care tasks such as walks, feeding, medications, grooming, or enrichment activities. Each task includes a duration (in minutes) and priority level (low, medium, high).
3. **Generate a daily schedule** - The system analyzes all tasks, considers the owner's available time and task priorities, then produces an optimized daily plan showing which tasks to do and in what order.

**Initial UML design:**

The initial design includes four main classes:

1. **Owner** - Represents the pet owner. Stores owner name and daily available time (in minutes). Responsible for knowing how much time is available for pet care.
2. **Pet** - Represents a pet. Stores pet name, species, and any special needs or preferences. Responsible for maintaining pet information.
3. **CareTask** - Represents a single care task (walk, feeding, medication, etc.). Stores task title, duration (minutes), and priority level (low/medium/high). Responsible for describing what needs to be done.
4. **Scheduler** - The scheduling engine. Takes a list of CareTask objects and the Owner's available time, then produces an optimized daily plan. Responsible for deciding which tasks to schedule and in what order based on priority and time constraints.

**b. Design changes**

Yes, the design changed during implementation.

**Design change: Added a DailyPlan class**

Initially, the Scheduler was designed to return a simple list of CareTask objects. However, during implementation, I realized this wasn't sufficient because:

- The schedule needed to include timing information (what time each task should happen)
- I needed to explain _why_ certain tasks were chosen or excluded
- The plan needed to track total time used vs. available time

**Solution:** I added a **DailyPlan** class that wraps the scheduled tasks and includes:

- A list of scheduled tasks with start times
- Total time allocated
- An explanation of the scheduling decisions
- Any tasks that couldn't fit in the available time

**Design change: Added missing relationships and validation (based on AI review)**

After reviewing the initial skeleton code with AI assistance, I identified several missing relationships and potential issues:

1. **Added Owner-Pet relationship**: The Owner class now includes a `pets: List[Pet]` attribute
2. **Added Pet-Task association**: CareTask now has an optional `pet: Optional[Pet]` field
3. **Replaced string priority with Enum**: Changed from `priority: str` to `priority: Priority`
4. **Added start time to Owner**: Added `start_time_hour: int` to specify when the day begins
5. **Added input validation**: Implemented `__post_init__()` methods in Owner and CareTask
6. **Added recurring and due_date fields**: CareTask now supports daily/weekly recurrence using `timedelta`

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints:

- **Time budget** — The owner's `available_time_minutes` is the hard limit. Tasks that don't fit are moved to `unscheduled_tasks`.
- **Priority** — Tasks are sorted HIGH → MEDIUM → LOW using the `Priority` enum's numeric value.
- **Duration** — Within the same priority level, shorter tasks are scheduled first to maximize the number of tasks that fit.

I decided priority mattered most because a pet's health needs (feeding, medication) should never be skipped due to time — they should always be scheduled before lower-priority enrichment tasks like playtime.

## 2b. Tradeoffs

The `detect_conflicts` method checks whether a task's start time falls before the previous task ends.
This is simple and readable but has a limitation: it assumes tasks are scheduled sequentially and
only compares adjacent pairs. A more robust approach would build a full timeline and check all
overlapping windows — but for a daily pet care schedule with 5-10 tasks, this simpler version
is fast enough and easier to maintain.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude as an AI coding assistant throughout the project across several areas:

- **Design brainstorming** — Asked Claude to review my UML and identify missing relationships (e.g., the Pet-Task link and Priority enum)
- **Code generation** — Used Claude to generate class stubs, method implementations, and the full test suite
- **Debugging** — When pytest collected 0 items or `sys.path` errors appeared, Claude helped diagnose the root cause quickly
- **Refactoring** — Asked Claude to suggest a more Pythonic version of `detect_conflicts` using `itertools.combinations`

The most helpful prompts were specific ones like: _"Here is my current `detect_conflicts` method — how could this be simplified for better readability or performance?"_ rather than vague ones like _"improve my code."_

**b. Judgment and verification**

When Claude suggested replacing `detect_conflicts` with an `itertools.combinations` version, I evaluated both versions side by side. The `itertools` version was more concise but harder to read for someone new to Python. Since this is a learning project and readability matters more than cleverness here, I kept the original nested loop version. This was a deliberate tradeoff — I chose the version a junior developer could understand and maintain over the "more Pythonic" one.

I also rejected Claude's initial suggestion to use `cat > file << 'EOF'` in the terminal for editing files, since it kept causing heredoc issues on my Mac. I switched to editing files directly in VS Code instead.

Using **separate chat sessions** for different phases (design, implementation, testing, reflection) helped me stay focused. Each session had a clear scope and I wasn't dragging unrelated context from earlier phases into later ones. It also helped me treat each phase as a fresh problem rather than continuing to patch the same growing conversation.

---

## 4. Testing and Verification

**a. What you tested**

I wrote 14 automated tests covering:

- **Task completion** — `mark_complete()` sets `completed` to `True`
- **Pet task list** — `add_task()` increases the pet's task count
- **Sorting by priority** — HIGH priority tasks come before LOW
- **Sorting by time** — `sort_by_time()` returns tasks in chronological HH:MM order
- **Priority + duration sort** — shorter tasks first within the same priority
- **Filter by pet name** — only tasks for the named pet are returned
- **Filter by completion status** — completed/incomplete tasks filtered correctly
- **Daily recurring** — completing a daily task creates next task due tomorrow
- **Weekly recurring** — completing a weekly task creates next task due next week
- **Non-recurring** — completing a one-off task returns `None`
- **No conflicts** — sequential tasks produce no conflict warnings
- **Zero time budget** — owner with 0 minutes schedules nothing
- **Empty pet filter** — filtering for a pet with no tasks returns an empty list

These tests mattered because they verified both happy paths and edge cases. Without them, bugs in recurring logic or filtering could go unnoticed until a user hit them in production.

**b. Confidence**

⭐⭐⭐⭐⭐ — All 14 tests pass. I'm confident in the core scheduling, sorting, filtering, and recurring logic.

If I had more time, I would test:

- Two tasks with the exact same start time (hard conflict)
- An owner with 1 minute available (boundary case)
- A pet with 20+ tasks to check performance
- Recurring tasks completing multiple times in sequence

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the recurring task logic. The idea that `mark_complete()` returns a new `CareTask` object with a `due_date` calculated using `timedelta` felt elegant — the task itself knows how to create its own successor. It also made the tests clean and easy to write.

The test suite is also something I'm proud of — 14 tests covering sorting, filtering, edge cases, and recurrence gave me real confidence that the system works correctly.

**b. What you would improve**

If I had another iteration, I would:

- Add a proper database or JSON file to persist tasks between sessions (right now everything resets on Streamlit reload)
- Improve conflict detection to handle non-sequential overlaps
- Add support for task time windows (e.g., "Feeding must happen between 7–9 AM")
- Build a multi-pet view in the UI so each pet's schedule is shown separately

**c. Key takeaway**

The most important thing I learned is that **AI is a powerful collaborator, but the architect's judgment still matters**. Claude could generate code quickly, but it couldn't decide which tradeoffs were right for my project — only I could. Every suggestion had to be evaluated: Is this readable? Does it fit my design? Does it solve the right problem?

Being the "lead architect" meant I had to understand the code well enough to accept, reject, or modify what the AI produced. The moments where I pushed back — keeping the readable `detect_conflicts` over the `itertools` version, fixing the `sys.path` issue myself in VS Code instead of using `cat` in terminal — were the moments where I learned the most. AI accelerates the work, but the human has to stay in the driver's seat.
