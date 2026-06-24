from pawpal_system import Owner, Pet, CareTask, Priority, Scheduler
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "diagrams"))

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "plan" not in st.session_state:
    st.session_state.plan = None

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=True):
    st.markdown("""
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
""")

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input(
    "Available time (minutes)", min_value=10, max_value=480, value=120)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input(
        "Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(
            duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        if st.session_state.owner is None or st.session_state.owner.name != owner_name:
            st.session_state.owner = Owner(
                name=owner_name, available_time_minutes=int(available_time))

        if st.session_state.pet is None or st.session_state.pet.name != pet_name:
            st.session_state.pet = Pet(name=pet_name, species=species)
            st.session_state.owner.add_pet(st.session_state.pet)

        priority_map = {"low": Priority.LOW,
                        "medium": Priority.MEDIUM, "high": Priority.HIGH}
        care_tasks = [
            CareTask(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=priority_map[t["priority"]],
                pet=st.session_state.pet
            )
            for t in st.session_state.tasks
        ]

        scheduler = Scheduler()
        st.session_state.plan = scheduler.create_daily_plan(
            care_tasks, st.session_state.owner)

if st.session_state.plan:
    st.success("Schedule generated!")
    st.markdown("### 📋 Today's Schedule")
    for task, start_time in st.session_state.plan.scheduled_tasks:
        st.markdown(
            f"- **{start_time}** — {task.title} ({task.duration_minutes} min) `{task.priority.name}`")
    if st.session_state.plan.unscheduled_tasks:
        st.warning("Could not fit these tasks:")
        for task in st.session_state.plan.unscheduled_tasks:
            st.markdown(f"- {task.title}")
    st.info(
        f"Total time used: {st.session_state.plan.total_time_used} min | {st.session_state.plan.explanation}")
