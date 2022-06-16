import unittest
from Data.actionsDatabase import insertUser, authLogin, insertUserNetwork, authNetworksLogin, savesScheduleDatabase, saveScheduleFiles, getIdQueue, nextSchedules, allSchedules, completedSchedules, deleteScheduleDatabase, updateScheduleDatabase, deleteNetworkDatabase, updateNetworkDatabase
from AutomacaoInstagram.ExtrairInfos import userAutenticateInstagram, alterFilename, validateIsVideos

class TestesRotas(unittest.TestCase):
    def teste_userAutenticateInstagram(self):
        self.assertTrue(userAutenticateInstagram('testeUser','testePassword'))


    def teste_authLogin(self):
        self.assertTrue(authLogin())
    

    def teste_insertUser(self):
        self.assertTrue(insertUser('testeUser','testePassword','teste','teste@teste.com'))


    def teste_registerUserNetwork(self):
        self.assertTrue(insertUserNetwork('testeUser','testePassword',1,0))


if __name__ == "__main__":
    unittest.main()