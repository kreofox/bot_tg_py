import urllib.request 
import urllib.parse
import base64


class RestApi:
    """class for using smsfeedback.ru service via GET requests"""

    __host = 'api.smsfeedback.ru'

    def __init__(self, api_login, api_password):
        self.login = api_login
        self.password = api_password

    def __sendRequest(self, uri, params=None):
        url = self.__getUrl(uri, params)
        request = urllib.request.Request(url)
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, self.login, self.password)
        authhandler = urllib.request.HTTPBasicAuthHandler(passman)

        opener = urllib.request.build_opener(authhandler)
        data = opener.open(request).read()
        return data


    def __getUrl(self, uri, params=None):
        url = "http://%s/messages/v2/%s/" % (self.getHost(), uri)
        paramStr = ''
        localList = { } if params is None else params.copy()
        if params is not None:
            for k, v in params.items():
                if v is None:
                    del localList[k]
            paramStr = urllib.parse.urlencode(localList)
        return "%s?%s" % (url, paramStr)

    def getHost(self):
        """Return current requests host """
        return self.__host

    def setHost(self, host):
        """Changing default requests host """
        self.__host = host

    def send(self, phone, text, sender='RATE-THIS',
             statusQueueName=None, scheduleTime=None, wapurl=None):
        """Sending sms """
        params = {'phone': phone,
                  'text': 'RATE-THIS code: {}'.format(text),
                  'sender': sender,
                  'statusQueueName': statusQueueName,
                  'scheduleTime': scheduleTime,
                  'wapurl': wapurl
                  }
        return self.__sendRequest('send', params)

    def status(self, id):
        """Retrieve sms status by it's id """
        params = {'id': id}
        return self.__sendRequest('status', params)

    def statusQueue(self, statusQueueName, limit=5):
        """Retrieve latest statuses from queue """
        params = {'statusQueueName': statusQueueName, 'limit': limit}
        return self.__sendRequest('statusQueue', params)

    def balance(self):
        """Retrieve current balance """
        return self.__sendRequest('balance')

    def senders(self):
        """Retrieve available signs """
        return self.__sendRequest('senders')