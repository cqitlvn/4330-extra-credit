import unittest
from typing import List
from dataclasses import dataclass

@dataclass
class Student:
    student_id: str
    name: str
    age: int
    major: str

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Major: {self.major}"

class StudentRegistrationSystem:
    def __init__(self):
        self.students = {}

    def create_student(self, student_id: str, name: str, age: int, major: str) -> bool:
        if student_id in self.students:
            print("Student with this ID already exists.")
            return False
        else:
            self.students[student_id] = Student(student_id, name, age, major)
            print("Student created successfully.")
            return True

    def read_student(self, student_id: str) -> str:
        if student_id in self.students:
            print(str(self.students[student_id]) + "\n")
            return student_id
        else:
            print("Student not found.")

    def read_all_students(self) -> List[Student]:
        if not self.students:
            print("No students registered.")
            return []
        else:
            for student in self.students.values():
                print(str(student))
            return list(self.students.values())

    def update_student(self, student_id: str, name=None, age=None, major=None) -> bool:
        if student_id in self.students:
            student = self.students[student_id]
            if name:
                student.name = name
            if age:
                student.age = age
            if major:
                student.major = major
            print("Student updated successfully.")
            return True
        else:
            print("Student not found.")
            return False

    def delete_student(self, student_id: str) -> bool:
        if student_id in self.students:
            del self.students[student_id]
            print("Student deleted successfully.")
            return True
        else:
            print("Student not found.")
            return False

class TestStudentRegistrationSystem(unittest.TestCase):
    def setUp(self):
        """Set up a new StudentRegistrationSystem before each test."""
        self.system = StudentRegistrationSystem()
        # Add a test student that we can use in multiple tests
        self.test_student_id = "12345"
        self.test_name = "John Doe"
        self.test_age = 20
        self.test_major = "Computer Science"

    def test_create_student_success(self):
        """Test successful student creation"""
        result = self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        self.assertTrue(result)
        self.assertIn(self.test_student_id, self.system.students)
        student = self.system.students[self.test_student_id]
        self.assertEqual(student.name, self.test_name)
        self.assertEqual(student.age, self.test_age)
        self.assertEqual(student.major, self.test_major)

    def test_create_student_duplicate(self):
        """Test creating a student with duplicate ID"""
        # First creation should succeed
        self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        # Second creation with same ID should fail
        result = self.system.create_student(
            self.test_student_id,
            "Jane Doe",
            21,
            "Mathematics"
        )
        self.assertFalse(result)

    def test_create_student_edge_cases(self):
        """Test creating students with edge case values"""
        # Test with minimum age
        result1 = self.system.create_student("1", "Test Student", 16, "Major")
        self.assertTrue(result1)

        # Test with maximum age
        result2 = self.system.create_student("2", "Test Student", 99, "Major")
        self.assertTrue(result2)

        # Test with empty major
        result3 = self.system.create_student("3", "Test Student", 20, "")
        self.assertTrue(result3)

    def test_read_student_exists(self):
        """Test reading an existing student"""
        self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        result = self.system.read_student(self.test_student_id)
        self.assertEqual(result, self.test_student_id)

    def test_read_student_not_found(self):
        """Test reading a non-existent student"""
        result = self.system.read_student("nonexistent")
        self.assertIsNone(result)

    def test_read_student_after_deletion(self):
        """Test reading a student after they've been deleted"""
        self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        self.system.delete_student(self.test_student_id)
        result = self.system.read_student(self.test_student_id)
        self.assertIsNone(result)

    def test_read_all_students_empty(self):
        """Test reading all students when the system is empty"""
        students = self.system.read_all_students()
        self.assertEqual(len(students), 0)

    def test_read_all_students_multiple(self):
        """Test reading all students with multiple students in system"""
        # Create multiple students
        student_data = [
            ("1", "John Doe", 20, "CS"),
            ("2", "Jane Smith", 22, "Physics"),
            ("3", "Bob Johnson", 21, "Math")
        ]
        
        for sid, name, age, major in student_data:
            self.system.create_student(sid, name, age, major)
        
        students = self.system.read_all_students()
        self.assertEqual(len(students), len(student_data))
        
        # Verify each student's data
        for student in students:
            self.assertIsInstance(student, Student)

    def test_read_all_students_after_deletion(self):
        """Test reading all students after deleting some"""
        # Create multiple students
        self.system.create_student("1", "John", 20, "CS")
        self.system.create_student("2", "Jane", 22, "Physics")
        
        # Delete one student
        self.system.delete_student("1")
        
        students = self.system.read_all_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].name, "Jane")

    def test_update_student_exists(self):
        """Test updating an existing student"""
        self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        new_name = "John Smith"
        new_age = 21
        new_major = "Physics"
        
        result = self.system.update_student(
            self.test_student_id,
            name=new_name,
            age=new_age,
            major=new_major
        )
        
        self.assertTrue(result)
        student = self.system.students[self.test_student_id]
        self.assertEqual(student.name, new_name)
        self.assertEqual(student.age, new_age)
        self.assertEqual(student.major, new_major)

    def test_update_student_partial(self):
        """Test partial update of student information"""
        self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        new_name = "John Smith"
        
        result = self.system.update_student(
            self.test_student_id,
            name=new_name
        )
        
        self.assertTrue(result)
        student = self.system.students[self.test_student_id]
        self.assertEqual(student.name, new_name)
        self.assertEqual(student.age, self.test_age)  # Should remain unchanged
        self.assertEqual(student.major, self.test_major)  # Should remain unchanged

    def test_update_student_not_found(self):
        """Test updating a non-existent student"""
        result = self.system.update_student(
            "nonexistent",
            name="New Name"
        )
        self.assertFalse(result)

    def test_update_student_no_changes(self):
        """Test updating a student without providing any new values"""
        self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        
        result = self.system.update_student(self.test_student_id)
        
        self.assertTrue(result)
        student = self.system.students[self.test_student_id]
        self.assertEqual(student.name, self.test_name)
        self.assertEqual(student.age, self.test_age)
        self.assertEqual(student.major, self.test_major)

    def test_delete_student_exists(self):
        """Test deleting an existing student"""
        self.system.create_student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        result = self.system.delete_student(self.test_student_id)
        self.assertTrue(result)
        self.assertNotIn(self.test_student_id, self.system.students)

    def test_delete_student_not_found(self):
        """Test deleting a non-existent student"""
        result = self.system.delete_student("nonexistent")
        self.assertFalse(result)

    def test_delete_multiple_students(self):
        """Test deleting multiple students"""
        # Create multiple students
        student_ids = ["1", "2", "3"]
        for sid in student_ids:
            self.system.create_student(sid, f"Student {sid}", 20, "Major")
        
        # Delete each student and verify
        for sid in student_ids:
            result = self.system.delete_student(sid)
            self.assertTrue(result)
            self.assertNotIn(sid, self.system.students)
        
        # Verify system is empty
        self.assertEqual(len(self.system.students), 0)

    def test_student_str_representation(self):
        """Test the string representation of a Student object"""
        student = Student(
            self.test_student_id,
            self.test_name,
            self.test_age,
            self.test_major
        )
        expected_str = f"ID: {self.test_student_id}, Name: {self.test_name}, Age: {self.test_age}, Major: {self.test_major}"
        self.assertEqual(str(student), expected_str)

    def test_system_initialization(self):
        """Test that the system is properly initialized"""
        system = StudentRegistrationSystem()
        self.assertEqual(len(system.students), 0)
        self.assertIsInstance(system.students, dict)

