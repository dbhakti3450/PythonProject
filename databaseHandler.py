import Database_base as db
import csv


class DatabaseHandler(db.DBase):
    """Database interface. All DB calls are made in this class."""

    def get_question(self, questionid):
        """Return question text"""
        super().get_cursor.execute("SELECT questiontext FROM questions WHERE id=?", (questionid,))
        return super().get_cursor.fetchone()[0]

    def get_question_count(self):
        """Return total number of questions in DB"""
        super().get_cursor.execute("SELECT count(*) FROM questions");
        return super().get_cursor.fetchone()[0]

    def get_answers(self, questionid):
        """Return all possible answers for a given question"""
        super().get_cursor.execute("SELECT answertext,correct FROM answers WHERE questionid=?", (questionid,))
        return [{'answertext': answertext, 'correct': correct} for answertext, correct in
                super().get_cursor.fetchall()]

    def get_score(self, playerid):
        """Return score for a given player id"""
        super().get_cursor.execute("SELECT score FROM players WHERE id=?", (playerid,))
        return super().get_cursor.fetchone()[0]

    def set_score(self, playerid, score):
        """Set a player's score"""
        super().get_cursor.execute("UPDATE players SET score = ? WHERE id = ?", (score, playerid))
        super().get_connection.commit()

    def get_highscores(self, count=5):
        """Get top scores. Most recent entries are preferred in the event of a tie."""
        super().get_cursor.execute("SELECT id,name,score FROM players ORDER BY score DESC, id DESC LIMIT ?", (count,))
        return [{'id': id, 'name': name, 'score': score} for id, name, score in super().get_cursor.fetchall()]

    def get_highscores_by_name(self, name):
        """Get top scores. Most recent entries are preferred in the event of a tie."""
        super().get_cursor.execute("SELECT id,name,score FROM players WHERE name = ? ORDER BY score DESC", (name,))
        return [{'id': id, 'name': name, 'score': score} for id, name, score in super().get_cursor.fetchall()]

    def delete_high_score_entry(self, id):
        """Delete an entry by its ID."""
        super().get_cursor.execute("DELETE FROM players WHERE id=?", (id,))
        super().get_connection.commit()

    def create_player(self, name):
        """Add a player to the DB and return their unique ID"""
        super().get_cursor.execute("INSERT INTO players (name,score) VALUES (?,?)", (name, 0))
        super().get_connection.commit()
        return super().get_cursor.lastrowid

    def check_db_ready(self):
        """check if the DB has been set up"""
        try:
            # note: this could also be done by querying the DB for tables by name, but this code is simpler
            super().get_cursor.execute("SELECT * FROM questions LIMIT 1")
            super().get_cursor.execute("SELECT * FROM answers LIMIT 1")
            super().get_cursor.execute("SELECT * FROM players LIMIT 1")
            return True
        except:
            return False

    def reset_db(self):
        """seed the database using accompanying CSV files"""
        c = super().get_cursor

        # drop tables
        for t in ["questions", "answers", "players"]:
            c.execute("DROP TABLE IF EXISTS " + t)

        # set up tables
        c.execute("CREATE TABLE questions (id INTEGER PRIMARY KEY, questiontext TEXT)")
        c.execute("CREATE TABLE answers (id INTEGER PRIMARY KEY, questionid INTEGER, answertext TEXT, correct INTEGER, FOREIGN KEY(questionid) REFERENCES questions(id))")
        c.execute("CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)")

        # import and insert seed data
        # questions
        with open("questions.csv") as csvfile:
            dr = csv.DictReader(csvfile)
            insert_values = [(d['Question_Number'], d['Questions']) for d in dr]

        c.executemany("INSERT INTO questions (id,questiontext) VALUES (?,?)", insert_values)

        # answers
        with open("answer_key.csv") as csvfile:
            dr = csv.DictReader(csvfile)
            insert_values = [(d['ID'], d['QuestionID'], d['AnswerText'], d['Correct']) for d in dr]

        c.executemany("INSERT INTO answers (id,questionid,answertext,correct) VALUES (?,?,?,?)", insert_values)

        # players
        players = [(i, "Person " + chr(i + 65), i + 1) for i in range(5)]
        c.executemany("INSERT INTO players (id,name,score) VALUES (?,?,?)", players)

        super().get_connection.commit()
