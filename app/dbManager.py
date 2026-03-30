import sqlite3 as sql3
from SQL_table_class import Table, Row

class DbManager:
    def __init__(self, path="db.db"):
        self.path = path
        self.con = sql3.connect(self.path, check_same_thread=False)
        self.cur = self.con.cursor()
        self.tables = (
            Table("users",
                  Row("id", "TEXT", pk=True),
                  Row("username", "TEXT"),
                  Row("password", "TEXT"),
                  Row("firstname", "TEXT"),
                  Row("secondName", "TEXT"),
                  )
        , )
        self.createTables(self.tables)

    def createTables(self, tables:tuple[Table, ...]):
        with self.con:
            for table in tables:
                self.con.execute(table.create())
            self.con.commit()
            
    def executemany(self, sql:str, data:tuple[tuple]) -> None:
        with self.con:
            self.con.executemany(sql, data)
            self.con.commit()

    def execute(self, sql:str, data:tuple):
        with self.con:
            self.con.execute(sql, data)
            self.con.commit()

    def selectData(self, sql:str, data=tuple()) -> list[tuple]:
        with self.con:
            self.cur.execute(sql, data)
            return self.cur.fetchall()

    # USERS MANAGEMENT
    def getUserById(self, userId:int) -> tuple[str, str]:
        query = """
            SELECT username, password
            FROM users
            WHERE id = ?
        """

        with self.con:
            data = self.execute(query, (userId, ))
            if len(data) > 0:
                return data[0]
            return data
    

    def checkIfUserExistsById(self, userId:int) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE id = ?
            )
        """

        with self.con:
            return bool(self.selectData(query, (userId,))[0][0])
    

    def checkIfUserExistsByUsername(self, username:str) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE username = ?
            )
        """

        with self.con:
            return bool(self.selectData(query, (username,))[0][0])
    

    def getNextFreeId(self) -> int:
        query = """
            SELECT MAX(id) FROM users;
        """

        with self.con:
            i = self.selectData(query)[0][0]
            if type(i) == int:
                return i + 1
            return 0

    def addUser(self, *args, userId=-1):
        if userId<=-1:
            userId = self.getNextFreeId()

        query = """
            INSERT INTO users (id, username, password, firstName, secondName)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.con:
            data = (userId,) + args
            print("__________DEBUGDATA__________", data)
            self.con.execute(query, data)
    
    def userLogin(self, username:str, password:str) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE username = ? AND password = ?
            )
        """

        with self.con:
            return bool(self.selectData(query, (username, password))[0][0]) 
    # USERS MANAGEMENT
    

if __name__ == "__main__":
    _ = DbManager()