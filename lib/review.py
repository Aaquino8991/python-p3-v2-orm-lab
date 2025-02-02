from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """ 
            INSERT INTO reviews (year, summary, employee_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review
   
    @classmethod
    def instance_from_db(cls, row):
        review = cls.all.get(row[0])

        if review:
            review.year = row[1]
            review.summary = row[2]
            review.employee_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            review = cls(row[1], row[2], row[3])
            review.id = row[0]
            cls.all[review.id] = review
        return review
   

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM pets
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id, )).fetchone()

        return cls.instance_from_db(row) if row else None

    def update(self):
        sql = """
            UPDATE pets
            SET year =?, employee_id = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.year, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM pets
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id, ))
        CONN.commit()

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM pets
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    


