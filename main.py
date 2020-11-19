#Не уверен что будет совпадать с тем что нужно на 100% так как не смотрел никакие видео, писал все сам. Главное работает как в инструкции)

import requests
import telebot
import json
import pyTelegramBotAPI



class myException(Exception):
    def __init__(self,text):
        self.txt = text



MainCurrence = "USD"
rates = requests.get("https://api.exchangeratesapi.io/latest?base="+MainCurrence)

#print(rates.content)

GetCurrencyRequestError = myException("Error, the format of data is incorrect!")



rates_json = json.loads(rates.content)
#print(rates_json['rates'])
rates_json = rates_json['rates']
#print(rates_json.keys())
ArrayOfKeys = list(rates_json.keys())
rates_for_user = []
print(ArrayOfKeys)
for i in range(0,len(ArrayOfKeys)):
    rates_for_user.append(str(ArrayOfKeys[i]) + ": " + str(rates_json[ArrayOfKeys[i]])+ " \n")
print("")
#rates_for_user = str(rates_for_user)
print(rates_for_user[2])


TOKEN = "1444968795:AAFXMedQFHgpbKs39D14Le9cHbBdXDvahic"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def gotCommands(command: telebot.types.BotCommand):
   bot.send_message(command.chat.id,"I can help you to convert one currency in other! But I need to get an information in correct order: ")
   bot.send_message(command.chat.id, "<name of currency which you want to convert> <name of currency in which you want to get price of first currency> <value>")
   bot.send_message(command.chat.id, "to get this instruction again write /help. To get list of available currencies write /values ")

@bot.message_handler(commands=['values'])
def gotCommands(command: telebot.types.BotCommand):
   bot.send_message(command.chat.id,"Available currencies(based on US Dollar): ")

   for i in range(0,len(ArrayOfKeys)):
     bot.send_message(command.chat.id, rates_for_user[i])


@bot.message_handler(content_types=['text'])
def ConvertCurrency(message: telebot.types.Message):
    msgStr = message.text
    msgStr = msgStr.split()
    try:
        if len(msgStr) > 3 or len(msgStr) < 3:
            raise GetCurrencyRequestError
        new_rates = requests.get("https://api.exchangeratesapi.io/latest?base=" + msgStr[0])
        new_rates = json.loads(new_rates.content)
        new_rates = new_rates['rates'][msgStr[1]]
        FinalResultValue = str(float(msgStr[2]) * float(new_rates)) + msgStr[1]
        bot.send_message(message.chat.id, FinalResultValue)
        print(new_rates)

    except:
        bot.send_message(message.chat.id, GetCurrencyRequestError.txt)






bot.polling(none_stop=True)
