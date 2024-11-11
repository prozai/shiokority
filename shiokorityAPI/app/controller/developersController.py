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

    def generate_api_key(self, dev_id):
        return Developers().generateApiKey(dev_id)
    
    def getDeveloperByEmail(self, dev_email):
        return Developers().getDeveloperByEmail(dev_email)
    
    def getApiKeys(self, dev_id):
        return Developers().get_api_keys(dev_id)
    
    def deleteApiKey(self, api_key):
        return Developers().delete_api_key(api_key)
    
    def saveApiKey(self, dev_id, iv, ciphertext, signature, public_key):
        return Developers().save_api_key(dev_id, iv, ciphertext, signature, public_key)
    
    def validateTokenEmail(self, email):
        return Developers().validateTokenEmail(email)
    