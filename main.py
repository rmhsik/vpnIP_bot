from telegram.ext import Updater
from telegram.ext import CommandHandler,MessageHandler, Filters
from telegram import InlineKeyboardButton
from telegram import ReplyKeyboardMarkup
import subprocess
import socket

with open('tokenfile.txt','r') as file:
    token_str = file.readlines()[0].strip('\n')
updater = Updater(token=token_str)

with open('chatid.txt','r') as file:
    chatidfile = file.readlines()
whitelist = [item.strip("\n") for item in chatidfile]

def isAllowed(chatid,whitelistedIDs):
    if str(chatid) in whitelistedIDs:
        return True
    else:
        return False

def start(update,context):
    #menu = [InlineKeyboardButton(text='Get IP',callback_data='getip')]
    menu = [["Get IP"]]
    menuKeyboard = ReplyKeyboardMarkup(menu)
    #context.bot.send_message(chat_id=update.effective_chat.id,text='Hello world!')
    if isAllowed(update.effective_chat.id,whitelist):
        context.bot.send_message(chat_id=update.effective_chat.id,text='Bot to reply the IP from tun0 interface',reply_markup=menuKeyboard)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text='User not allowed')

def execGetIP():
    command = ["./command"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('UTF-8').strip("\n")
    data = socket.gethostname() + ": " + output
    if output == '':
        output = "No IP found"
        data = socket.gethostname() + ": " + output
    if error == None:
        return data
    else:
        return "Error getting IP!"


def action(update,context):
    if isAllowed(update.effective_chat.id,whitelist): 
        if update.message.text == 'Get IP':
            data = execGetIP()
            context.bot.send_message(chat_id=update.effective_chat.id,text=data)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text='User not allowed')
#menu = [InlineKeyboardButton(text='Get IP',callback_data='getip')]
#menu = [["Get IP"]]
#menuKeyboard = ReplyKeyboardMarkup(menu)

dispatcher = updater.dispatcher
start_handler = CommandHandler('start',start)
reply_handler = MessageHandler(Filters.text & (~Filters.command),action)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(reply_handler)
updater.start_polling()
