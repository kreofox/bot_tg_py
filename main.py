print("version 1")
from threading import Thread
# import modules
import logging
from aiogram import Bot, Dispatcher, executor, types
import service.notify as nt
#self modules
import modules.product as pr
import service.button as btn
import modules.user as user
import mysql.connector


usersTaskReport = {}

API_TOKEN = '6064527659:AAFhLaVPjMcQBGQoqKoSPKoaR0YD7NKct6w'    # bot token here

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

Product = pr.Product()
User = user.User()
Button = btn.Button()
# command for bot
commentText = {

    '/start': 'start',

    'Отчеты': Product.reports,

    'Что умеет бот': '''Комманды бота:
     
        start :   запускает бота, используется всего 1 раз при запуске бота
        
        help : 
            instruction:   выводит полную документацию к боту
            info:   выводит информацию, и статистику к боту 
        command:   выводит полные команды
    '''

}
getPhone = []
smsCode = []
smsPhone = []
lastMsg = False
userTaskSet = {
}
@dp.message_handler()
async def send_message(message: types.Message):
    global lastMsg
    print()
    isLog = User.checkLog(message.from_user.id)
    if lastMsg:
        await lastMsg.delete()
        lastMsg = False
    if message.from_user.id in smsCode and (message.text.split(" ")[0] in commentText) == False:
        answer = User.checkSMS(message.from_user.id, message.text, smsPhone[smsCode.index(message.from_user.id)])
        if answer[1]:
            isUsers = User.getIsUsers(message.from_user.id)
            if (len(isUsers) > 1):
                btn = Button.reportTaskBtn(isUsers)
                usersTaskReport[message.from_user.id] = False
                await bot.send_message(message.from_user.id, 'Выберете Личный Кабинет!', reply_markup=btn)
            else:
                usersTaskReport[message.from_user.id] = isUsers[0][4]
                Product.dayPushOne(isUsers[0][4], message.from_user.id)
                Product.setTask(isUsers[0][4], message.from_user.id)
                btnSetting = Button.startButton()
                await message.reply("Теперь вам доступен полный функционал БОТА", reply_markup=btnSetting)
            smsCode.remove(message.from_user.id)
        else:
            lastMsg = await message.answer(answer[0])

    if message.from_user.id in getPhone and (message.text.split(" ")[0] in commentText) == False:

        answer = User.userLog(message.from_user.id, message.text)
        lastMsg = await message.answer(answer[0])
        if answer[1]:
            getPhone.remove(message.from_user.id)
            smsPhone.append(message.text)
            smsCode.append(message.from_user.id)


    if message.text.split(" ")[0] in commentText:
        if message.from_user.id in getPhone:
            getPhone.remove(message.from_user.id)
        if message.from_user.id in smsCode:
            smsCode.remove(message.from_user.id)

        if type(commentText[message.text.split(" ")[0]]) == str:
            if message.text == '/start':
                lastMsg = await message.answer("Рады приветсвовать вас в RATE-THIS tg BOT")
                answer = User.checkLog("{0}".format(message.from_user.id))
                if answer[1]:
                    btnSetting = Button.phoneBTN()
                    getPhone.append(message.from_user.id)
                    lastMsg = await message.answer(answer[0], reply_markup=btnSetting)
                else:
                    isUsers = User.getIsUsers(message.from_user.id)
                    if(len(isUsers) > 1):
                        btn = Button.reportTaskBtn(isUsers)
                        usersTaskReport[message.from_user.id] = False
                        await bot.send_message(message.from_user.id, 'Выберете Личный Кабинет', reply_markup=btn)
                    else:
                        usersTaskReport[message.from_user.id] = isUsers[0][4]
                        Product.setTask(isUsers[0][4], message.from_user.id)
                        Product.dayPushOne(isUsers[0][4], message.from_user.id)
                        btnSetting = Button.startButton()
                        await message.reply("Теперь вам доступен полный функционал БОТА", reply_markup=btnSetting)

                print(answer[0])
        else:
            Button.getDateReport(1, message.from_user.id)
            print(Product.reports(message.from_user.id, 1, 3))

    print(123132, message.text == "📑 Отчет 📊")
    if message.text == "📑 Отчет 📊" and isLog[1] == False:
        btnSetting = Button.reportButton()
        lastMsg = await message.reply('''Выберите пожалуйста необходимый отчет 📑
❗️Все отчеты позволяют получить информацию за сегодня, за неделю, месяц, за все время, или конкретный день. 
🛍Выкупы- Позволяет узнать какие товары когда были заказаны. 
📦Доставки- Позволяет узнать какие товары когда были забраны 
💬Отзывы- Позволяет узнать какой статус у отзыва и когда он был опубликован 
🔥Общий отчёт- Он позволяет посмотреть по каждому товару статус и всю необходимую информацию.''', reply_markup=btnSetting)
    elif message.text == "📑 Функционал 💬" and isLog[1] == False:
        lastMsg = await message.reply('''👋 Данный бот, предназначен, для того что бы уведомлять вас, о статусе вашего заказа.
🔥Бот расскажет вам:

1️⃣ Какой у нас план на день
2️⃣ Сверяет с выполнением плана 
3️⃣ Говорит о получении товара
4️⃣ О статусах товара на пвз
5️⃣ Уведомляет вас о постановке на сборку корзины 
6️⃣ Когда мы заказываем ваш товар, 
7️⃣ Когда мы публикуем на него отзывы. 
8️⃣ Статус о прохождении модерации 
Данный бот может быстро выгрузить следующие отчеты:
🛍 По выкупам, 
💬 Отзывам, 
📦 Доставкам. 
Данный бот позволяет нам сделать нашу с вами работу прозрачнее. 😘
Если у вас возникли трудности, пожалуйста напишите сюда ↙️
@Rate_this_grop_bot''')
    elif message.text == '📑 Кабинет 💬' and isLog[1] == False:
        isUsers = User.getIsUsers(message.from_user.id)
        btn = Button.reportTaskBtn(isUsers)

        await bot.send_message(message.from_user.id, 'Выберете Личный Кабинет', reply_markup=btn)
    if message.text == 'rate-this':
        Product.nightPush()



