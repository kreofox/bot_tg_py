from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import dto.Product as prDto
import dto.User as userDTO
productDB = prDto.Product({'host': 'j45316134.myjino.ru', 'username': 'j45316134', 'password': 'cf}j}R75tRzM', 'dbname': 'j45316134', })
userDB = userDTO.User({'host': 'j45316134.myjino.ru', 'username': 'j45316134', 'password': 'cf}j}R75tRzM', 'dbname': 'j45316134', })


class Button:
    def __init__(self):
        pass
    def getDateReport(self, type, username):
        user = userDB.getUser(username)
        print(user)
        task = user[0][4]

        answer = productDB.getDateVariable(type, task)

        print(answer)

    def phoneBTN(self):
        button_hi = KeyboardButton('📑 Телефон 📊', request_contact=True)
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_hi)

        return greet_kb
    def startButton(self):
        button_hi = KeyboardButton('📑 Отчет 📊')
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_hi)
        button_hi = KeyboardButton('📑 Функционал 💬')
        greet_kb.add(button_hi)
        button_hi = KeyboardButton('📑 Кабинет 💬') 
        greet_kb.add(button_hi)

        return greet_kb
    def reportButton(self):
        inline_btn_1 = InlineKeyboardButton('🛍 Выкупы 🛍', callback_data='reportType|1')
        inline_btn_2 = InlineKeyboardButton('📦 Доставки 📦', callback_data='reportType|2')
        inline_btn_3 = InlineKeyboardButton('💬 Отзывы 💬', callback_data='reportType|3')
        inline_btn_4 = InlineKeyboardButton('💬 Общий 💬', callback_data='reportType|4')
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4)


        return inline_kb1
    def reportTaskBtn(self, users):
        buttonList = []
        for i in users:
            buttonList.append([])
            buttonList[len(buttonList) - 1].append(InlineKeyboardButton('ваш уникальный номер: {0}'.format(i[4]), callback_data='task-report|{0}'.format(i[4])))
            #InlineKeyboardMarkup().add(InlineKeyboardButton('🛍 день: {0} 🛍'.format(i[0]), callback_data='reportdt|{0}'.format(i[0])))
        print(buttonList)
        inline_kb1 = InlineKeyboardMarkup(inline_keyboard=buttonList)
        return  inline_kb1
    def reportDateButton(self):
        inline_btn_1 = InlineKeyboardButton('🛍 За день 🛍', callback_data='report date|1')
        inline_btn_2 = InlineKeyboardButton('📦 За неделю 📦', callback_data='report date|2')
        inline_btn_3 = InlineKeyboardButton('💬 За месяц 💬', callback_data='report date|3')
        inline_btn_4 = InlineKeyboardButton('💬 Конкретный день 💬', callback_data='report date|4')
        inline_btn_5 = InlineKeyboardButton('💬 Все время 💬', callback_data='report date|5')
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3 , inline_btn_4, inline_btn_5)


        return inline_kb1
    def currentDayReport(self, username, type):
        user = userDB.getUser(username)
        print(user)
        task = user[0][4]
        dateList = productDB.getDateVariable(type, task)
        buttonList = []
        for i in dateList:
            buttonList.append([])
            buttonList[len(buttonList) - 1].append(InlineKeyboardButton('🛍 день: {0} 🛍'.format(i[0]), callback_data='reportdt|{0}'.format(i[0])))
            #InlineKeyboardMarkup().add(InlineKeyboardButton('🛍 день: {0} 🛍'.format(i[0]), callback_data='reportdt|{0}'.format(i[0])))
        print(buttonList)
        inline_kb1 = InlineKeyboardMarkup(inline_keyboard=buttonList)


        return inline_kb1

