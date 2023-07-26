#Quiz Maker
"""
Quiz Maker - Make an application which takes various questions from a database, picked randomly,
and puts together a quiz for students. Each quiz can be different and then reads a key to grade the quizzes.
"""

"""
Strategy/approach to the project:
Step 1. create quiz questions database with answer keys. Do we want questions to be multiple choices?
Step 2. Write a program that randomly selects a set of questions from the database. Use random package.
Step 3. Display the questions to the user and ask for their answers.
Step 4. Grade the user's answers and display their score.
Step 5. Save the user's score to a file.

To incorporate ethics and critical thinking in the project, I would make sure that the questions are fair and unbiased.
I would also make sure that the program is well-designed and easy to use. Additionally, I would provide the user with 
feedback on their answers, so that they can learn from their mistakes and improve their critical thinking skills.

Here are some additional ethical considerations for this project:

The questions should be appropriate for the target audience.
The answers should be accurate and up-to-date.
The program should not discriminate against any group of people.
The user's privacy should be protected.

I believe that this project can be a valuable tool for learning and assessment. By incorporating ethics and critical 
thinking into the project, I can help to ensure that it is used in a responsible and ethical way.
"""

import random as r
import db_base as db
import csv


class Questions: #this is for questions
    def __init__(self,questionID, Questions):
        self.questionID = questionID
        self.Questions = Questions
class Csvlab(db.DBase):
    def reset_or_create_db(self):
        try:
            sql = """ DROP TABLE IF EXISTS Questions;
                CREATE TABLE Questions(Question_Number INT NOT NULL PRIMARY KEY UNIQUE,
                    Questions TEXT)"""
            super().execute_script(sql)
        except Exception as e:
            print("An error has occurred: ", e)
        print(Questions)

class Quiz:
    """Shows List of Questions."""
    def __init__(self,questions):
        self.questions = questions

    def generate_quiz(self):
        """Generates a quiz by randomly selecting questions from the pool of questions."""
        quiz = []
        for q in range(10):
            question = r.choice(self.questions)
            quiz.append(question)
            return quiz

    def grade_quiz(self,quiz,key):
        """Grades a quiz by comparing the student's answers to the key."""
        score = 0
        for question, answer in zip(quiz, key):
            if question.answer == answer:
                score += 1






