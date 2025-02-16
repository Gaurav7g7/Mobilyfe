import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_calendar import calendar

# Page configuration
st.set_page_config(page_title="Mobilyfe Calendar", page_icon="📆")

# Title and description
st.title("Mobilyfe")
st.markdown("## Your Time, Your Mind, Your Lyfe")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Calendar", "Health Dashboard"])

# Calendar page
if page == "Calendar":
    st.markdown("### Calendar 📆")
    mode = st.selectbox(
        "Calendar Mode:",
        (
            "daygrid",
            "timegrid",
            "timeline",
            "resource-daygrid",
            "resource-timegrid",
            "resource-timeline",
            "list",
            "multimonth",
        ),
    )

    events = [
        {"title": "Event 1", "color": "#FF6C6C", "start": "2023-07-03", "end": "2023-07-05", "resourceId": "a"},
        {"title": "Event 2", "color": "#FFBD45", "start": "2023-07-01", "end": "2023-07-10", "resourceId": "b"},
        # Add more events as needed
    ]
    calendar_resources = [
        {"id": "a", "building": "Building A", "title": "Room A"},
        {"id": "b", "building": "Building A", "title": "Room B"},
        # Add more resources as needed
    ]

    calendar_options = {
        "editable": "true",
        "navLinks": "true",
        "resources": calendar_resources,
        "selectable": "true",
    }

    if "resource" in mode:
        if mode == "resource-daygrid":
            calendar_options.update({
                "initialDate": "2023-07-01",
                "initialView": "resourceDayGridDay",
                "resourceGroupField": "building",
            })
        elif mode == "resource-timeline":
            calendar_options.update({
                "headerToolbar": {"left": "today prev,next", "center": "title", "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth"},
                "initialDate": "2023-07-01",
                "initialView": "resourceTimelineDay",
                "resourceGroupField": "building",
            })
        elif mode == "resource-timegrid":
            calendar_options.update({
                "initialDate": "2023-07-01",
                "initialView": "resourceTimeGridDay",
                "resourceGroupField": "building",
            })
    else:
        if mode == "daygrid":
            calendar_options.update({
                "headerToolbar": {"left": "today prev,next", "center": "title", "right": "dayGridDay,dayGridWeek,dayGridMonth"},
                "initialDate": "2023-07-01",
                "initialView": "dayGridMonth",
            })
        elif mode == "timegrid":
            calendar_options.update({"initialView": "timeGridWeek"})
        elif mode == "timeline":
            calendar_options.update({
                "headerToolbar": {"left": "today prev,next", "center": "title", "right": "timelineDay,timelineWeek,timelineMonth"},
                "initialDate": "2023-07-01",
                "initialView": "timelineMonth",
            })
        elif mode == "list":
            calendar_options.update({"initialDate": "2023-07-01", "initialView": "listMonth"})
        elif mode == "multimonth":
            calendar_options.update({"initialView": "multiMonthYear"})

    state = calendar(
        events=st.session_state.get("events", events),
        options=calendar_options,
        custom_css="""
        .fc-event-past { opacity: 0.8; }
        .fc-event-time { font-style: italic; }
        .fc-event-title { font-weight: 700; }
        .fc-toolbar-title { font-size: 2rem; }
        """,
        key=mode,
    )

    if state.get("eventsSet") is not None:
        st.session_state["events"] = state["eventsSet"]

    st.write(state)

# Health Dashboard page
elif page == "Health Dashboard":
    st.markdown("### Health Dashboard 📊")

    # Input fields for user data
    bpm = st.number_input("Enter your heart rate (BPM):", min_value=0)
    steps = st.number_input("Enter your steps for the day:", min_value=0)
    sleep = st.number_input("Enter your sleep duration (hours):", min_value=0.0, step=0.1)
    meditation = st.number_input("Enter your meditation duration (minutes):", min_value=0)

    # Store the input data
    if "health_data" not in st.session_state:
        st.session_state["health_data"] = []

    if st.button("Submit"):
        st.session_state["health_data"].append({
            "date": pd.Timestamp.now().date(),
            "bpm": bpm,
            "steps": steps,
            "sleep": sleep,
            "meditation": meditation,
        })
        st.success("Data submitted successfully!")

    # Display the input data
    st.write("### Today's Data")
    st.write(f"Heart Rate: {bpm} BPM")
    st.write(f"Steps: {steps}")
    st.write(f"Sleep: {sleep} hours")
    st.write(f"Meditation: {meditation} minutes")

    # Calculate weekly averages
    if st.session_state["health_data"]:
        df = pd.DataFrame(st.session_state["health_data"])
        df["date"] = pd.to_datetime(df["date"])
        last_week = df[df["date"] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]

        if not last_week.empty:
            weekly_averages = last_week.mean(numeric_only=True)

            st.write("### Weekly Averages")
            st.write(f"Heart Rate: {weekly_averages['bpm']:.2f} BPM")
            st.write(f"Steps: {weekly_averages['steps']:.2f}")
            st.write(f"Sleep: {weekly_averages['sleep']:.2f} hours")
            st.write(f"Meditation: {weekly_averages['meditation']:.2f} minutes")

            # Convert date format to month abbreviated-day (e.g., Jan-15)
            last_week["date"] = last_week["date"].dt.strftime('%b-%d')

            # Plotting the data as a bar chart with pastel colors
            st.write("### Weekly Data Chart")
            sns.set_palette("pastel")
            fig, ax = plt.subplots()
            last_week.set_index("date").plot(kind='bar', ax=ax)
            st.pyplot(fig)

           

# API reference
st.markdown("## API reference")
st.help(calendar)

st.write(
    "Thank you Hacklahoma! -Gaurav, Maya, Simon, and Houston"
)
