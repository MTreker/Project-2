from PyQt6.QtWidgets import *
from gui import *
import csv


class InvalidScoreError(Exception):
    pass


class Logic(QMainWindow, Ui_Grade_Calc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.grade_button.clicked.connect(lambda: self.grade())
        self.clear_button.clicked.connect(lambda: self.clear())
        st_1 = self.student_one_radio
        st_1.toggled.connect(lambda: self.total())
        st_2 = self.student_two_radio
        st_2.toggled.connect(lambda: self.total())
        st_3 = self.student_three_radio
        st_3.toggled.connect(lambda: self.total())
        st_4 = self.student_four_radio
        st_4.toggled.connect(lambda: self.total())
        st_5 = self.student_five_radio
        st_5.toggled.connect(lambda: self.total())
        self.total_score_2.hide()
        self.total_score_3.hide()
        self.total_score_4.hide()
        self.total_score_5.hide()

    def total(self):
        """This checks what radio button is checked and displays the appropriate number of input boxes

        """
        if self.student_two_radio.isChecked():
            self.total_score_2.show()
            self.total_score_3.hide()
            self.total_score_4.hide()
            self.total_score_5.hide()
        elif self.student_three_radio.isChecked():
            self.total_score_2.show()
            self.total_score_3.show()
            self.total_score_4.hide()
            self.total_score_5.hide()
        elif self.student_four_radio.isChecked():
            self.total_score_2.show()
            self.total_score_3.show()
            self.total_score_4.show()
            self.total_score_5.hide()
        elif self.student_five_radio.isChecked():
            self.total_score_2.show()
            self.total_score_3.show()
            self.total_score_4.show()
            self.total_score_5.show()
        else:
            self.total_score_2.hide()
            self.total_score_3.hide()
            self.total_score_4.hide()
            self.total_score_5.hide()

    def grade(self):
        """Compute and displays the letter grade for each student in the list

        Args:
            total_stu (int): A number that represents the number of students between 1 and 5
            totalStudents (int): a number that comes from total_stu
            studentScoreAsStrings (list): List of all the grades for the total number of students
            studentScoreAsInts (list[int]): List of all the grades as an integer
            highScore (int(max)): Highest score for the list of students
            grade (string): The letter grade for each student

        """
        with open('grades.txt', 'a', newline='') as grade_file:
            self.menu.clear()
            total_stu = 1  # checks to see what radio button is checked
            if self.student_two_radio.isChecked():
                total_stu = 2
            elif self.student_three_radio.isChecked():
                total_stu = 3
            elif self.student_four_radio.isChecked():
                total_stu = 4
            elif self.student_five_radio.isChecked():
                total_stu = 5
            else:
                total_stu = 1
            totalStudents = int(total_stu)

            studentScoreAsStrings = []
            while len(studentScoreAsStrings) < totalStudents:  # This takes what is in the text boxs and
                # puts them in a list as a string. This depends on what radio box is checked
                if totalStudents == 2:
                    studentScoreAsStrings = self.total_score.text().split() + self.total_score_2.text().split()
                elif totalStudents == 3:
                    studentScoreAsStrings = (self.total_score.text().split() + self.total_score_2.text().split() +
                                             self.total_score_3.text().split())
                elif totalStudents == 4:
                    (self.total_score.text().split() + self.total_score_2.text().split() +
                     self.total_score_3.text().split() + self.total_score_4.text().split())
                elif totalStudents == 5:
                    (self.total_score.text().split() + self.total_score_2.text().split() +
                     self.total_score_3.text().split() + self.total_score_4.text().split() +
                     self.total_score_5.text().split())
                else:
                    studentScoreAsStrings = self.total_score.text().split()

            studentScoreAsInts = []
            try:
                for x in range(totalStudents):  # Takes what is in the list(that is a string) and firstly, checks to
                    # see if it is between 0 and 100. If it is between the numbers,
                    # it changes the string list to an integer list.
                    try:
                        score = int(studentScoreAsStrings[x])
                        if 0 <= score <= 100:
                            studentScoreAsInts.append(score)
                        else:
                            self.menu.appendPlainText(
                                f'Invalid score for Student {x + 1}. \nScore must be between 0 and 100.')
                            raise InvalidScoreError()  # Raise the custom exception to break out of both loops
                    except ValueError:
                        self.menu.appendPlainText(f'Invalid input for Student {x + 1}. '
                                                  f'\nPlease enter a valid integer score.')
                        raise InvalidScoreError()  # Raise the custom exception to break out of both loops

            except InvalidScoreError:
                self.menu.appendPlainText('')
            else:
                highScore = max(studentScoreAsInts)
                grade = ''
                for x in range(totalStudents):  # Takes the highest score and subtracts a
                    # certain amount to get the other grades
                    if studentScoreAsInts[x] >= highScore - 10:
                        grade = 'A'
                    elif studentScoreAsInts[x] >= highScore - 20:
                        grade = 'B'
                    elif studentScoreAsInts[x] >= highScore - 30:
                        grade = 'C'
                    elif studentScoreAsInts[x] >= highScore - 40:
                        grade = 'D'
                    else:
                        grade = 'F'
                    self.menu.appendPlainText(f'Student {x + 1} score is {studentScoreAsInts[x]} and grade is {grade}')
                    info = f'Student {x + 1} score is {studentScoreAsInts[x]} and grade is {grade}'  # prints the text
                    # to show each students score and grade
                    grade_file.write(info)
        grade_file.close()

    def clear(self):
        """
        Clears the number of students and all the grades
        Hides text boxes 2-5
        Unchecks radio buttons 2-5 and rechecks radio button 1
        Resets text for menu
        """
        self.student_one_radio.setChecked(True)  # resets everything back to the beginning
        self.student_two_radio.setChecked(False)
        self.student_three_radio.setChecked(False)
        self.student_four_radio.setChecked(False)
        self.student_five_radio.setChecked(False)
        self.total_score_2.hide()
        self.total_score_3.hide()
        self.total_score_4.hide()
        self.total_score_5.hide()
        self.total_score.clear()
        self.total_score_2.clear()
        self.total_score_3.clear()
        self.total_score_4.clear()
        self.total_score_5.clear()
        self.menu.setPlainText("Please enter total number of students and their grade\n"
                               "\n"
                               "Enter grades as follows:\n"
                               "10 20 30 40 etc...")