if __name__ == '__main__':
    # Run the unit tests with verbosity level 2
    unittest.main(verbosity=2)
    
    # Note: The code below will only execute if we modify the unittest.main() 
    # call because unittest.main() exits the program. In a real application,
    # you would typically put this in a separate file.
    
    def print_menu():
        print("\n=== Student Registration System ===")
        print("1. Add new student")
        print("2. View student details")
        print("3. View all students")
        print("4. Update student")
        print("5. Delete student")
        print("6. Run tests")
        print("0. Exit")
        print("================================")

    def get_student_info():
        student_id = input("Enter student ID: ")
        name = input("Enter student name: ")
        while True:
            try:
                age = int(input("Enter student age: "))
                if 16 <= age <= 99:  # Basic age validation
                    break
                print("Age must be between 16 and 99")
            except ValueError:
                print("Please enter a valid number for age")
        major = input("Enter student major: ")
        return student_id, name, age, major

    def main():
        system = StudentRegistrationSystem()
        
        while True:
            print_menu()
            choice = input("Enter your choice (0-6): ")
            
            if choice == '1':
                # Add new student
                student_id, name, age, major = get_student_info()
                system.create_student(student_id, name, age, major)
                
            elif choice == '2':
                # View student details
                student_id = input("Enter student ID to view: ")
                system.read_student(student_id)
                
            elif choice == '3':
                # View all students
                system.read_all_students()
                
            elif choice == '4':
                # Update student
                student_id = input("Enter student ID to update: ")
                print("\nLeave blank if no change is needed:")
                name = input("Enter new name (or press Enter to skip): ")
                age_str = input("Enter new age (or press Enter to skip): ")
                major = input("Enter new major (or press Enter to skip): ")
                
                # Process the updates
                age = int(age_str) if age_str.strip() else None
                name = name if name.strip() else None
                major = major if major.strip() else None
                
                system.update_student(student_id, name, age, major)
                
            elif choice == '5':
                # Delete student
                student_id = input("Enter student ID to delete: ")
                system.delete_student(student_id)
                
            elif choice == '6':
                # Run tests
                print("\nRunning unit tests...")
                unittest.main(verbosity=2, exit=False)
                
            elif choice == '0':
                print("Thank you for using the Student Registration System!")
                break
                
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
