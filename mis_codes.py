
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

        questions = read_questions_from_database()
        answers = read_answers_from_database()

        score = 0
        for question, answer in zip(questions, answers):
            answer_given = ask_question(question, answers)
            if answer_given == answer:
                score += 1

        print(f"Your score is {score} out of {len(questions)}")

    if __name__ == "__main__":
        questions = []
        with open("Questions.csv", "r")
