#!/usr/bin/python
import MySQLdb as mdb

class DBUtils:
    @staticmethod
    def connect_to_db():
        db = mdb.connect(host="localhost",
                         user="root",
                         passwd="khron0s725",
                         db="mario")
        cur = db.cursor()
        return db, cur

    @staticmethod
    def record_new_score(new_score, player_name):
        db, cur = DBUtils.connect_to_db()
        qry = "INSERT INTO Scores (score, name) VALUES (" + str(new_score) + ", \'" + player_name + "\')"
        cur.execute(qry)
        db.commit()
        db.close()

    @staticmethod
    def get_top_3_scores():
        db, cur = DBUtils.connect_to_db()

        qry = """SELECT *
                FROM Scores s1
                ORDER BY s1.score DESC"""

        cur.execute(qry)

        top3 = []
        for i in range(3):
            row = cur.fetchone()
            print str(row[0]), row[1], "\n"
            top3.append((row[0], row[1]))

        db.close()
        return top3

    @staticmethod
    def get_high_score():
        db, cur = DBUtils.connect_to_db()

        qry = """SELECT s1.score
                FROM Scores s1
                WHERE s1.score >= ALL (SELECT s2.score FROM Scores s2)"""

        cur.execute(qry)
        row = cur.fetchone()
        db.close()

        print row[0]
        return row[0]

    @staticmethod
    def clear_db():
        db, cur = DBUtils.connect_to_db()

        qry = "DELETE FROM Scores"
        cur.execute(qry)
        db.commit()
        db.close()

'''
DBUtils.clear_db()
DBUtils.record_new_score(0, "zero")
DBUtils.record_new_score(0, "zero")
DBUtils.record_new_score(0, "zero")
DBUtils.get_high_score()
DBUtils.get_top_3_scores()
'''
