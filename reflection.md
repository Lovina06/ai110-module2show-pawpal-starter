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
- I needed to explain *why* certain tasks were chosen or excluded
- The plan needed to track total time used vs. available time

**Solution:** I added a **DailyPlan** class that wraps the scheduled tasks and includes:
- A list of scheduled tasks with start times
- Total time allocated
- An explanation of the scheduling decisions (e.g., "High priority tasks scheduled first")
- Any tasks that couldn't fit in the available time

This made the Scheduler's output more informative and easier for the UI to display.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

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
