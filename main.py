
# извините если бот плохо написан :(
import random
import string
import telebot
from datetime import datetime, timedelta
bot = telebot.TeleBot("TOKEN HIDDEN")




# сохранение информации
students = []

# отправка новых ключей старостам
special_access = []
key1 = "ABCDE"
keylogincount = 0

def send_new_keys():
    global key1
    key1 = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    for tg_id in special_access:
        bot.send_message(tg_id, f"Новый ключ доступа: {key1}.")

# команды бота

@bot.message_handler(commands=["start"])
def start(message, res=False):

    bot.send_message(message.chat.id, "Добро пожаловать в бота учета посещаемости ФЭК РГЭУ (РИНХ!)📚\n"
                    " \n"
                     "🗓Здесь вы можете узнать посещаемость студентов и получить статистику пропусков студента\n"
                    " \n"
                                      "чтобы узнать подробно про команды напишите /info\n"
                     )


@bot.message_handler(commands=["login"])
def login(message, res=False):
    global keylogincount
    splitmessage = message.text.split()
    countcheck = 0
    for mes in splitmessage:
        countcheck += 1
    if countcheck >= 2:
        if splitmessage[1] == key1:
            special_access.append(message.chat.id)
            bot.send_message(message.chat.id, "Вы получили специальный доступ")
            keylogincount += 1
            if keylogincount >= 10:
                send_new_keys()


@bot.message_handler(commands=["info"])
def info(message, res=False):
    bot.send_message(message.chat.id, "ИНФОРМАЦИЯ ПО КОМАНДАМ\n"
                    "для получения специального доступа напишите '/login 1234567890ABCDE' (нужен работающий ключ)\n"
                    "\n"
                     "для того чтобы проверить пропуски существующего студента напишите '/student ГРУППА ФАМИЛИЯ ИМЯ ДАТА1 ДАТА2'\n"
                    "\n"
                     "группа - группа в которой состоит студент (например ИС-101)\n"
                    "дата1 - начало промежутка по которому вы хотите просмотреть пропуски (например 15.01.25)\n"
                    "дата2 - конец промежутка (напрмер 15.10.25)\n"
                    "\n"
                     "для того чтобы добавить студента напишите команду '/add ГРУППА ФАМИЛИЯ ИМЯ'\n"
                    "\n"
                     "для того чтобы поставить студенту пропуск напишите команду '/set ГРУППА ФАМИЛИЯ ИМЯ ДАТА УВАЖ/НЕУВАЖ'\n"
                    "\n"
                     "дата - дата пропуска за определенный день (например 15.11.25)\n"
                     "уваж/неуваж - пропуск по уважительной или не уважительной причине (нужно написать уваж либо неуваж)"
                     )


@bot.message_handler(commands=["add"])
def add(message, res=False):
    access = False
    for tg_id in special_access:
        if message.chat.id == tg_id:
            access = True
    if access:
        bot.send_message(message.chat.id, "проверяю существует ли такой студент...")
        args = message.text.split()
        countcheck = 0
        for mes in args:
            countcheck += 1
        if countcheck-1 >= 3:
            group = False
            for groupcheck in students:
                if args[1] == groupcheck[0]:
                    group = groupcheck

            if not group:
                students.append([args[1]])
                for groupcheck in students:
                    if args[1] == groupcheck[0]:
                        group = groupcheck

            student = False
            for existstudent in group:
                if existstudent != args[1]:
                    studentinfo = existstudent[0].split()
                    if studentinfo[0] == args[2] and studentinfo[1] == args[3]:
                        student = True

            if student:
                bot.send_message(message.chat.id, "этот студент уже есть в базе данных")
            else:
                group.append([str(str(args[2])+" "+str(args[3]))])
                bot.send_message(message.chat.id, "студент добавлен в базу данных")
        else:
            bot.send_message(message.chat.id, "НЕПРАВИЛЬНО ВВЕДЕНЫ ДАННЫЕ")
    else:
        bot.send_message(message.chat.id, "ОТКЛОНЕНО, НУЖЕН СПЕЦИАЛЬНЫЙ ДОСТУП")

