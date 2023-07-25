#!/usr/bin/env python

import sqlite3
import csv
import random
import string
import os
import textwrap

from databaseHandler import DatabaseHandler


class Question(object):
    """Manages a question and its related answers"""

    def __init__(self, dbh, id):
        self._id = id
        self.questiontext = dbh.get_question(id)
        self.answers = dbh.get_answers(id)

    def get_question(self):
        """get the question text"""
        return self.questiontext

    def get_answers(self):
        """get a shuffled list of answers"""
        random.shuffle(self.answers)
        return self.answers

    def get_correct_answer_count(self):
        """get the number of correct answers for the given question"""
        return len([x for x in self.answers if x['correct'] == 1])

    def sanitize_user_answer_to_list(self, user_answer):
        """turn the user's response into a list of alphabetical characters"""
        return [c for c in str.upper(user_answer) if c in string.ascii_uppercase]

    def check_answer(self, user_answer):
        """check correctness of user's response and whether a valid response was supplied.
        raises ValueError for invalid input, otherwise returns True/False"""

        user_answer = self.sanitize_user_answer_to_list(user_answer)
        ans_count = self.get_correct_answer_count()

        # check response validity
        if len(user_answer) == 0:
            raise ValueError("No answer selected")
        elif len(user_answer) != ans_count:
            raise ValueError("This question has " + str(ans_count) + " answer" + ("s" if ans_count > 1 else ""))

        # loop through sanitized user response
        for ans in user_answer:

            # assign a numerical index so we can check against the list of answers
            answer_index = ord(ans) - ord('A')

            # check if the answer is within bounds of the answer list; raise an error if not
            if answer_index >= len(self.answers) or answer_index < 0:
                raise ValueError("Invalid selection: " + ans)

            # check if any user selections are wrong
            if self.answers[answer_index]['correct'] == 0:
                return False

        # if we make it out of the loop without triggering any returns or errors, the answer must be true
        return True


class Player(object):
    """Manages the current user and their score"""

    def __init__(self, dbh, name):
        self.id = dbh.create_player(name)
        self.name = name
        self._dbh = dbh
        self.score = 0

    def score_up(self, points=1):
        """increment the player's score"""
        newscore = self.score + points
        self._dbh.set_score(self.id, newscore)
        self.score = newscore

    def score_down(self, points=1):
        """decrement the player's score"""
        return self.score_up(self, -points)

    def get_score(self):
        """returns the player's current score"""
        return self.score

    def get_name(self):
        """return the player's name"""
        return self.name

    def get_id(self):
        """return the player's unique ID as set by the database"""
        return self.id


if __name__ == '__main__':
    dbh = DatabaseHandler("quizApp.sqlite")

    if not dbh.check_db_ready():
        print("No database found. Initializing new database...")
        dbh.reset_db()
        print("Done!\n")

    name = ""
    while name.strip() == "":
        name = input("Please enter your name: ")

    player = Player(dbh, name)

    question_count = dbh.get_question_count()
    qids = random.sample(range(0, question_count), 3)

    # loop through all the questions until we run out
    for qid in qids:
        os.system("cls" if os.name == "nt" else "clear")
        print(player.name + "                   Score: " + str(player.score))

        # create a question object and store some of the question's data
        question = Question(dbh, qid)
        answers = question.get_answers()
        answer_count = question.get_correct_answer_count()
        wrapper = textwrap.TextWrapper(initial_indent="    ", subsequent_indent="       ")

        # output the question and possible answers to the user
        print("\n" + question.get_question() + "\n")
        print("Select " + str(answer_count) + " answer" + ("s" if answer_count > 1 else "") + " from below:\n")
        for i in range(len(answers)):
            anstext = chr(65 + i) + ". " + answers[i]['answertext']
            for line in wrapper.wrap(anstext):
                print(line)

        # use a loop to repeatedly ask for answers if the user's input is invalid
        while True:
            try:
                # prompt the user for an answer
                user_answer = input(
                    "\nYour response (" + str(answer_count) + " answer" + ("s" if answer_count > 1 else "") + "): ")

                # let the user know if they got it right
                if question.check_answer(user_answer):
                    print("Correct! You get " + str(answer_count) + " point" + ("s" if answer_count > 1 else ""))
                    player.score_up(answer_count)
                else:
                    print("Sorry, that's incorrect. No points for you!")

                # exit the answer-asking loop
                break

            # something was wrong with the user's input. report the error and loop again
            except ValueError as e:
                print(e)

        # give the user a chance to see whether they got it right or not before proceeding
        input("\nPress Enter to continue...")

    # clear the screen
    os.system("cls" if os.name == "nt" else "clear")

    # report the player's final score
    print("\nThanks for playing!")
    print("\nFinal score: " + str(player.score))

    # report high scores
    print("\nHigh scores:")
    rank = 0
    print("  {0} {1} {2}".format("Rank", "Pts", "Name"))
    for hs_entry in dbh.get_highscores():
        rank += 1
        # include an indicator for the current player if they make the cut
        indic = "<------" if hs_entry['id'] == player.get_id() else ""
        print("  {0:3d}. {1:3d} {2} {3}".format(rank, hs_entry['score'], hs_entry['name'], indic))

    dbh.close_db()
