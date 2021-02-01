# muantibot v 1.0
#---------------------------------------
from telegram import *
from telegram.ext import *
from telegram.ext.dispatcher import *
import random, os
#//////////////////////////////////////////////////////////////////////////////////////

cuntid=0
keys=[]
entries = os.listdir('img/') # Make list Keys
for i in entries:
     keys.append(i.split('.')[0])

def ping(update:Update, context:CallbackContext):
    print('ping')
    bot.send_message(chat_id=update.message.chat_id, text='i am ready',reply_to_message_id=update.message.message_id) 

def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return string_to_search
    return False

def check_repetition():
    lines_seen = set() # holds lines already seen
    with open("authorizedUser/auserO.txt", "w") as output_file:
        for each_line in open("authorizedUser/auser.txt", "r"):
            if each_line not in lines_seen: # check if line is not duplicate
                output_file.write(each_line)
                lines_seen.add(each_line)
    os.remove('authorizedUser/auser.txt')
    os.rename('authorizedUser/auserO.txt', 'authorizedUser/auser.txt')

def delete_user(x):
    a_file = open("authorizedUser/auser.txt", "r")
    lines = a_file.readlines()
    a_file.close()

    new_file = open("authorizedUser/auser.txt", "w")
    for line in lines:
        if line.strip("\n") != f"{x}":
            new_file.write(line)

    new_file.close()


def join(update:Update, context:CallbackContext):
    idUser = update.message.from_user.id
    f = open('authorizedUser/auser.txt', 'a')
    f.write(f"{idUser}\n")
    f.close()
    check_repetition() 
    
    img = random.choice([x for x in os.listdir("img/")
               if os.path.isfile(os.path.join("img/", x))])

    kis = img.split('.')[0]
    keys.remove(kis)
    new_list = random.sample(set(keys), 3)
    new_list.append(kis)
    random.shuffle(new_list)
    keys.append(kis)

    context.user_data['sub'] = img.split('.')[0]

    Keyboard = [
        [InlineKeyboardButton(new_list[0] , callback_data=new_list[0]),
        InlineKeyboardButton(new_list[1], callback_data=new_list[1])],
        [InlineKeyboardButton(new_list[2], callback_data=new_list[2]),
        InlineKeyboardButton(new_list[3], callback_data=new_list[3])]
    ]
    chat_id = update.message.chat_id

    msgbut = bot.send_photo(chat_id=chat_id ,reply_to_message_id=update.message.message_id, photo=open(f'img/{img}','rb'),caption=f"{update.message.from_user.first_name} عزیز\nبرای چت در گروه تصویر درست را انتخاب نمایید", reply_markup=InlineKeyboardMarkup(Keyboard))
    context.user_data['msgid'] = msgbut.message_id
    context.user_data['chatid'] = chat_id

def button(update:Update, context:CallbackContext):
    query = update.callback_query
    
    msgid = context.user_data.get('msgid')
    chat_id = context.user_data.get('chatid')
    if(msgid==query.message.message_id):
        if(query.data.__eq__(context.user_data.get('sub'))):
            bot.delete_message(chat_id=chat_id, message_id=msgid)
            delete_user(query.from_user.id)
        else:
            bot.answer_callback_query(callback_query_id=query.id, text="شما حذف شدید دوباره جوین شده و گزینه صحیح را بزنید", show_alert =True)
            bot.kick_chat_member(chat_id=chat_id, user_id=query.from_user.id)
    else:
        bot.answer_callback_query(callback_query_id=query.id, text="شما نمیتوانید انتخاب کنید", show_alert =True)
    
def newMessages(update:Update, context:CallbackContext):
    msg = update.message.message_id
    chat_id = update.message.chat_id
    if(str(update.message.from_user.id) == str(check_if_string_in_file('authorizedUser/auser.txt', str(update.message.from_user.id)))):
        bot.delete_message(chat_id=chat_id, message_id=msg)
    else:
        pass

if __name__ == "__main__":
    Token = "1652811680:AAHSaaTxF4Hs0ZkPzFKFV28jOVSHyNX6OS4"
    bot = Bot(Token)
    updater = Updater(Token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('ping',ping))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, join))
    dispatcher.add_handler(MessageHandler(Filters.all,newMessages))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()
