# ------------------------------------------------------------------------------------------ #
# Title: Assignment06.py
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
# Michael Kemery, 2024.08.03, evaluated original program
# Michael Kemery, 2024.08.04, created classes and functions
# ------------------------------------------------------------------------------------------ #

import json
import io as _io

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
# FILE_NAME: str = "Enrollments.csv"
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
## user input and storage of data
menu_choice: str  # Hold the choice made by the user. - moved to be with user inputs
student_first_name: str = ''  # Holds the first name of a student entered by the user.
student_last_name: str = ''  # Holds the last name of a student entered by the user.
course_name: str = ''  # Holds the name of a course entered by the user.

student_data: dict = {}  # one row of student data
students: list = []  # a table of student data

# file related
#csv_data: str = ''  # Holds combined string data separated by a comma. -- commented out bc not using
json_data: str = ''  # Holds combined string data in a json format.
file = None  # Holds a reference to an opened file.


class FileProcessor:
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            # print("Data read from file:", stu_data)  # debugging line
            # print(type(stu_data)) ## debugging line
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("File does not exist!\n")
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!\n")
        finally:
            if file.closed == False:
                file.close()
        return student_data

class IO:
    """
        A collection of presentation layer functions that manage user input and output
        MDKemery:2024.08.04,Created Class, added functions: menu output, input functions
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ Function displays a custom error messages to the user
        ChangeLog: (Who, When, What)
        MDKemery:2024.08.04,created function
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep="\n")

    @staticmethod
    def output_menu(menu: str):
        """ Function displays the menu of choices to the user
            ChangeLog: (Who, When, What)
            MDKemery: 2024.08.24,Created function
        :return: None
        """
        print(MENU)

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user
        ChangeLog: (Who, When, What)
        MDKemery: 2024.08.04, Created function
        : return string of user choice
        """
        choice = ("0")
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # note num are captured strings
                raise Exception("Please, choose only 1,2,3,4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def input_student_data(student_data: list):
        '''
            This function gets the first name, last name, and course name of student
            includes some error handling

            ChangeLog: (Who, When, What)
            MDKemery: 2024.08.04,Created function

            :return: str
        '''

        try:
            student_first_name = input("Enter the student's first name: ").title()
            if not student_first_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            student_last_name = input("Enter the student's last name: ").title()
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the name of the course: ").title()
            ## let's add a "duplication detection" step to this branch.
            #  basically loop through students and look for exact match for all three
            #    variables.  if exact match for all 3 then found = true
            found = False
            for student in students:
                if (student["FirstName"] == student_first_name and
                        student["LastName"] == student_last_name and
                        student["CourseName"] == course_name):
                    found = True
                    break
            ## give user information that student is already enrolled.
            if found:
                print()
                print(f"{student_first_name} {student_last_name} is already enrolled in {course_name}.\n")
            else:
                stu_data = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
                students.append(stu_data)
                print(f"\nYou have registered {student_first_name} {student_last_name} for {course_name}. \n")

        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("Non-specific error!", e)
        return students

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        '''
        Function to write data to JSON file; indent = 4 for clarity to review JSON
        Changelog (WWW)
        MDKemery, 2024.08.04, created function
        '''
        try:
            file = open(file_name, "w")
            json.dump(student_data, file, indent=4)  #indent is just a formatting parameter
            file.close()
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format\n", e)
        except Exception as e:
            IO.output_error_messages("There is not a specific error!", e)
            print("Built-In Python error info: ")
            print(e, e.__doc__, type(e), sep='\n')
        finally:
            if file.closed == False:
                file.close()

    @staticmethod
    def output_student_courses(student_data: list):
        '''
        function outputs student information, with an option to sort the output (NOT FILE) by course name
        ChangeLog: (Who, When, What)
        MDKemery: 2024.08.04,Created function
        MDKemery: 2024.08.05, added option to look at data sorted.

        '''

        choice = input("Would you like to view the registered students sorted by course name? (Y/N)")
        print()
        # define header for output
        my_message = ("-" * 5 + "STUDENTS CURRENTLY REGISTERED" + "-" * 5)
        if choice in ("Y", "y", "N", "n"):

            if choice in ("Y", "y"):
                # sort the data!
                sort_data = IO.sort_output(student_data)

                ## let's try and groups students together by course
                course_dict = {}  ## creating a new dictionary - locally scoped
                for student in sort_data:
                    course_name = student["CourseName"]
                    if course_name not in course_dict:
                        course_dict[course_name] = []  ## basically - create new <blank> entry in dictionary
                    course_dict[course_name].append(f"{student['FirstName']} {student['LastName']}")

                print(my_message)

                ## nested loop - first loop - print course name.
                ##               second loop - print student
                for course_name, students in course_dict.items():
                    print(course_name)
                    for student in students:
                        print(student)
                    print("-" * len(my_message))
            else:
                # keep original order / don't sort
                sort_data = student_data
                my_message = ("-" * 5 + "STUDENTS CURRENTLY REGISTERED" + "-" * 5)
                print(my_message)
                for student in sort_data:
                    print(student["FirstName"], student["LastName"], student["CourseName"])
                print("-" * len(my_message))
        else:
            print("Invalid choice.  Please enter 'Y' or 'N'.")

    @staticmethod
    def sort_output(data):
        '''
             This function sorts output (NOT F3ILE) by COURSE_NAME making it easier to see how many students are
             registered to the same course.

             ChangeLog: (Who, When, What)
             MDKemery: 2024.08.04,Created function

             return: str
        '''
        sort_data = sorted(data, key=lambda x: (x['CourseName'], x['FirstName']))
        #print(sort_data["FirstName"], sort_data["LastName"], sort_data["CourseName"])
        return sort_data

# END OF CLASS & FUNCTION DEFINITIONS
# END OF CLASS & FUNCTION DEFINITIONS

## START PROGRAM

# Extract the data from the (JSON) file and read into students object
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        IO.output_student_courses(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        print()  # for easier reading between prompt and output
        IO.output_student_courses(student_data=students)
        print()
        continue

    # Save the data to a file
    elif menu_choice == "3":
        IO.write_data_to_file(FILE_NAME, students)
        print("Data saved to file!")
        continue
        
    # Stop the loop
    elif menu_choice == "4":
        break

print("Program Ended")