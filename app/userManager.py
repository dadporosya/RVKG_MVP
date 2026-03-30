# from project import dbManager as _dbManager

import dbManager as _dbManager


class UserManager:
    def __init__(self, dbManager:_dbManager.DbManager):
        self.dbManager = dbManager
    
    def checkIfUserExists(self, userId=-1, username='') -> bool:
        if userId:
            return self.dbManager.checkIfUserExistsById(userId)
        elif username:
            return self.dbManager.checkIfUserExistsByUsername(username)
        
        return False
    
    def addUser(self, *args):
        self.dbManager.addUser(*args)
    
    def login(self, username:str, password:str):
        return self.dbManager.userLogin(username, password)
