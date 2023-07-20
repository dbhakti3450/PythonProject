#Quiz Maker
"""
Quiz Maker - Make an application which takes various questions from a database, picked randomly,
and puts together a quiz for students. Each quiz can be different and then reads a key to grade the quizzes.
"""

"""
Strategy/approach to the project:
Step 1. create quiz questions database with answer keys. Do we want questions to be multiple choices?
Step 2. Write a program that randomly selects a set of questions from the database. Use random package.
3. Display the questions to the user and ask for their answers.
4. Grade the user's answers and display their score.
5. Save the user's score to a file.

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

class Question: #this is for questions

    def __init__(self,questions, answers, correct_answers):
        self.question = questions
        self.answers = answers
        self.correct_answers = correct_answers

    def ask_question(self, question, answers):
        """Asks the user a question and returns their answer."""
        self.question = question
        self.answers = answers
        print(question)

        for index, answer in enumerate(answers):
            print(f"{index + 1}: {answer}")

        answer = input("Your answer: ")
        return answer

    def main():
        """The main function of the program."""

        questions = read_questions_from_database()
        answers = read_answers_from_database()

        score = 0
        for question, answer in zip(questions, answers):
            answer_given = ask_question(question, answers)
            if answer_given == answer:
                score += 1

        print(f"Your score is {score} out of {len(questions)}")

    if __name__ == "__main__":
        main()