@bot.message_handler(commands=["set"])
def set(message, res=False):
    access = False
    for tg_id in special_access:
        if message.chat.id == tg_id:
            access = True
    if access:
        args = message.text.split()
        countcheck = 0
        for mes in args:
            countcheck += 1
        if countcheck-1 >= 5:
            group = False
            for groupcheck in students:
                if args[1] == groupcheck[0]:
                    group = groupcheck

            if not group:
                bot.send_message(message.chat.id,"Такой группы не существует")
            else:
                student = False
                info = False
                for existstudent in group:
                    if existstudent != args[1]:
                        studentinfo = existstudent[0].split()
                        if studentinfo[0] == args[2] and studentinfo[1] == args[3]:
                            student = True
                            info = existstudent
                if not student:
                    bot.send_message(message.chat.id, "Такого студента не существует")
                else:
                    data = args[4]
                    datacheck = str(data).split(".")
                    mtt = False
                    count = 0
                    for dat in datacheck:
                        if len(dat) != 2:
                            mtt = True
                        count += 1
                    if count != 3:
                        mtt = True
                    if mtt:
                        bot.send_message(message.chat.id, "Дата указана неправильно (примеры правильных дат: 01.01.25, 15.10.25, 03.11.25, 10.05.25)")
                    else:
                        type = str(args[5]).lower()
                        if type != "уваж" and type != "неуваж":
                            bot.send_message(message.chat.id, "тип пропуска указан неправильно, нужно либо 'уваж' либо 'неуваж'")
                        else:
                            info.append([data, type])
                            bot.send_message(message.chat.id, "пропуск проставлен")
    else:
        bot.send_message(message.chat.id, "ОТКЛОНЕНО, НУЖЕН СПЕЦИАЛЬНЫЙ ДОСТУП")

@bot.message_handler(commands=["student"])
def student(message, res=False):
    args = message.text.split()
    countcheck = 0
    for mes in args:
        countcheck += 1
    if countcheck-1 == 5:
        group = False
        for groupcheck in students:
            if args[1] == groupcheck[0]:
                group = groupcheck
        if not group:
            bot.send_message(message.chat.id,"Такой группы не существует")
        else:
            student = False
            info = False
            for existstudent in group:
                if existstudent != args[1]:
                    studentinfo = existstudent[0].split()
                    if studentinfo[0] == args[2] and studentinfo[1] == args[3]:
                        student = True
                        info = existstudent
            if not student:
                bot.send_message(message.chat.id, "Такого студента не существует")
            else:
                data1 = args[4]
                datacheck = str(data1).split(".")
                mtt = False
                count = 0
                for dat in datacheck:
                    if len(dat) != 2:
                        mtt = True
                    count += 1
                if count != 3:
                    mtt = True
                if mtt:
                    bot.send_message(message.chat.id, "начало промежутка указано неправильно (примеры правильных начал промежутка: 01.01.25, 15.10.25, 03.11.25, 10.05.25)")
                else:
                    data2 = args[5]
                    datacheck2 = str(data2).split(".")
                    mtt2 = False
                    count2 = 0
                    for dat in datacheck2:
                        if len(dat) != 2:
                            mtt2 = True
                        count2 += 1
                    if count2 != 3:
                        mtt2 = True
                    if mtt2:
                        bot.send_message(message.chat.id, "конец промежутка указан неправильно (примеры правильных концов промежутка: 01.01.25, 15.10.25, 03.11.25, 10.05.25)")
                    else:
                        start_date = datetime(int(datacheck[2]), int(datacheck[1]), int(datacheck[0]))
                        end_date =  datetime(int(datacheck2[2]), int(datacheck2[1]), int(datacheck2[0]))
                        fairskip = 0
                        unfairskip = 0
                        for skip in info:
                            if skip != info[0]: # если информация это не фамилия и имя то
                                datacheck3 = str(skip[0]).split(".")
                                print(datacheck3)
                                date = datetime(int(datacheck3[2]),int(datacheck3[1]),int(datacheck3[0]))
                                if start_date <= date <= end_date:
                                    if skip[1] == "уваж":
                                        fairskip += 1
                                    else:
                                        unfairskip += 1
                        bot.send_message(message.chat.id, f"количество пропусков по уважительной причине: {fairskip}\n"
                                         f"количество пропусков по не уважительной причине: {unfairskip}\n"
                                                          "\n"
                                         f"количество пропусков всего: {fairskip+unfairskip}"
                                         )




bot.polling(none_stop = True, interval = 1)


