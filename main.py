import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
import os

# Configure page
st.set_page_config(
    page_title="Task Manager Dashboard",
    page_icon="✅",
    layout="wide"
)

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Helper functions
def get_all_tasks():
    try:
        response = requests.get(f"{API_URL}/tasks")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tasks: {str(e)}")
        return []

def create_task(title, description="", is_completed=False):
    try:
        payload = {
            "title": title,
            "description": description,
            "is_completed": is_completed
        }
        response = requests.post(f"{API_URL}/tasks", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating task: {str(e)}")
        return None

def update_task(task_id, title, description, is_completed):
    try:
        payload = {
            "title": title,
            "description": description,
            "is_completed": is_completed
        }
        response = requests.put(f"{API_URL}/tasks/{task_id}", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating task: {str(e)}")
        return None

def delete_task(task_id):
    try:
        response = requests.delete(f"{API_URL}/tasks/{task_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting task: {str(e)}")
        return False

def format_datetime(dt_string):
    dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
    return dt.strftime("%Y-%m-%d %H:%M")

# App header
st.title("✅ Task Manager Dashboard")
st.markdown("Manage your tasks easily with this interactive dashboard.")

# Sidebar
st.sidebar.header("Task Manager")
api_status = st.sidebar.empty()

# Check API connection
try:
    health_response = requests.get(f"{API_URL}/health")
    if health_response.status_code == 200:
        api_status.success("API Connection: Online ✅")
    else:
        api_status.error("API Connection: Error ❌")
except requests.exceptions.RequestException:
    api_status.error(f"API Connection: Failed to connect to {API_URL} ❌")

# Add task section
st.sidebar.subheader("Add New Task")
with st.sidebar.form("new_task_form", clear_on_submit=True):
    new_task_title = st.text_input("Task Title", max_chars=100)
    new_task_desc = st.text_area("Description", max_chars=500)
    new_task_completed = st.checkbox("Mark as completed")
    
    submit_button = st.form_submit_button("Add Task")
    
    if submit_button and new_task_title:
        result = create_task(new_task_title, new_task_desc, new_task_completed)
        if result:
            st.success("Task added successfully!")
            st.rerun()
    elif submit_button:
        st.warning("Task title cannot be empty!")

# Dashboard layout
tab1, tab2 = st.tabs(["📋 Task List", "📊 Task Statistics"])

# Task List Tab
with tab1:
    st.subheader("All Tasks")
    refresh_button = st.button("Refresh Tasks")
    
    if refresh_button:
        st.rerun()
    
    tasks = get_all_tasks()
    
    if not tasks:
        st.info("No tasks found. Add a task using the sidebar form.")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_status = st.selectbox(
                "Filter by Status",
                ["All", "Completed", "Pending"]
            )
        
        # Apply filters
        filtered_tasks = tasks
        if filter_status == "Completed":
            filtered_tasks = [task for task in tasks if task["is_completed"]]
        elif filter_status == "Pending":
            filtered_tasks = [task for task in tasks if not task["is_completed"]]
        
        # Display tasks
        for task in filtered_tasks:
            with st.expander(f"{task['title']} {'✅' if task['is_completed'] else '🔄'}"):
                task_col1, task_col2 = st.columns([3, 1])
                
                with task_col1:
                    edited_title = st.text_input("Title", task["title"], key=f"title_{task['id']}")
                    edited_desc = st.text_area("Description", task["description"] or "", key=f"desc_{task['id']}")
                    edited_status = st.checkbox("Completed", task["is_completed"], key=f"status_{task['id']}")
                    
                    created_at = format_datetime(task["created_at"])
                    updated_at = format_datetime(task["updated_at"])
                    
                    st.caption(f"Created: {created_at} | Last Updated: {updated_at}")
                
                with task_col2:
                    st.markdown("### Actions")
                    
                    # Check if anything changed
                    task_changed = (
                        edited_title != task["title"] or
                        edited_desc != (task["description"] or "") or
                        edited_status != task["is_completed"]
                    )
                    
                    if task_changed:
                        if st.button("Save Changes", key=f"save_{task['id']}"):
                            updated = update_task(
                                task["id"],
                                edited_title,
                                edited_desc,
                                edited_status
                            )
                            if updated:
                                st.success("Task updated successfully!")
                                st.rerun()
                    
                    if st.button("Delete Task", key=f"delete_{task['id']}"):
                        deleted = delete_task(task["id"])
                        if deleted:
                            st.success("Task deleted successfully!")
                            st.rerun()

# Task Statistics Tab
with tab2:
    st.subheader("Task Statistics")
    
    if not tasks:
        st.info("No tasks available for statistics.")
    else:
        # Create stats
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task["is_completed"])
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tasks", total_tasks)
        col2.metric("Completed", completed_tasks)
        col3.metric("Pending", pending_tasks)
        col4.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        # Create dataframe for charts
        df = pd.DataFrame([
            {"Status": "Completed", "Count": completed_tasks},
            {"Status": "Pending", "Count": pending_tasks}
        ])
        
        # Display charts
        st.subheader("Task Status Distribution")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.bar_chart(df.set_index("Status"))
        
        with chart_col2:
            st.pie_chart(df.set_index("Status"))
        
        # Add recent activity table
        st.subheader("Recent Tasks")
        
        # Sort tasks by updated_at (most recent first)
        sorted_tasks = sorted(tasks, key=lambda x: x["updated_at"], reverse=True)[:5]
        
        if sorted_tasks:
            recent_data = []
            for task in sorted_tasks:
                recent_data.append({
                    "Title": task["title"],
                    "Status": "Completed" if task["is_completed"] else "Pending",
                    "Last Updated": format_datetime(task["updated_at"])
                })
            
            st.table(pd.DataFrame(recent_data))

# Footer
st.markdown("---")
st.markdown("Task Manager Dashboard | Powered by FastAPI & Streamlit")