typeList = {

}

@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
    global lastMsg, usersTaskReport
    if lastMsg:
        await lastMsg.delete()
        lastMsg = False
    query = callback_query.data
    isLog = User.checkLog(callback_query.from_user.id)
    if 'task-report' in query:
        if not usersTaskReport[callback_query.from_user.id]:
            btnSetting = Button.startButton()
            await bot.send_message(callback_query.from_user.id, "Теперь вам доступен полный функционал БОТА", reply_markup=btnSetting)
        print(query.split('|')[1])
        Product.dayPushOne(query.split('|')[1], callback_query.from_user.id)
        Product.setTask(query.split('|')[1], callback_query.from_user.id)
        usersTaskReport[callback_query.from_user.id] = query.split('|')[1]

    if "reportType" in query and isLog[1] == False:
        if query.split('|')[1] == '4':
            answer = Product.reports(callback_query.from_user.id, int(query.split('|')[1]), 5)
            doc = open(answer, 'rb')
            await bot.send_document(chat_id=callback_query.from_user.id, document=doc, caption=f"Данные успешно сохранены!")
        else:
            btnSetting = Button.reportDateButton()
            typeList[callback_query.from_user.id] = int(query.split('|')[1])
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, 'Выберете сроки!', reply_markup=btnSetting)
        await callback_query.message.delete()
    elif "report date" in query and isLog[1] == False:

        if query.split('|')[1] == '4':
            print(query.split('|')[1])
            btnSetting = Button.currentDayReport(callback_query.from_user.id, typeList[callback_query.from_user.id])

            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, 'Выберете сроки!', reply_markup=btnSetting)
        else:
            answer = Product.reports(callback_query.from_user.id, typeList[callback_query.from_user.id], int(query.split('|')[1]))
            doc = open(answer, 'rb')
            await bot.send_document(chat_id=callback_query.from_user.id, document=doc,caption=f"Данные успешно сохранены!")
        await callback_query.message.delete()
    elif "reportdt" in query and isLog[1] == False:
        answer = Product.reports(callback_query.from_user.id, typeList[callback_query.from_user.id], 4, query.split('|')[1])
        doc = open(answer, 'rb')
        await bot.send_document(chat_id=callback_query.from_user.id, document=doc, caption=f"Данные успешно сохранены!")
    await callback_query.message.delete()


@dp.message_handler(content_types=['contact'])
async def contact(message):
    global lastMsg
    if lastMsg:
        await lastMsg.delete()
        lastMsg = False
    if message.from_user.id in getPhone:

        answer = User.userLog(message.from_user.id, str(message.contact.phone_number))
        await message.answer(answer[0])
        if answer[1]:
            getPhone.remove(message.from_user.id)
            smsPhone.append(message.contact.phone_number)
            smsCode.append(message.from_user.id)
    await message.delete()
th = Thread(target=nt.checkNot)
th.start()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

