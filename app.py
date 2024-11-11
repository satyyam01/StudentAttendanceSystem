import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("Student Attendance Viewer")

# Get list of attendance files
attendance_dir = "attendance"
if not os.path.exists(attendance_dir):
    st.error("No attendance records found!")
else:
    attendance_files = [f for f in os.listdir(attendance_dir) if f.endswith('.csv')]

    if not attendance_files:
        st.warning("No attendance records available")
    else:
        # Date selector
        selected_date = st.selectbox(
            "Select Date",
            attendance_files,
            format_func=lambda x: x.split('.')[0]
        )

        # Load and display attendance data
        if selected_date:
            df = pd.read_csv(os.path.join(attendance_dir, selected_date))

            # Display statistics
            st.subheader("Attendance Statistics")
            total_students = len(df)
            st.write(f"Total Students Present: {total_students}")

            # Display attendance table
            st.subheader("Attendance Records")
            st.dataframe(df)

            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=selected_date,
                mime='text/csv',
            )