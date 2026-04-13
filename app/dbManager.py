import sqlite3 as sql3
from SQL_table_class import Table, Row
import CookieManager as CookieMan

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
        , Table("cookies",
                Row("id", "TEXT", pk=True),
                Row("userId", "TEXT"),
                Row("loggedIn", "BOOLEAN"),
                Row("userId", "TEXT", fk=True, connectedTable="users", connectedValue="id"),

                ))
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
            try:
                return int(i) + 1
            except:
                return 0

    def addUser(self, *args, userId=-1) -> tuple:
        print(args)

        if userId<=-1:
            userId = self.getNextFreeId()

        query = """
            INSERT INTO users (id, username, password, firstName, secondName)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.con:
            data = (userId,) + args
            self.con.execute(query, data)
            return data
    
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

    # COOKIES
    # def getNextFreeCookieId(self) -> int:
    #     query = """
    #             SELECT MAX(CAST(id AS INTEGER)) \
    #             FROM cookies; \
    #             """
    #     i = self.selectData(query)[0][0]
    #     try:
    #         return int(i) + 1
    #     except:
    #         return 0

    def saveCookie(self, userId: str, cookie: str | None=None) -> None:
        """Insert a new session cookie for the user."""
        if not cookie:
            cookie = CookieMan.generateCookie()

        query = """
                INSERT INTO cookies (id, userId, loggedIn)
                VALUES (?, ?, 1) \
                """

        with self.con:
            self.con.execute(query, (cookie, userId))
            self.con.commit()

    def isUserLoggedIn(self, cookie: str) -> bool:
        """Return True if the token exists in DB and loggedIn = 1."""
        query = """
                SELECT EXISTS(SELECT 1 \
                              FROM cookies \
                              WHERE id = ? \
                                AND loggedIn = 1) \
                """
        return bool(self.selectData(query, (cookie,))[0][0])

    def setCookieLoggedIn(self, cookie: str, value: bool) -> None:
        """Set loggedIn to True (1) or False (0) for a given token."""
        query = """
                UPDATE cookies
                SET loggedIn = ?
                WHERE id = ? \
                """
        with self.con:
            self.con.execute(query, (int(value), cookie))
            self.con.commit()

    def setCookieUserId(self, cookie: str, value: str) -> None:
        """Set loggedIn to True (1) or False (0) for a given token."""
        query = """
                UPDATE cookies
                SET userId = ?
                WHERE id = ? \
                """
        with self.con:
            self.con.execute(query, (value, cookie))
            self.con.commit()

    def getCookieByUserId(self, userId: str) -> str | None:
        query = """
                SELECT id
                FROM cookies
                WHERE userId = ? \
                """
        result = self.selectData(query, (userId,))
        return result[0][0] if result else None
    

if __name__ == "__main__":
    _ = DbManager()