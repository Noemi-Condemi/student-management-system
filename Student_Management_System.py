import json
import os


# ---- Constants & Data ----

DATA_FILE ="student_database.json"
students_db = []


# ---- Database Functions ----

# *** LOAD DATABASE FROM FILE ***

def load_database(filename = DATA_FILE):
    """Load the student database from a JSON file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return []
    return []
        

# *** SAVE DATABASE TO FILE ***

def save_database(students, filename = DATA_FILE):
    """Save students_db to JSON file"""
    with open(filename, "w") as f:
        json.dump(students, f, indent=4) 


# ---- Main Program ----

def main():
    students_db = load_database()

    print("\n" + "="*70)
    print(("WELCOME TO THE STUDENT MANAGEMENT SYSTEM").center(70))
    print("="*70)

    while True:
        display_menu()
        choice = input("\n Enter your choice (1 - 15): " ).strip()

        #"1. Add Student"
        if choice =="1":
            add_student_flow(students_db)
            save_database(students_db)

        #"2. Add Score"
        elif choice == "2":
            add_score(students_db)
            save_database(students_db)
            
        #"3. List All Students"
        elif choice == "3":
            list_all_students()

        # "4. Sort Students"
        elif choice == "4":
            sort_students()

        #"5. Display Student Report"
        elif choice == "5":
            display_student_report()

        #"6. Find Student by Name"
        elif choice == "6":
            name_input = input("\n Enter Student's Name: ").strip()
            result = find_students_by_name(name_input)

            if result:
                print_student_table(result)
            else:
                print("No students found.")
            
        #"7. Find Student by Address"
        elif choice == "7":
            address_input = input("\n Enter Student's Address: ")
            result = find_students_by_address(address_input)
            print_student_table(result)

        #"8. Find Student by Phone"
        elif choice == "8":
            phone_input = input("\n Enter Student's Phone: ")
            result = find_students_by_phone(phone_input)
            print_student_table(result)

        #"9. Find Student by ID"
        elif choice == "9":
            student_id = get_valid_student_id(students_db)
            student = get_student_by_id(student_id)
            print_student_table([student] if student else [])

        #"10. Find Top Student"
        elif choice == "10":
            result = find_top_student()
            if isinstance(result, dict):
                print_student_table([result])
            else:
                print(result)
        
        #"11. Calculate Average"
        elif choice == "11":
            student_id = get_valid_student_id(students_db)
            student = get_student_by_id(student_id)

            if student:
                avg = calculate_average(student_id)
                print(f"{student['name'] } average score is {avg:.2f}")
            else:
                print("Student not found!")    

        #"12. List Students Above Average"
        elif choice == "12":
            list_above_average()    

        # "13. Update Student"
        elif choice == "13":
            student_id = get_valid_student_id(students_db)
            student = get_student_by_id(student_id)
            if not student:
                print("Student not found!")
                continue

            field_input = input("\n Which field would you like to update: Name, Age, Address, Email, Phone, Subjects, Notes: ").lower()
            allowed_fields = ['name', 'age', 'address', 'email', 'phone', 'subjects', 'notes']
            
            if field_input not in allowed_fields:
                print("Invalid field")
                continue

            new_value = input("\n Enter the new value: ")
            update_student(student_id, **{field_input: new_value})
            save_database(students_db)
                
            print("Updated completed!")

        #"14. Remove Student"
        elif choice == "14":
            student_id = get_valid_student_id(students_db)
            removed_student = remove_student(student_id)

            if removed_student:
                save_database(students_db)
            
        #"15. Exit"
        elif choice == "15":
            print("Thank you for using our system.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 15.")
            
    
# *** GENERATE ID ***
def generate_student_id(students):
    """GEnerate a unique student ID"""
    if not students:
        return 1
    
    highest_id = max(student['id'] for student in students)
    return highest_id + 1


# *** ID VALIDATION ***

def get_valid_student_id(students):
    """Prompt user for a valid student ID and return it."""
    
    while True:
        id_input_user =input("\n Enter Student ID: ").strip()
      
        try:
            id_input_user = int(id_input_user)    
        except ValueError:
            print(f"Invalid Student ID : '{id_input_user}'. Please enter a number.")
            continue

        student = next((s for s in students if s['id'] == id_input_user), None) # next() takes a generator and gives you the first value it produces.
        if not student:
            print(f"Student with ID {id_input_user} not found!")
            continue  

        return id_input_user 
    
def name_validation():
    """Ask the user for a full name until a non-empty value is given."""
    
    while True:
        student_name = input("Full Name: ").strip()
        if student_name == "":
            print(" Name cannot be empty. Please enter a valid name.")
        else:
            return student_name
    
def age_validation():
    """Prompt the user to enter a valid age between 16 and 100."""
    while True:
        try:
            student_age = int(input("Age: "))
            if 16 <= student_age <= 100:
                return student_age
            else:
                print("Age must be between 16 and 100")
        except ValueError:
            print("Invalid input. Please enter a number.")


# *** ADD STUDENT ***

def add_student_flow(students):
    """Collect student information and add to the students list"""
   
    print("\n -----Add Full Name-----")
    student_name = name_validation()

    print("\n -----Add Age-----")
    student_age = age_validation()

    print("\n -----Add Address----- ")
    student_address = input("Address: ").strip()

    print("\n -----Add Email-----")
    student_email = input("Email: ").strip()

    print("\n -----Add Phone Number-----")   
    student_phone = input("Phone Number: ").strip()
    
    print("\n -----Add Subjects-----")
    student_subjects = input("Subjects (comma separated): ").split(",")
    student_subjects = [s.strip().lower() for s in student_subjects if s.strip()]
    
    print("\n -----Add Notes (Optional)-----")
    student_notes = input("Additional notes (optional): ").strip()

    add_students(
        students, 
        student_name, 
        student_age, 
        student_address, 
        student_email, 
        student_phone, 
        student_subjects, 
        notes=student_notes
        )
    
    print(f"Student '{student_name}' added successfully!")


def add_students(name:str, age:int, address:str, email:str, phone:str, subjects:list, notes:str ) -> dict: 
    student = {
        "id" : generate_student_id(students_db),
        "name": name,
        "age" : age,
        "address" : address,
        "email" : email,
        "phone" : phone,
        "subjects": subjects,
        "score": {},
        "notes": notes,
    }
    students_db.append(student)
    return(student)


# *** ADD STUDENT'S SCORE ***

def add_score_flow(students):
    """Prompt the userr to add a score for a student."""

    student_id = get_valid_student_id(students)
    student = get_student_by_id(student_id)
    
    while True:
    
        subject_input = input("\n Which subject do you want to add a score for? ").strip().lower()
        if subject_input in student['subjects']:
            break
        print(f"{subject_input} is not in the student's subjects. Please try again.")
                
    while True:
        try:
            score_input = float(input("Enter score: "))
            if score_input < 0:
                print("Score cannot be negative.")
                continue
            break
        except ValueError:
            print(f"Invalid input. Please enter a decimal number.")

    if add_score(student_id, score_input, subject_input):
        print(f"Added score {score_input} for {subject_input} to {student['name']}")
    else:
        print("Failed to add score. Something went worng.")    
   

def add_score(student_id: int, score:float, subject:str )-> bool:
    for student in students_db:
        if student["id"] == student_id:
            if subject not in student['subjects']:
                return False
            
            if subject not in student['score']:
                student["score"][subject]= []
            student["score"][subject].append(score)
            return True
    return False


# *** LIST ALL STUDENTS ***

def list_all_students(students=None) -> None:
    """Print a concise table of all students with average."""
    if students is None:
        students = students_db

    print("\n" + "=" * 70)
    print("ALL STUDENTS".center(70))
    print( "=" * 70)
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Avg':<8} {'Phone':<12} {'Email':<25}")    
    print( "=" * 70)

    for student in students:
        avg = calculate_average(student['id'])
        print(f"{student['id']:<5} {student['name']:<20} {student['age']:<5} {avg:<8.2f} {student['phone']:<12} {student['email']:<25}")
    
    print("=" * 70)


# *** STUDENT TABLE ***

def print_student_table(student_list):
    """Print a table for a list of students."""
    if not student_list:
        print("No students found.")
        return

    print("\n" + "=" * 70)
    print("SEARCH RESULT".center(70))
    print( "=" * 70)
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Avg':<8} {'Phone':<12} {'Email':<25}")    
    print( "=" * 70)

    for student in student_list:
        avg = calculate_average(student['id'])
        print(f"{student['id']:<5} {student['name']:<20} {student['age']:<5} {avg:<8.2f} {student['phone']:<12} {student['email']:<25}")

    print( "=" * 70)

# *** SORT STUDENTS ***

def sort_students():

    while True:
        sort_field = input("\n Sort by (name / age / average): ").strip().lower()
        if sort_field in ['name', 'age', 'average']:
            break
        print("Invalid choice. Please choose name, age, or average.")

    if sort_field == 'name' :
        students_sorted = sorted(students_db, key = lambda student: student['name'])

    elif sort_field == 'age':
        students_sorted = sorted(students_db, key = lambda student: student['age'])

    elif sort_field == 'average':
        students_sorted = sorted(students_db, key = lambda student: calculate_average(student['id']), reverse = True)
    
    print_student_table(students_sorted)    
    

# *** DISPLAY STUDENT ***

def display_student(student_id: int) -> None:
    for student in students_db:
        if student["id"] == student_id:
            print("\n" + "=" * 70)
            print(f"{'Student ID':<10}: {student['id']}")
            print(f"{'Name':<10}: {student['name']}")
            print(f"{'Age':<10}: {student['age']}")
            print(f"{'Address':<10}: {student['address']}")
            print(f"{'Email':<10}: {student['email']}")
            print(f"{'Phone':<10}: {student['phone']}")
           
            for subject in student['subjects']:
                scores = student['score'].get(subject) 
                scores_str = ', '.join(str(s) for s in scores) if scores else ''
                print(f"{subject.upper():<12}: {scores_str}")
                
         
            avg = calculate_average(student['id'])
            print(f"{'Average':<10}: {avg:.2f}")
            
            if student['notes']:
                print(f"{'Notes':<10}: {student['notes']}")

            print("\n" + "=" *70)
            return
    print(f"Student with ID {student_id} does not exist!")  


# *** DISPLAY STUDENT REPORT ***

def display_student_report():
    """Show a detailed report for one student, including subjects, scores, and notes."""
    student_id = get_valid_student_id(students_db)
    student = get_student_by_id(student_id)

    if not student:
        print("Student not found!")
        return
    
    avg = calculate_average(student['id'])

    print("\n" + "=" * 70)
    print(f"STUDENT REPORT: {student['name']} ".center(70))
    print("=" * 70)
    print(f"{'ID':<10}: {student['id']}")
    print(f"{'Name':<10}: {student['name']}")
    print(f"{'Age':<10}: {student['age']}") 
    print(f"{'Phone':<10}: {student['phone']}")
    print(f"{'Email':<10}: {student['email']}")
    print(f"{'Average':<10}: {avg:.2f}") 
    print("\nSubjects & Scores:")

    for subject in student['subjects']:
        scores = student['score'].get(subject, [])
        scores_str = ', '.join(str(s) for s in scores)
        print(f"{subject.upper():<12}: {scores_str}")

    if student['notes']:
        print(f"\nNotes: {student['notes']}")
    print("=" * 70)


# *** FIND STUDENT BY NAME ***

def find_students_by_name(name:str):

    search_name = name.lower().strip()
    matching_students = []

    for student in students_db:        
        if search_name in student["name"].lower():
            matching_students.append(student)
            
    return matching_students


# *** Find Student by Address ***

def find_students_by_address(address:str):

    search_address = address.lower().strip()
    matching_students = []

    for student in students_db:        
        if search_address in student["address"].lower():
            matching_students.append(student)
            
    return matching_students

# *** Find Student by Phone ***
        
def find_students_by_phone(phone:str):

    search_phone = phone.strip()
    matching_students = []

    for student in students_db:        
        if search_phone in student["phone"]:
            matching_students.append(student)
            
    return matching_students


# *** Find Student by ID ***

def get_student_by_id(student_id:int):
    
    for student in students_db:
        if student_id == student['id'] :
            return student
    return None


# *** FIND TOP STUDENT ***            

def find_top_student() -> dict:
    if not students_db:
        return "No students in the database"

    top_student = None
    highest_avg = 0

    for student in students_db:
        if student['score']:
            avg = calculate_average(student['id'])
            if avg > highest_avg:
                highest_avg = avg
                top_student = student
    return top_student


# *** CALCULATE THE AVERAGE SCORE FOR EACH STUDENT ***

def calculate_average(student_id: int) -> float:
    """Calculate the average score for a specific student."""
    
    student = get_student_by_id(student_id)
    if not student:
        return 0.0
    
    student_score= []

    for score_list in student['score'].values():
        student_score.extend(score_list)

    if student_score:
        return sum(student_score) / len(student_score)
    
    return 0.0

# *** LIST STUDENTS ABOVE AVERAGE ***

def list_above_average():
    above_average = []
    for student in students_db:
        avg = calculate_average(student['id'])
        if avg > 50:
            above_average.append(student)
    print_student_table(above_average)

    
# *** UPDATE STUDENT ***

def update_student(student_id: int, **updates):
    """Update a student's details"""

    student = get_student_by_id(student_id)
    if not student:
        print("No student found.")
        return None
    
    updateable_field = ['name', 'age', 'address', 'email', 'phone', 'subjects', 'notes']

    for field, new_value in updates.items():
        if field not in updateable_field:
                    continue

        if field == "name":
            student[field] = name_validation()
                     
        elif field == "age":
            student[field] = age_validation()

        elif field in ["address", "email", "phone"]:
            if new_value.strip():
                    student[field] = new_value 

        elif field == "subjects":
            if  isinstance(new_value, str) and new_value.strip():
                student[field] = [s.strip().lower() for s in new_value.split(",") if s.strip()]
            else:
                student[field] = []    

        elif field == "notes":                 
            if new_value.strip():
                student[field] = new_value
            else:
                if student[field]:
                    confirm = input("This will clar existing notes. Are you sure? (y/n): ").strip().lower()
                    if confirm == "y":
                        student[field] = ""
                        print("Notes cleared.")
                else:
                    print("Notes not changed.") 
                   
    print(f"Student {student['name']} (ID: {student['id']}) updated successfully.")
    return student
    

# *** REMOVE STUDENT ***

def remove_student(student_id: int):
    """Remove a student by ID"""

    for i, student in enumerate(students_db): 
        if student ["id"]== student_id:
            removed = students_db.pop(i)
            print(f"Student {removed['name']} (ID: {removed['id']}) has been removed successfully.")
            return removed
    print(f"Student with ID {student_id} not found.")
    return None


# ***DISPLAY MENU ***

def display_menu():
    """This will display the list of options."""
    print("="*25, "Student Management System", "="*25)
    print(" 1. Add Student")
    print(" 2. Add Score")
    print(" 3. List All Students")
    print(" 4. Sort Students")
    print(" 5. Display Student Report")
    print(" 6. Find Student by Name")
    print(" 7. Find Student by Address")
    print(" 8. Find Student by Phone")
    print(" 9. Find Student by ID")
    print("10. Find Top Student")
    print("11. Calculate Average")
    print("12. List Students Above Average")
    print("13. Update Student")
    print("14. Remove Student")
    print("15. Exit")
    print("="*50)

if __name__ == "__main__":
    main()
