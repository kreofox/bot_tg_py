import mysql.connector
import datetime


class Product:
    def __init__(self, connectOption):
        self.db = mysql.connector.connect(
            host = connectOption['host'],
            user = connectOption['username'],
            password = connectOption['password'],
            database = connectOption['dbname']
        )
    def buyout(self, task1, status, date):
        self.db.reconnect()
        if date:
            sqlScript = "SELECT COUNT(*) AS count, article, price_wb FROM client  WHERE task1 = '{0}' AND status IN({1}) AND date_add = '{2}'".format(
                task1, status, date)
            if(status == '0,1'):
                sqlScript = "SELECT COUNT(*) AS count, article, price_wb FROM client   WHERE task1 = '{0}' AND date_add = '{2}' AND (status IN(0,1,2) OR status IS NULL)".format(task1, status, date)


        else:
            sqlScript = "SELECT COUNT(*) AS count, article FROM client  WHERE task1 = {0} AND status IN({1}) GROUP BY article".format(task1, status)
            if (status == '0,1'):
                sqlScript = "SELECT COUNT(*) AS count, article FROM client  WHERE task1 = {0} AND (status IN(0,1) OR status IS NULL) GROUP BY article".format(task1, status)
        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        return answer
    def delivery(self, task1, status, date):
        self.db.reconnect()
        print(date)
        if date:
            sqlScript = "SELECT COUNT(*) AS count, article FROM client  WHERE task1 = {0} AND date_get = '{2}'".format(task1, status, date)
        else:
            sqlScript = "SELECT COUNT(*) AS count, article FROM client  WHERE task1 = {0} AND status IN({1})".format(task1, status)

        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        return answer

    def review(self, task1, status, date):
        self.db.reconnect()
        if date:
            sqlScript = "SELECT COUNT(*) AS count, article FROM client  WHERE task1 = '{0}' AND status IN({1}) AND date_otziv = '{2}'".format(
                task1, status, date)
        else:
            sqlScript = "SELECT COUNT(*) AS count, article FROM client t  WHERE task1 = {0} AND t.type = 'отзыв'  AND status IN({1}) AND date_otziv IS NOT NULL GROUP BY article".format(
                task1, status)

        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        return answer

    def getDateVariable(self, type, task1):
        if type == 1:
            sqlScript = "SELECT date_buy FROM client WHERE status IN(1,2,3,4,5,6,7,8) AND task1 = '{0}' GROUP BY date_buy".format(task1)
        elif type == 2:
            sqlScript = "SELECT date_get FROM client WHERE status IN(4,5,6,7,8) AND task1 = '{0}' GROUP BY date_get".format(task1)
        elif  type == 3:
            sqlScript = "SELECT date_otziv FROM client WHERE status IN(6,7,8) AND task1 = '{0}' GROUP BY date_otziv".format(task1)
        self.db.reconnect()
        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        return answer

    def report(self, type, task, dateType, date = datetime.date.today().strftime("%y-%m-%d")):
        self.db.reconnect()
        task1 = int(task)
        if type == 1:
            if dateType == 1:
                sqlScript = "SELECT article, date_buy, COUNT(*) as cnt, naming, price FROM client WHERE date_buy = '{0}' AND status IN (1,2,3,4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 2:
                sqlScript = "SELECT article, date_buy, COUNT(*) as cnt, naming, price FROM client WHERE date_buy > DATE_SUB(CURDATE(),INTERVAL 7 DAY)  AND status IN (1,2,3,4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 3:
                sqlScript = "SELECT article, date_buy, COUNT(*) as cnt, naming, price FROM client WHERE date_buy > DATE_SUB(CURDATE(),INTERVAL 31 DAY) AND status IN (1,2,3,4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 4:
                sqlScript = "SELECT article, date_buy, COUNT(*) as cnt, naming, price FROM client WHERE date_buy = '{0}' AND status IN (1,2,3,4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(date, task1)
            elif dateType == 5:
                sqlScript = "SELECT article, date_buy, COUNT(*) as cnt, naming, price FROM client WHERE status IN (1,2,3,4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article, price, date_buy".format(date, task1)


        elif type == 2:
            if dateType == 1:
                sqlScript = "SELECT article, date_get, COUNT(*) as cnt, naming, price FROM client WHERE date_get = '{0}' AND status IN (4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 2:
                sqlScript = "SELECT article, date_get, COUNT(*) as cnt, naming, price FROM client WHERE DATE(date_get) > DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND status IN (4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 3:
                sqlScript = "SELECT article, date_get, COUNT(*) as cnt, naming, price FROM client WHERE DATE(date_get) > DATE_SUB(CURDATE(),INTERVAL 31 DAY) AND status IN (4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 4:
                sqlScript = "SELECT article, date_get, COUNT(*) as cnt, naming, price FROM client WHERE date_get = '{0}' AND status IN (4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article".format(date, task1)
            elif dateType == 5:
                sqlScript = "SELECT article, date_get, COUNT(*) as cnt, naming, price FROM client  WHERE status IN (4,5,6,7,8) AND mp = 'wb' AND task1 = {1} GROUP BY article, price, date_get".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)



        elif type == 3:
            if dateType == 1:
                sqlScript = "SELECT date_otziv, status, article, text_otziv, naming, screen_otziv FROM client WHERE date_otziv = '{0}' AND status IN (6,7,8) AND mp = 'wb' AND task1 = {1}".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 2:
                sqlScript = "SELECT date_otziv, status, article, text_otziv, naming, screen_otziv FROM client WHERE date_otziv > DATE_SUB(NOW(),INTERVAL 7 DAY) AND status IN (6,7,8) AND mp = 'wb' AND task1 = {1}".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 3:
                sqlScript = "SELECT date_otziv, status, article, text_otziv, naming, screen_otziv FROM client WHERE date_otziv > DATE_SUB(NOW(),INTERVAL 31 DAY) AND status IN (6,7,8) AND mp = 'wb' AND task1 = {1}".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)
            elif dateType == 4:
                sqlScript = "SELECT date_otziv, status, article, text_otziv, naming, screen_otziv FROM client WHERE date_otziv = '{0}' AND status IN (6,7,8) AND mp = 'wb' AND task1 = {1}".format(date, task1)
            elif dateType == 5:
                sqlScript = "SELECT date_otziv, status, article, text_otziv, naming, screen_otziv FROM client WHERE mp = 'wb' AND task1 = {1}".format(
                    datetime.date.today().strftime("%y-%m-%d"), task1)
        elif type == 4:
            sqlScript = "SELECT status, grafik, `type`, article, `size`, search_key, brand, naming, date_buy, date_get, price, text_otziv, date_otziv FROM client WHERE mp = 'wb' AND task1 = {0}".format(task1)

        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        print(answer)
        return answer



    def getSortProduct(self, type, article, dateType, task1):
        self.db.reconnect()
        if type == 1:
            if dateType == 2:
                sqlScript = "SELECT article, date_buy, COUNT(*) as cnt, naming, price FROM client WHERE article = '{0}' AND date_buy > DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND task1 = '{1}' GROUP BY date_buy, price"

            elif dateType == 3:
                sqlScript = "SELECT article, date_buy, COUNT(*) as cnt, naming, price FROM client WHERE article = '{0}' AND date_buy > DATE_SUB(CURDATE(),INTERVAL 31 DAY) AND task1 = '{1}'  GROUP BY date_buy, price"
        elif type == 2:
            if dateType == 2:
                sqlScript = "SELECT article, date_get, COUNT(*) as cnt, naming, price FROM client WHERE article = '{0}' AND date_get > DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND task1 = '{1}'  GROUP BY date_buy, price"

            elif dateType == 3:
                sqlScript = "SELECT article, date_get, COUNT(*) as cnt, naming, price FROM client WHERE article = '{0}' AND date_get > DATE_SUB(CURDATE(),INTERVAL 31 DAY)  AND task1 = '{1}' GROUP BY date_buy, price"

        elif type == 3:
            if dateType == 2:
                sqlScript = "SELECT article, date_otziv, COUNT(*) as cnt, naming, price FROM client WHERE article = '{0}' AND date_otziv > DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND task1 = '{1}'  GROUP BY date_buy, price"

            elif dateType == 3:
                sqlScript = "SELECT article, date_otziv, COUNT(*) as cnt, naming, price FROM client WHERE article = '{0}' AND date_otziv > DATE_SUB(CURDATE(),INTERVAL 31 DAY) AND task1 = '{1}'  GROUP BY date_buy, price"
        sqlScript = sqlScript.format(article, task1)
        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        print(answer)
        return answer


    def getUsersNot(self):
        self.db.reconnect()
        sqlScript = "SELECT task1, user_id FROM client_data WHERE user_id IS NOT NULL"
        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        print(answer)
        return answer

        