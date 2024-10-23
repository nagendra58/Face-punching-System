import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Function to calculate work hours from check-in and check-out times
def calculate_work_hours(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

    # Create an empty list to store work hours data
    work_hours_list = []

    # Group data by Employee Name and Date
    for name, group in df.groupby(['Employee Name', 'Date']):
        check_in_times = group[group['Status'] == 'Check-in']['Time']
        check_out_times = group[group['Status'] == 'Check-out']['Time']

        # Calculate total work hours (only if both check-in and check-out exist)
        if not check_in_times.empty and not check_out_times.empty:
            check_in = datetime.combine(group['Date'].iloc[0], check_in_times.iloc[0])
            check_out = datetime.combine(group['Date'].iloc[0], check_out_times.iloc[0])
            work_duration = round((check_out - check_in).total_seconds() / 3600, 2)  # Convert seconds to hours and round to 2 decimals
            work_hours_list.append({'Employee Name': name[0], 'Date': name[1], 'Work Hours': work_duration})

    # Convert list to DataFrame
    work_hours_df = pd.DataFrame(work_hours_list)
    return work_hours_df

# Function to generate daily, weekly, and monthly reports
def generate_attendance_reports(work_hours_df):
    folder_path = 'Attendance_reports'
    os.makedirs(folder_path, exist_ok=True)

    # Generate daily report
    daily_report = work_hours_df.groupby(['Employee Name', 'Date'])['Work Hours'].sum().reset_index()
    daily_report.to_csv(os.path.join(folder_path, 'daily_report.csv'), index=False)

    # Generate weekly report
    work_hours_df['Week'] = work_hours_df['Date'].dt.strftime('%Y-%U')  # %U is the week number
    weekly_report = work_hours_df.groupby(['Employee Name', 'Week'])['Work Hours'].sum().reset_index()
    weekly_report.to_csv(os.path.join(folder_path, 'weekly_report.csv'), index=False)

    # Generate monthly report
    work_hours_df['Month'] = work_hours_df['Date'].dt.strftime('%Y-%m')
    monthly_report = work_hours_df.groupby(['Employee Name', 'Month'])['Work Hours'].sum().reset_index()
    monthly_report.to_csv(os.path.join(folder_path, 'monthly_report.csv'), index=False)

# Function to generate bar graphs for daily, weekly, and monthly work hours
def generate_attendance_graphs(work_hours_df):
    graph_folder_path = os.path.join('Attendance_reports', 'graph_reports')
    os.makedirs(graph_folder_path, exist_ok=True)

    # Daily bar graph
    daily_report = work_hours_df.groupby(['Employee Name', 'Date'])['Work Hours'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    for name in daily_report['Employee Name'].unique():
        employee_data = daily_report[daily_report['Employee Name'] == name]
        plt.bar(employee_data['Date'].astype(str), employee_data['Work Hours'], label=name)  # Bar chart
    plt.title('Daily Work Hours')
    plt.xlabel('Date')
    plt.ylabel('Work Hours')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder_path, 'daily_work_hours.png'))
    plt.close()

    # Weekly bar graph
    weekly_report = work_hours_df.groupby(['Employee Name', 'Week'])['Work Hours'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    for name in weekly_report['Employee Name'].unique():
        employee_data = weekly_report[weekly_report['Employee Name'] == name]
        plt.bar(employee_data['Week'], employee_data['Work Hours'], label=name)  # Bar chart
    plt.title('Weekly Work Hours')
    plt.xlabel('Week')
    plt.ylabel('Work Hours')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder_path, 'weekly_work_hours.png'))
    plt.close()

    # Monthly bar graph
    monthly_report = work_hours_df.groupby(['Employee Name', 'Month'])['Work Hours'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    for name in monthly_report['Employee Name'].unique():
        employee_data = monthly_report[monthly_report['Employee Name'] == name]
        plt.bar(employee_data['Month'], employee_data['Work Hours'], label=name)  # Bar chart
    plt.title('Monthly Work Hours')
    plt.xlabel('Month')
    plt.ylabel('Work Hours')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder_path, 'monthly_work_hours.png'))
    plt.close()
    print("Reports and Graphs generated.")

# Load the attendance CSV file
def main():
    try:
        attendance_df = pd.read_csv("attendance.csv")
    except FileNotFoundError:
        print("attendance.csv not found.")
        return

    # Calculate work hours
    work_hours_df = calculate_work_hours(attendance_df)

    # Generate reports
    generate_attendance_reports(work_hours_df)

    # Generate bar graphs
    generate_attendance_graphs(work_hours_df)

# Run the main function
if __name__ == "__main__":
    main()