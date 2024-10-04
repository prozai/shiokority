from app.models.developers import Developers

class DevelopersController():
    def __init__(self):
        self.developers = Developers()

    def registerDevelopers(self, developer, secret_key):
        return self.developers.registerDeveloper(developer, secret_key)

    def loginDeveloper(self, developer):
        return self.developers.loginDeveloper(developer)
    
    def getDeveloperByEmail(self, email):
        return self.developers.getDeveloperByEmail(email)
    
    def update2FAbyEmail(self, email):
        return self.developers.update2FAbyEmail(email)