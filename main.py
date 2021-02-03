# muantibot v 1.1
#---------------------------------------
from telegram import *
from telegram.ext import *
from telegram.ext.dispatcher import *
from sqlite3 import Error
import random, os, sqlite3
#///////////////////////////////////////
if not os.path.exists('authorizedUser'):
    os.makedirs('authorizedUser')

dic = {}
cuntid=0
keys=[]
entries = os.listdir('img/') 
for i in entries:
     keys.append(i.split('.')[0])

#/////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////
def check_if_string_in_file(file_name, string_to_search): # Completed
    try:
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if string_to_search in line:
                    return string_to_search
        return False
    except:
        pass
def check_repetition(): # Completed
    try:
        lines_seen = set() # holds lines already seen
        with open("authorizedUser/auserO.txt", "w") as output_file:
            for each_line in open("authorizedUser/auser.txt", "r"):
                if each_line not in lines_seen: # check if line is not duplicate
                    output_file.write(each_line)
                    lines_seen.add(each_line)
        os.remove('authorizedUser/auser.txt')
        os.rename('authorizedUser/auserO.txt', 'authorizedUser/auser.txt')
    except:
        pass
def delete_user(x): # Completed
    try:
        a_file = open("authorizedUser/auser.txt", "r")
        lines = a_file.readlines()
        a_file.close()

        new_file = open("authorizedUser/auser.txt", "w")
        for line in lines:
            if line.strip("\n") != f"{x}":
                new_file.write(line)

        new_file.close()
    except:
        pass
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def add_to_database(tableName, id, status, warning):
    try:
        con = sqlite3.connect('DB/mydatabase.db')
        con.execute(f"CREATE TABLE IF NOT EXISTS db_{tableName} (id, status, warning);")
        cur = con.execute(f'select * from db_{tableName} where id = {id}')

        if(cur.fetchone() is None):
            print('if')
            con.execute(f"INSERT INTO db_{tableName} (id, status, warning) \
                VALUES ({id}, '{status}', {warning})");
            con.commit()
    except Error:
        print(Error)
    finally:
        con.close()

def ping(update:Update, context:CallbackContext): # Completed
    print('ping')
    try:
        if(update.message.from_user.id==806733685):
            bot.send_message(chat_id=update.message.chat_id, text='i am ready',reply_to_message_id=update.message.message_id) 
        else:
            pass
    except:
        pass
def join(update:Update, context:CallbackContext): # Completed v1.1
    try:
        idUser = update.message.new_chat_members[0].id
        if(update.message.new_chat_members[0].id!=bot.id):
            img = random.choice([x for x in os.listdir("img/")
                        if os.path.isfile(os.path.join("img/", x))])
            
            kis = img.split('.')[0]
            keys.remove(kis)
            new_list = random.sample(set(keys), 3)
            new_list.append(kis)
            random.shuffle(new_list)
            keys.append(kis)

            Keyboard = [
                [InlineKeyboardButton(new_list[0] , callback_data=new_list[0]),
                InlineKeyboardButton(new_list[1], callback_data=new_list[1])],
                [InlineKeyboardButton(new_list[2], callback_data=new_list[2]),
                InlineKeyboardButton(new_list[3], callback_data=new_list[3])]
            ]
            chat_id = update.message.chat_id

            msgbut = bot.send_photo(chat_id=chat_id ,reply_to_message_id=update.message.message_id, photo=open(f'img/{img}','rb'),caption=f"{update.message.from_user.first_name} عزیز\nبرای چت در گروه تصویر درست را انتخاب نمایید", reply_markup=InlineKeyboardMarkup(Keyboard))
            dic[idUser]={'chatid':chat_id, 'msgid':msgbut.message_id, 'img':kis}
        else:
            bot.send_message(chat_id=update.message.chat_id, text='please admin me\nfor working')
    except:
        pass

def left(update:Update, context:CallbackContext): # Completed v1.1
    try:
        idu = update.message.left_chat_member.id
        for i in dic:
            if(i==idu):
                bot.delete_message(chat_id=int(dic[i]['chatid']), message_id=int(dic[i]['msgid']))
            else:
                pass
    except:
        pass
def button(update:Update, context:CallbackContext): # Completed v1.1
    try:
        query = update.callback_query
        user = query.message.reply_to_message.new_chat_members[0].id
        chat_id = dic[user]['chatid']
        message_id = dic[user]['msgid']
        img = dic[user]['img']
        
        #?////////////////////////////////
        tableName = str(bot.get_chat(chat_id=update.effective_chat.id).id).split('-')[1]
        status = "active"
        warning = 0
        if(query.message.reply_to_message.new_chat_members[0].id==query.from_user.id):
            if(query.data.__eq__(img)):
                print('OK')
                bot.delete_message(chat_id=chat_id, message_id=message_id)
                add_to_database(tableName, user, status, warning)
                print('Done')
            else:
                bot.answer_callback_query(callback_query_id=query.id, text="شما حذف شدید دوباره جوین شده و گزینه صحیح را بزنید", show_alert =True)
                bot.kick_chat_member(chat_id=chat_id, user_id=query.from_user.id)
                dic.pop(query.from_user.id)
                bot.delete_message(chat_id=chat_id, message_id=message_id)
        else:
            bot.answer_callback_query(callback_query_id=query.id, text="شما نمیتوانید انتخاب کنید", show_alert =True)
    except:
        pass  
  
def newMessages(update:Update, context:CallbackContext): 
    try:
        msg = update.message.message_id
        chat_id = update.message.chat_id
        if(str(update.message.from_user.id) == str(check_if_string_in_file('authorizedUser/auser.txt', str(update.message.from_user.id)))):
            bot.delete_message(chat_id=chat_id, message_id=msg)
        else:
            pass
    except:
        pass

#/////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    Token = "1681656442:AAH_acqDhDv5LOX6RJAaTLeklyOlISVI8qo"
    bot = Bot(Token)
    updater = Updater(Token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('ping',ping))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, join))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, left))
    dispatcher.add_handler(MessageHandler(Filters.text, newMessages))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    print('START')
    updater.idle()
