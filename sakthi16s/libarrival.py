import datetime

# Function to add a new student
def add_student(library_users):
    name = input("Enter the student's name: ")
    roll_no = input("Enter the roll number: ")
    
    if roll_no not in library_users:
        library_users[roll_no] = {'name': name, 'attendance': []}
        print(f"Student {name} with roll number {roll_no} added successfully.\n")
    else:
        print("Student with this roll number already exists.\n")

# Function to mark attendance for a student
def mark_attendance(library_users):
    roll_no = input("Enter the roll number of the student: ")
    
    if roll_no in library_users:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        library_users[roll_no]['attendance'].append(current_time)
        print(f"Attendance marked for {library_users[roll_no]['name']} at {current_time}.\n")
    else:
        print("Student not found! Please make sure the roll number is correct.\n")

# Function to view attendance records of a student
def view_attendance(library_users):
    roll_no = input("Enter the roll number of the student: ")
    
    if roll_no in library_users:
        name = library_users[roll_no]['name']
        attendance_records = library_users[roll_no]['attendance']
        
        if attendance_records:
            print(f"\nAttendance records for {name} (Roll No: {roll_no}):")
            for record in attendance_records:
                print(f"- {record}")
        else:
            print(f"No attendance records found for {name} (Roll No: {roll_no}).")
    else:
        print("Student not found! Please make sure the roll number is correct.\n")

# Function to display the main menu
def display_menu():
    print("Library Attendance System")
    print("1. Add New Student")
    print("2. Mark Attendance")
    print("3. View Attendance Records")
    print("4. Exit")

# Main function to run the system
def library_attendance_system():
    library_users = {}  # Dictionary to store student information and attendance
    
    while True:
        display_menu()
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            add_student(library_users)
        elif choice == '2':
            mark_attendance(library_users)
        elif choice == '3':
            view_attendance(library_users)
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.\n")

# Run the program
if __name__ == "__main__":
    library_attendance_system()
