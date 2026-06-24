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
- An explanation of the scheduling decisions (e.g., "High priority tasks scheduled first")
- Any tasks that couldn't fit in the available time

This made the Scheduler's output more informative and easier for the UI to display.

**Design change: Added missing relationships and validation (based on AI review)**

After reviewing the initial skeleton code with AI assistance, I identified several missing relationships and potential issues:

1. **Added Owner-Pet relationship**: The Owner class now includes a `pets: List[Pet]` attribute to track which pets they own, matching the UML relationship "Owner owns 1..\* Pet"

2. **Added Pet-Task association**: CareTask now has an optional `pet: Optional[Pet]` field to link tasks to specific pets. This is important for multi-pet households where you need to track which task belongs to which pet.

3. **Replaced string priority with Enum**: Changed from `priority: str` to `priority: Priority` using an Enum (LOW=1, MEDIUM=2, HIGH=3). This prevents typos and makes priority comparison more reliable.

4. **Added start time to Owner**: Added `start_time_hour: int` to specify when the day begins (e.g., 8 AM), which is needed to calculate actual clock times for scheduled tasks.

5. **Added input validation**: Implemented `__post_init__()` methods in Owner and CareTask to validate data (e.g., no negative durations, valid hour ranges).

6. **Clarified time format**: Documented that start times in DailyPlan should use "HH:MM" format (e.g., "08:30") for consistency.

**Why these changes mattered**: The initial design had the right classes but missed important relationships between them. Without linking tasks to pets, the system couldn't handle multi-pet scenarios. Using strings for priority was error-prone. These changes made the system more robust and better matched real-world requirements.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

## 2b. Tradeoffs

The `detect_conflicts` method checks whether a task's start time falls before the previous task ends.
This is simple and readable but has a limitation: it assumes tasks are scheduled sequentially and
only compares adjacent pairs. A more robust approach would build a full timeline and check all
overlapping windows — but for a daily pet care schedule with 5-10 tasks, this simpler version
is fast enough and easier to maintain.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
