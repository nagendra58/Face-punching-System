import pandas as pd
import os
from datetime import datetime

# Function to generate attendance report for a specific date
def generate_daily_attendance_report():
    # Read the attendance CSV file
    try:
        df = pd.read_csv("attendance.csv")
    except FileNotFoundError:
        print("Attendance CSV file not found.")
        return
    
    # Convert the 'Date' column to datetime for easier manipulation
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Get the unique dates from the CSV file
    unique_dates = df['Date'].dt.date.unique()
    
    # Iterate over each unique date
    for date in unique_dates:
        # Filter the data for that specific date
        daily_data = df[df['Date'].dt.date == date]
        
        # Get the list of unique employees for that date
        employees = daily_data['Employee Name'].unique()

        # Create a dictionary to store attendance status
        attendance_status = {}

        # Loop over each employee
        for employee in employees:
            employee_data = daily_data[daily_data['Employee Name'] == employee]
            
            # Check if there is both check-in and check-out for that employee
            check_in_exists = any(employee_data['Status'] == 'Check-in')
            check_out_exists = any(employee_data['Status'] == 'Check-out')
            
            # If both check-in and check-out exist, mark as 'Present', else 'Absent'
            if check_in_exists and check_out_exists:
                attendance_status[employee] = 'Present'
            else:
                attendance_status[employee] = 'Absent'

        # Create a DataFrame from the attendance status
        attendance_report_df = pd.DataFrame(list(attendance_status.items()), columns=['Employee Name', 'Status'])

        # Save the report to a new CSV file in 'attendance_logs' folder
        folder_path = 'attendance_logs'
        os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists
        report_file_path = os.path.join(folder_path, f"{date}_attendance.csv")
        attendance_report_df.to_csv(report_file_path, index=False)

        print(f"Attendance report generated for {date}: {report_file_path}")

# Run the function to generate daily attendance reports
generate_daily_attendance_report()