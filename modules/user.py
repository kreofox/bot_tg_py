from dto.User import User as userDTO
from service.sms import RestApi as smsApi
import random


userDB = userDTO.User({
    'host': 'j45316134.myjino.ru', 
    'username': 'j45316134', 
    'password': 'cf}j}R75tRzM', 
    'dbname': 'j45316134', 
    })
sms = smsApi('rate-this', 'KoBe6263')



class User:
    def userLog(self, username, phone):
        code = random.randint(11111, 99999)

        userDB.setCode(username, code)
        answer = sms.send(phone.replace('+', ""), code)

        if 'error'.encode() in answer:
            return[ "error number phone", False]
        return ["Отлично введите код отправленный вам по смс", True]

    def checkLog(self, username):
        user = userDB.getUser(username)

        if len(user) < 1:

            text = 'придется авторизоваться'
            return [text, True]
        else:
            text = 'мы очень рады что вы с нами'
            return [text, False]

    def getIsUsers(self, tgId):
        user = userDB.getUser(tgId)
        phone = user[0][5]
        isUsers = userDB.getUserByPhone(phone)
        
        return isUsers
    
    def checkSMS(self, username, sms_code, phone):
        answer = userDB.checkCode(username, sms_code)
        
        if len(answer) < 1:
            return ['Неверный код', False]
        
        phone = phone.replace('+', '')
        user = userDB.getUserByPhone(phone)
        
        if len(user) > 0:
            userDB.updateUser(username, user[0][5])
        
        else:
            task1 = random.randint(1111111111111111111, 9999999999999999999)
            userDB.createUser(username, phone.replace('+', ''), task1, 1111)
        return ['Вы успешно зарегестрированны', True]