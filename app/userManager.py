# from project import dbManager as _dbManager

import dbManager as _dbManager
import PasswordManager as pMan


class UserManager:
    def __init__(self, dbManager:_dbManager.DbManager):
        self.dbManager = dbManager
    
    def checkIfUserExists(self, userId=-1, username='') -> bool:
        if userId:
            return self.dbManager.checkIfUserExistsById(userId)
        elif username:
            return self.dbManager.checkIfUserExistsByUsername(username)
        
        return False
    
    def addUser(self, username, password, *args):
        password = pMan.hash(password)
        return self.dbManager.addUser(username, password, *args)
    
    def login(self, username:str, password:str):
        password = pMan.hash(password)
        return self.dbManager.userLogin(username, password)
