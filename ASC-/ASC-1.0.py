from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import InputFile
from aiogram.utils import executor
import dateBase1 as lbr
import sqlite3 as sq
import os
import pandas as pd
import time
import datetime
import asyncio
import aioconsole

Code = "L29"
proxy_url = 'http://proxy.server:3128'

if Code[0] == "T":
    bot = Bot(token="6871609784:AAF5M0toDxiEps8Rs0ibB6kcRaF7IfBLpnI", proxy=proxy_url) # Бот Тесты
elif Code == "L14":
    bot = Bot(token="6321164079:AAFhVkhIPXkc9OmOBb3cgK-P4HoMb3tSpqg", proxy=proxy_url) # Бот 14 Лицей
elif Code == "L29":
    bot = Bot(token="7405779446:AAEZr8G4xvly2U0JU4kyUx-0fjmgFAae1z8", proxy=proxy_url) # Бот 29 Лицей
dp = Dispatcher(bot)

bot.delete_webhook()
if Code[1:] == "14":
    lbr.connect(os.path.realpath('db_14_lyceum_bot.db'))
if Code[1:] == "29":
    lbr.connect(os.path.realpath('db_29_lyceum_bot.db'))


sss = '‼️‼️Внимание‼️‼️'
Develobers = [1, 2]

cnt = 0
cnt_Global = 0



print(lbr.getData(1, "ID", '''AlreadySelected = 1 OR AlreadySelected = "1"'''))
async def log_to_excel(IdList):

    file_path = os.path.realpath('menu.xlsx')
    print(file_path)
    print(IdList)
    data = {
        "Человек": [],
        "Понедельник 1": [],
        "Вторник 1": [],
        "Среда 1": [],
        "Четверг 1": [],
        "Пятница 1": [],
        "Понедельник 2": [],
        "Вторник 2": [],
        "Среда 2": [],
        "Четверг 2": [],
        "Пятница 2": [],
        "Льгота": []
    }
    change = {1:"✓", 0:"X", "-":"    "}
    for Id in IdList:
        data["Человек"].append(f"{lbr.getData(1, 'Klass', Id)[0]}{lbr.getData(1, 'KlassLit', Id)[0]} {lbr.getData(1, 'Name', Id)[0]}")
        data["Понедельник 1"].append(change[lbr.getData(2, '11', Id)[0]])
        data["Вторник 1"].append(change[lbr.getData(2, '12', Id)[0]])
        data["Среда 1"].append(change[lbr.getData(2, '13', Id)[0]])
        data["Четверг 1"].append(change[lbr.getData(2, '14', Id)[0]])
        data["Пятница 1"].append(change[lbr.getData(2, '15', Id)[0]])
        data["Понедельник 2"].append(change[lbr.getData(2, '21', Id)[0]])
        data["Вторник 2"].append(change[lbr.getData(2, '22', Id)[0]])
        data["Среда 2"].append(change[lbr.getData(2, '23', Id)[0]])
        data["Четверг 2"].append(change[lbr.getData(2, '24', Id)[0]])
        data["Пятница 2"].append(change[lbr.getData(2, '25', Id)[0]])
        data["Льгота"].append(change[lbr.getData(2, 'free', Id)[0]])
    print(data)

    df = pd.DataFrame(data)

    with pd.ExcelWriter(file_path, mode="a", engine="openpyxl",if_sheet_exists="overlay",) as writer:
        df = df.sort_values('Человек')
        df.style.set_properties(**{'border': '1.3px solid black', 'color': 'black'}).to_excel(writer, sheet_name="Столовая",index=False)
        print(IdList, "->", file_path)

    return file_path

class UserClass:
    def __init__(self, ID, ChatID = -100):
        if ChatID != -100:
            self.ChatID = ChatID
            self.ID = lbr.getUserId(self.ChatID)
        else:
            self.ID = ID
            self.ChatID =lbr.getData(1, "ChatID", self.ID)[0]
        if self.ID != -1:
            self.Name = lbr.getData(1, "Name", self.ID)[0]
            self.AlreadySelected = lbr.getData(1, "AlreadySelected", self.ID)[0]
            self.Admin = lbr.getData(1, "Admin", self.ID)[0]
            self.Klass = lbr.getData(1, "Klass", self.ID)[0]
            self.KlassLit = lbr.getData(1, "KlassLit", self.ID)[0]
            self.AlreadyRegistraate = lbr.getData(1, "AlreadyRegistraate", self.ID)[0]
            self.Mode = lbr.getData(1, "Mode", self.ID)[0]
            self.Inf = lbr.getData(1, "Inf", self.ID)[0]
        else:
            self.Name = "F"
            self.AlreadySelected = -1
            self.Admin = -1
            self.Klass = -1
            self.KlassLit = "F"
            self.AlreadyRegistraate = -1
            self.Mode = -1
            self.Inf = -1
    async def update(self):
        self.ID = lbr.getUserId(self.ChatID)
        if self.ID != -1:
            self.Name = lbr.getData(1, "Name", self.ID)[0]
            self.AlreadySelected = lbr.getData(1, "AlreadySelected", self.ID)[0]
            self.Admin = lbr.getData(1, "Admin", self.ID)[0]
            self.Klass = lbr.getData(1, "Klass", self.ID)[0]
            self.KlassLit = lbr.getData(1, "KlassLit", self.ID)[0]
            self.AlreadyRegistraate = lbr.getData(1, "AlreadyRegistraate", self.ID)[0]
            self.Mode = lbr.getData(1, "Mode", self.ID)[0]
            self.Inf = lbr.getData(1, "Inf", self.ID)[0]
    async def print_(self):
        print("Information for user: ChatID -", self.ChatID)
        if self.ID != -1:
            print("ID -", self.ID)
            print("Name -", self.Name)
            print("Klass -", self.Klass, self.KlassLit)
            print("Admin -", self.Admin)
            print("Mode -", self.Mode)
            print("Inf -", self.Inf)
            print("AlreadySelected -", self.AlreadySelected)
            print("AlreadyRegistraate -", self.AlreadyRegistraate)
        else:
            print("User not registered")
admins = []
adminsChatID = []

@dp.message_handler(commands=["ping"])
async def pingLoad(message):
    await bot.send_message(message.chat.id, "PING")
    global cnt_Global
    cnt_Global += 1


@dp.message_handler(content_types = ['text'])
async def textLoad(message, stop = False):
    if stop:
        raise RuntimeError("Fall by command")
    try:
        global admins
        global cnt_Global
        global adminsChatID
        User = UserClass(ChatID=message.chat.id, ID=0)
        User.print_()

        if User.ID in Develobers:
            if User.Mode == -2:
                lbr.writeData(1, "Mode", 0, User.ID)
                User.update()
            if User.Admin == 0:
                lbr.writeData(1, "Admin", 1, User.ID)
                User.update()
        text = message.text
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",User.ID, User.Name, ":", text)
        admins = lbr.getData(1, "ID", "`Admin` = 1")
        adminsChatID = lbr.getData(1, "ChatID", "`Admin` = 1")
        if message.chat.type == 'private':
            if text == "/stop" and User.ID != -1 and User.Mode != -2:
                await bot.send_message(User.ChatID, "Ок")
                lbr.writeData(1, "Mode", 0, User.ID)
                User.update()
            # Новый юзер
            if text == "/start":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Изменить данные о себе")
                item2 = types.KeyboardButton("Выбрать варианты")
                markup.add(item1, item2)
                await bot.send_message(User.ChatID, f"👋Привет👋, я бот - столовая, созданный группой 'it-cub' \nhttps://t.me/ITcubeDevelopers\nВсе команды /help ", reply_markup=markup)
                lbr.writeData(1, "Username", message.from_user.username, User.ID)


            if User.ID == -1:
                User.print_()
                lbr.writeData(1, 'ChatID', User.ChatID)
                User.update()
                User.print_()
                await bot.send_message(User.ChatID, f"Для продолжения пройди регистрацию.")

            # Бан
            elif (User.Mode == -2):
                await bot.send_message(User.ChatID,  "Моли у админов прощения!")
            # Стандарт
            elif (User.Mode == 0):
                lbr.writeData(1, "Username", message.from_user.username, User.ID)
                if User.AlreadyRegistraate == 1 and text != "/set" and text != "Изменить данные о себе":
                    lbr.writeData(1, "Username", message.from_user.username, User.ID)
                    if text == '/help':
                        help = "/set - изменить данные о себе" \
                            "\n/select - выбрать варианты" \
                            "\n/help - и так понятно"
                        if User.Admin:
                            help = "Обычный пользователь:\n" + help + "\nАдмин:" \
                                                                    "\n/reMenu - обновить конкретный вариант" \
                                                                    "\n/reMenuAll - обновить все меню" \
                                                                    "\n/ivent - отправить сообщение" \
                                                                    "\n/exel - exel таблица"\
                                                                    "\n/ban - БАН!!!"\
                                                                    "\n/unban - разбан"\
                                                                    "\n/write - писать в бд"\
                                                                    "\n/reed - читать из бд"\
                                                                    "\n/banList - список забаненых"\
                                                                    "\n/pingGo - вкл/выкл постоянный ping"\
                                                                    "\n/stat - статистика"

                        await bot.send_message(User.ChatID, help)
                    elif User.AlreadySelected == 0 or text == "/select" or text == "Выбрать варианты":
                        lbr.writeData(1, "Username", message.from_user.username, User.ID)
                        if User.AlreadySelected == 0:
                            await bot.send_message(User.ChatID, 'Вы не выбрали меню, предлагаю сделать это сейчас')
                        lbr.writeData(1, "Mode", 3, User.ID)
                        User.update()
                        await textLoad(message)
                    elif User.Admin:
                        if text == "/ivent":
                            lbr.writeData(1, "Mode", 4, User.ID)
                            lbr.writeData(1, "Inf", "1|-1|F", User.ID)
                            await bot.send_message(User.ChatID, "Ок, напишите ID получателя или -1 если требуется отправить всем")
                        elif text == "/reMenu":
                            lbr.writeData(1, "Mode", 5, User.ID)
                            lbr.writeData(1, "Inf", "1|-1|F", User.ID)
                            await bot.send_message(User.ChatID, "Ок, напишите вариант для изменения (WDV)")
                        elif text == "/reMenuAll":
                            lbr.writeData(1, "Mode", 6, User.ID)
                            lbr.writeData(1, "Inf", "0|", User.ID)
                            await bot.send_message(User.ChatID, "Ок, напишите вариант на 111 (WDV)")
                        elif text == "/exel":
                            print("exel")
                            filepath = await log_to_excel(lbr.getData(1, "ID", '''AlreadySelected = 1 OR AlreadySelected = "1"'''))
                            with open(filepath, 'rb') as f1:
                                await bot.send_document(message.chat.id, f1)
                        elif text == "/ban":
                            IDList = lbr.getData(1, "ID")
                            sps = 'Выберете пользователя для бана (напишите его номер/ID):'
                            for id in IDList:
                                SelectUser = UserClass(ID=id)
                                sps = sps + f'''\n{id} - {"!АДМИН!" if SelectUser.Admin else ""} {SelectUser.Name} {SelectUser.Klass}{SelectUser.KlassLit} '''
                            await bot.send_message(User.ChatID, sps)
                            lbr.writeData(1, "Mode", 7, User.ID)
                            lbr.writeData(1, "Inf", "1|-1|-1", User.ID)
                        elif text == "/unban":
                            IDList = lbr.getData(1, "ID", "`Mode` = -2")
                            sps = 'Выберете пользователя для разбана (напишите его номер/ID):'
                            for id in IDList:
                                SelectUser = UserClass(ID=id)
                                sps = sps + f'''\n{id} - {"!АДМИН!" if SelectUser.Admin else ""} {SelectUser.Name} {SelectUser.Klass}{SelectUser.KlassLit} '''
                            await bot.send_message(User.ChatID, sps)
                            lbr.writeData(1, "Mode", 8, User.ID)
                            lbr.writeData(1, "Inf", "1|-1|-1", User.ID)
                        elif text == "/banList":
                            IDList = lbr.getData(1, "ID", "`Mode` = -2")
                            sps = 'Список забаненых:'
                            if IDList != []:
                                for id in IDList:
                                    SelectUser = UserClass(ID=id)
                                    sps = sps + f'''\n{id} - {"!АДМИН!" if SelectUser.Admin else ""} {SelectUser.Name} {SelectUser.Klass}{SelectUser.KlassLit} '''
                            else:
                                sps = sps + "\nТаких нет"
                            await bot.send_message(User.ChatID, sps)
                        elif text == "/write":
                            lbr.writeData(1, "Mode", 9, User.ID)
                            lbr.writeData(1, "Inf", "1|-1|F|F|F", User.ID)
                            await bot.send_message(User.ChatID, "Выберете базу данных: \n1 - Users\n2 - Select\n3 - Data")
                        elif text == "/reed":
                            lbr.writeData(1, "Mode", 10, User.ID)
                            lbr.writeData(1, "Inf", "1|-1", User.ID)
                            await bot.send_message(User.ChatID, "Выберете базу данных: \n1 - Users\n2 - Select\n3 - Data")
                        elif text == "/pingGo":
                            if lbr.getData(3, "Value", '''ID = "PID"''') != []:
                                pingsID = str(lbr.getData(3, "Value", '''ID = "PID"''')[0]).split("|")
                            else:
                                pingsID = []
                            if str(User.ID) in pingsID:
                                pingsID.remove(str(User.ID))
                                await bot.send_message(User.ChatID, "Режим пинга 🔕выключен🔕")
                            else:
                                if pingsID != [""]:
                                    pingsID.append(str(User.ID))
                                else:
                                    pingsID = [str(User.ID)]
                                await bot.send_message(User.ChatID, "Режим пинга 🔔включен🔔")
                            print(pingsID)
                            lbr.writeData(3, "Value", '|'.join(pingsID), '''ID = "PID"''')
                        elif text == "/stat":
                            timeProg = int(time.time() - start_time)/60
                            await bot.send_message(User.ChatID, f"Стабильная работа, обработано {cnt_Global} запросов."
                                      f"\nВремя со старта:"
                                      f"\n{int(timeProg//60//24)} сут."
                                      f"\n{int(timeProg//60%24)} часов."
                                      f"\n{float(timeProg%60):2.2} минут.")

                else:
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    keyboard.add(
                        InlineKeyboardButton(text="Изменить Имя", callback_data=f'{User.ID} change Name'),
                        InlineKeyboardButton(text="Изменить Класс", callback_data=f'{User.ID} change Klass')
                    )
                    if User.Name != "F" and User.Klass != -1:
                        keyboard = InlineKeyboardMarkup(row_width=2)
                        keyboard.add(
                        InlineKeyboardButton(text="Изменить Имя", callback_data=f'{User.ID} change Name'),
                        InlineKeyboardButton(text="Изменить Класс", callback_data=f'{User.ID} change Klass'),
                        InlineKeyboardButton(text="Применить изменения/завершить регистрацию", callback_data=f'{User.ID} change end')
                        )
                        await bot.send_message(User.ChatID, f"Текущие данные:"
                                                f"\nИмя - {User.Name if User.Name != 'F' else 'Не указанно'}"
                                                f"\nКласс - {f'{User.Klass}{User.KlassLit}' if User.Klass != -1 else 'Не указанно'}",
                                    reply_markup=keyboard)
                    else:
                        await bot.send_message(User.ChatID, f"Текущие данные:"
                                                f"\nИмя - {User.Name if User.Name != 'F' else 'Не указанно'}"
                                                f"\nКласс - {f'{User.Klass}{User.KlassLit}' if User.Klass != -1 else 'Не указанно'}",
                                    reply_markup=keyboard)
            elif (User.Mode == 1):
                if len(text.split()) == 2:
                    lbr.writeData(1, "Name", text, User.ID)
                    User.update()
                    await bot.send_message(User.ChatID, "ОК")
                    lbr.writeData(1, "Mode", 0, User.ID)
                    await textLoad(message)
                else:
                    await bot.send_message(User.ChatID, "Ошибка предствавления")
            elif (User.Mode == 2):
                if len(text) == 2:
                    if text[0].isdigit() and text[1] in "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЭЮЯ":
                        lbr.writeData(1, "Klass", text[0], User.ID)
                        lbr.writeData(1, "KlassLit", text[1], User.ID)
                        User.update()

                        lbr.writeData(1, "Mode", 0, User.ID)
                        await bot.send_message(User.ChatID, "ОК")
                        await textLoad(message)
                    else:
                        await bot.send_message(User.ChatID, "Ошибка предствавления")
                else:
                    await bot.send_message(User.ChatID, "Ошибка предствавления")
            elif (User.Mode == 3):
                    if User.AlreadySelected == 0:
                        keyboard = InlineKeyboardMarkup(row_width=1)
                        keyboard.add(
                        InlineKeyboardButton(text="Я бесплатник", callback_data=f'{User.ID} select free 1'),
                        InlineKeyboardButton(text="Я платник", callback_data=f'{User.ID} select free 0'))
                        await bot.send_message(User.ChatID, f'Веберете:', reply_markup=keyboard)

                    else:
                        day = 1
                        week = 1
                        # Функция для получения текущего дня недели и номера недели
                        # Получаем текущую дату
                        today = datetime.datetime.now().date()
                        # \Определяем, когда начинается 1 сентября текущего года
                        start_date = datetime.date(today.year, 9, 1)
                        # Вычисляем номер недели, начиная с 1 сентября
                        week_num = (today - start_date).days // 7 + 1
                        # Определяем день недели
                        day_num = today.weekday() + 1
                        # Определяем, какой это день недели
                        if week_num % 2 == 1:
                            if day_num == 1:
                                print("Понедельник 1-й недели")
                                day = 1
                                week = 1
                            elif day_num == 2:
                                print("Вторник 1-й недели")
                                day = 2
                                week = 1
                            elif day_num == 3:
                                print("Среда 1-й недели")
                                day = 3
                                week = 1
                            elif day_num == 4:
                                print("Четверг 1-й недели")
                                day = 4
                                week = 1
                            elif day_num == 5:
                                print("Пятница 1-й недели")
                                day = 5
                                week = 1
                            elif day_num == 6:
                                print("Суббота 1-й недели")
                                day = 1
                                week = 2
                            elif day_num == 7:
                                print("Воскресенье 1-й недели")
                                day = 1
                                week = 2
                        else:
                            if day_num == 1:
                                print("Понедельник 2-й недели")
                                day = 1
                                week = 2
                            elif day_num == 2:
                                print("Вторник 2-й недели")
                                day = 2
                                week = 2
                            elif day_num == 3:
                                print("Среда 2-й недели")
                                day = 3
                                week = 2
                            elif day_num == 4:
                                print("Четверг 2-й недели")
                                day = 4
                                week = 2
                            elif day_num == 5:
                                print("Пятница 2-й недели")
                                day = 5
                                week = 2
                            elif day_num == 6:
                                print("Суббота 2-й недели")
                                day = 1
                                week = 1
                            elif day_num == 7:
                                print("Воскресенье 2-й недели")
                                day = 1
                                week = 1

                            if day == 0:
                                day = 1
                        keyboard = InlineKeyboardMarkup(row_width = 3)
                        lbr.writeData(1, "Username", message.from_user.username, User.ID)
                        keyboard.add(
                        InlineKeyboardButton(text="суп",callback_data=f'{User.ID} select {week}{day} 1'),
                        InlineKeyboardButton(text="без супа",callback_data=f'{User.ID} select {week}{day} 0'),
                        InlineKeyboardButton(text="Не обедаю", callback_data=f'{User.ID} select {week}{day} -'),
                                            InlineKeyboardButton(text="Назад", callback_data=f'{User.ID} select {week}{day} nazad'))

                        await bot.send_message(User.ChatID, f'Веберете вариант {week} нед. {day} день:'
                                                    f'\nСУП - {lbr.getData(3, "Value", week*100 + day*10 + 1)[0]}'
                                                    f'\nБЛЮДО - {lbr.getData(3, "Value", week*100 + day*10 + 2)[0]}', reply_markup=keyboard)
                        days = 6
            elif (User.Mode == 4):
                inf = str(User.Inf).split("|")
                stad = inf[0]
                data = inf[1:]
                if stad == "1":
                    data[0] = text
                    if data[1] == "F":
                        lbr.writeData(1, "Inf", f"2|{'|'.join(data)}", User.ID)
                        await bot.send_message(User.ChatID, "ОК, теперь текст сообщения")
                    else:
                        lbr.writeData(1, "Inf", f'''3|{'|'.join(data)}''', User.ID)
                elif stad == "2":
                    data[1] = text
                    lbr.writeData(1, "Inf", f'''3|{'|'.join(data)}''', User.ID)
                User.update()
                inf = str(User.Inf).split("|")
                stad = inf[0]
                data = inf[1:]
                if stad == "3":
                    if data[0] == "-1":
                        Send_to = lbr.getData(1, "ChatID")
                    else:
                        Send_to = lbr.getData(1, "ChatID", data[0])
                    print(Send_to)
                    if Send_to != []:
                        lbr.writeData(1, "Inf", -1, User.ID)
                        lbr.writeData(1, "Mode", 0, User.ID)
                        for Chat in Send_to:
                            await bot.send_message(Chat, f'''Сообщение от администратора:\n{data[1]}''')
                    else:
                        await bot.send_message(User.ChatID, "Получателя не существует(\nИзмение критерий")
                        lbr.writeData(1, "Inf", f'''1|{'|'.join(data)}''', User.ID)
            elif (User.Mode == 5):
                data = str(User.Inf).split("|")
                print(data)
                if int(data[0]) == 1:
                    data[1] = text
                    if data[2] == "F":
                        await bot.send_message(User.ChatID, "Ок, напишите новый вариант (блюдо/суп)")
                        data[0] = '2'
                        lbr.writeData(1, "Inf", '|'.join(data), User.ID)
                    else:
                        lbr.writeData(1, "Inf", '|'.join(data), User.ID)
                        User.update()
                elif int(data[0]) == 2:
                    data[2] = text
                    data[0] = '3'
                    lbr.writeData(1, "Inf", '|'.join(data), User.ID)
                    User.update()
                data = str(User.Inf).split("|")
                if int(data[0]) == 3:
                    lbr.writeData(3, "Value", data[2], data[1])
                    await bot.send_message(User.ChatID, "Успешное изменение")
                    lbr.writeData(1, "Mode", 0, User.ID)
                    lbr.writeData(1, "Inf", -1, User.ID)
            elif (User.Mode == 6):
                if Code[1:] == "14":
                    vars, days = 3, 5
                elif Code[1:] == "29":
                    vars, days = 2, 6
                data = str(User.Inf).split("|")
                dayCnt = int(data[0]) // vars
                day = dayCnt % days + 1
                weak = dayCnt // days + 1
                var = (int(data[0]) % vars) + 1
                print(data[0], "->", dayCnt, var)
                print(f"{weak}{day}{var} <-", text)
                lbr.writeData(3, "Value", text, f"{weak}{day}{var}")
                data[0] = str(int(data[0]) + 1)
                dayCnt = int(data[0]) // vars
                day = dayCnt % days + 1
                weak = dayCnt // days + 1
                var = (int(data[0]) % vars) + 1

                lbr.writeData(1, "Inf", "|".join(data), User.ID)
                if weak == 3:
                    await bot.send_message(User.ChatID, f"Ок, обновление заeвершено")
                    lbr.writeData(1, "Mode", 0, User.ID)
                    lbr.writeData(1, "Inf", "-1", User.ID)
                else:
                    await bot.send_message(User.ChatID, f"Ок, напишите вариант на {weak}{day}{var} (WDV)")
            elif (User.Mode == 7):
                data = str(User.Inf).split("|")

                if lbr.getData(1, "ID", text) != []:
                    data[1] = text
                    data[0] = str(2)
                    print( "|".join(data), "->", "Inf", User.ID)
                    lbr.writeData(1, "Inf", "|".join(data), User.ID)
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    keyboard.add(
                    InlineKeyboardButton(text="ананимно",callback_data=f'{User.ID} ban 1 1'),
                    InlineKeyboardButton(text="не ананимно",callback_data=f'{User.ID} ban 0 1'))
                    await bot.send_message(User.ChatID, 'Как забанить?', reply_markup=keyboard)
                else:
                    await bot.send_message(User.ChatID, 'ID неверен')
            elif (User.Mode == 8):
                data = str(User.Inf).split("|")
                if lbr.getData(1, "ID", text) != []:
                    data[1] = text
                    data[0] = str(2)
                    print(data)
                    lbr.writeData(1, "Inf", "|".join(data), User.ID)
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    keyboard.add(
                    InlineKeyboardButton(text="ананимно",callback_data=f'{User.ID} ban 1 0'),
                    InlineKeyboardButton(text="не ананимно",callback_data=f'{User.ID} ban 0 0'))
                    await bot.send_message(User.ChatID, 'Как разбанить??', reply_markup=keyboard)
            elif (User.Mode == 9):
                data = str(User.Inf).split("|")
                if data[0] == "1":
                    if text in ["1", "2", "3"]:
                        data[1] = text
                        data[0] = "2"
                        sps = []
                        tabs = lbr.getTabls(int(text))
                        for i in range(len(tabs)):
                            sps.append(f"{i} - {tabs[i][0]}")
                        await bot.send_message(User.ChatID, "Напишите номер столбец для записи\n" + "\n".join(sps))
                    else:
                        await bot.send_message(User.ChatID, "Ошибка представления")
                elif data[0] == "2":
                    if text.isdigit():
                        sps = []
                        tabs = lbr.getTabls(int(data[1]))
                        for i in range(len(tabs)):
                            sps.append(str(tabs[i][0]))
                        print(text, int(text), len(sps), int(text) < len(sps))
                        if int(text) >= 0 and int(text) < len(sps):
                            data[2] = sps[int(text)]
                            data[0] = "3"
                            await bot.send_message(User.ChatID, "Напишите данные для записи")
                        else:
                            await bot.send_message(User.ChatID, "Ошибка представления")
                    else:
                        await bot.send_message(User.ChatID, "Ошибка представления")
                elif data[0] == "3":
                    data[3] = text
                    data[0] = "4"
                    spsB = lbr.getAll(int(data[1]))
                    print(spsB)
                    sps = ["ID - <значения>"]
                    for i in spsB:
                        i = list(map(str, i))
                        x = "|".join(i[1:])
                        sps.append(f"{i[0]} - {x}")
                    s = "\n".join(sps)
                    await bot.send_message(User.ChatID, f'''Напишите условие для записи: \nTrue - запись без условия, \nчисло - ID для записи, \nстрока - условие (SQ3)\n {s}''')
                elif data[0] == "4":
                    if text.isdigit():
                        data[4] = text
                    elif text == "True":
                        data[4] = "1 = 1"
                    else:
                        data[4] = text
                    data[0] = "5"
                if data[0] == "5":
                    lbr.writeData(1, "Mode", 0, User.ID)
                    lbr.writeData(1, "Inf", "-1", User.ID)
                    try:
                        lbr.writeData(int(data[1]), data[2], data[3], data[4])

                        await bot.send_message(User.ChatID, '''✅Успешно✅''')
                    except Exception as e:
                        await bot.send_message(User.ChatID, f'''❌Ошибка❌\n{e}''')
                lbr.writeData(1, "Inf", "|".join(data), User.ID)
            elif (User.Mode == 10):
                dataFuc = str(User.Inf).split("|")
                print(dataFuc)
                if dataFuc[0] == "1":
                    if text in ["1", "2", "3"]:
                        print(text, "-> dataFuc[1]")
                        dataFuc[1] = text
                        dataFuc[0] = "2"
                        sps = []
                    else:
                        await bot.send_message(User.ChatID, "Ошибка представления")
                if dataFuc[0] == "2":
                    file_path = os.path.realpath('data.xlsx')
                    tabB = lbr.getTabls(int(dataFuc[1]))
                    tab = []
                    data = dict()
                    for i in tabB:
                        tab.append(i[0])
                    dataB = lbr.getAll(int(dataFuc[1]))
                    print(dataB)
                    print(tab)
                    for iT in range(len(tab)):
                        data[tab[iT]] = []
                        for iD in range(len(dataB)):
                            print(f"data[{tab[iT]}] = {str(dataB[iD][iT])}")
                            data[tab[iT]].append(str(dataB[iD][iT]))
                    print(*data, sep="\n")
                    df = pd.DataFrame(data)
                    with pd.ExcelWriter(file_path, mode="a", engine="openpyxl",if_sheet_exists="replace",) as writer:
                        df.style.set_properties(**{'border': '1.3px solid black', 'color': 'black'}).to_excel(writer, sheet_name="Data",index=False)
                        print(data, "->", file_path)
                    with open(file_path, 'rb') as f1:
                        await bot.send_document(User.ChatID, f1)
                    lbr.writeData(1, "Mode", 0, User.ID)
        print(cnt_Global)
        cnt_Global += 1
    except Exception as e:
    #finally: #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
        if e is None:
            pass
        else:
            print(e)

            for i in adminsChatID:
                await bot.send_message(i, f"{sss}.\nОбработано {cnt_Global} запросов /ping\nОшибка:\n{e}")



@dp.callback_query_handler(lambda c: True)
async def process_callback_query(call: types.CallbackQuery):
    try:
        global admins
        global adminsChatID
        message = call.message
        input = call.data.split()

        User = UserClass(int(input[0]))
        print(User.ID, User.Name, ":", input)
        if input[1] == "change":
            if input[2] == "Name":
                await  bot.edit_message_text('Напишите ФИ в формате "Иванов Иван"', chat_id=User.ChatID, message_id=message.message_id)
                lbr.writeData(1, "Mode", 1, User.ID)
            elif input[2] == "Klass":
                await  bot.edit_message_text('Напишите класс в формате "7Б" (литера класса - заглавная, русская буква)', chat_id=User.ChatID, message_id=message.message_id)
                lbr.writeData(1, "Mode", 2, User.ID)
            elif input[2] == "end":
                lbr.writeData(1, "AlreadyRegistraate", 1, User.ID)
                lbr.writeData(1, "Mode", 0, User.ID)
                await textLoad(message)
                await bot.edit_message_text('ОК', chat_id=User.ChatID, message_id=message.message_id)

        elif input[1] == "select":

            if Code[1:] == "14":
                days = 6
            elif Code[1:] == "29":
                days = 6


            await  bot.edit_message_text('ОК', chat_id=User.ChatID, message_id=message.message_id)
            if input[2] == "free":
                lbr.writeData(2, "ID", User.ID, User.ID)
            lbr.writeData(2, input[2], input[3], User.ID)
            if input[2] == "free":

                day = 1
                week = 1
                if User.AlreadySelected == 1 and Code[1:] == "29":
                    # Функция для получения текущего дня недели и номера недели
                    # Получаем текущую дату
                    today = datetime.datetime.now().date()
                    # \Определяем, когда начинается 1 сентября текущего года
                    start_date = datetime.date(today.year, 9, 1)
                    # Вычисляем номер недели, начиная с 1 сентября
                    week_num = (today - start_date).days // 7 + 1
                    # Определяем день недели
                    day_num = today.weekday() + 1
                    # Определяем, какой это день недели
                    if week_num % 2 == 1:
                        if day_num == 1:
                            print("Понедельник 1-й недели")
                            day = 1
                            week = 1
                        elif day_num == 2:
                            print("Вторник 1-й недели")
                            day = 2
                            week = 1
                        elif day_num == 3:
                            print("Среда 1-й недели")
                            day = 3
                            week = 1
                        elif day_num == 4:
                            print("Четверг 1-й недели")
                            day = 4
                            week = 1
                        elif day_num == 5:
                            print("Пятница 1-й недели")
                            day = 5
                            week = 1
                        elif day_num == 6:
                            print("Суббота 1-й недели")
                            day = 1
                            week = 2
                        elif day_num == 7:
                            print("Воскресенье 1-й недели")
                            day = 1
                            week = 2
                    else:
                        if day_num == 1:
                            print("Понедельник 2-й недели")
                            day = 1
                            week = 2
                        elif day_num == 2:
                            print("Вторник 2-й недели")
                            day = 2
                            week = 2
                        elif day_num == 3:
                            print("Среда 2-й недели")
                            day = 3
                            week = 2
                        elif day_num == 4:
                            print("Четверг 2-й недели")
                            day = 4
                            week = 2
                        elif day_num == 5:
                            print("Пятница 2-й недели")
                            day = 5
                            week = 2
                        elif day_num == 6:
                            print("Суббота 2-й недели")
                            day = 1
                            week = 1
                        elif day_num == 7:
                            print("Воскресенье 2-й недели")
                            day = 1
                            week = 1


            else:
                week = int(input[2][0])
                day = int(input[2][1])
                if input[3] == "nazad":
                    day -= 1
                    if day == 0 and week == 2:
                        week = 1
                        day = 5
                    if day == 0 and week == 1:
                        week = 1
                        day = 1
                    if week == 1 and day == 0:
                        week = 2
                        day = 1
                else:
                    day += 1
                    if day == 6 and week == 1:
                        day = 1
                        week = 2

                week += day // days
                day %= days

                print(week, day)
                admins = lbr.getData(1, "ChatID", "`Admin` = 1")
                for i in range(len(admins)):
                    await bot.send_message(admins[i], f"+1")

            if week == 3 and day == 0:
                await bot.send_message(User.ChatID, 'Вы завершили выбор вариантов')
                lbr.writeData(1, "AlreadySelected", 1, User.ID)
                lbr.writeData(1, "Mode", 0, User.ID)
                admins = lbr.getData(1, "ChatID", "`Admin` = 1")
                for i in range(len(admins)):
                    await bot.send_message(admins[i], f"👋Привет👋, ещё один человек выбрал варианты, печатай новую таблицу /exel")


            else:
                if Code[1:] == "14":
                    keyboard = InlineKeyboardMarkup(row_width = 4)
                    keyboard.add(
                    InlineKeyboardButton(text="1 + суп",
                                                                callback_data=f'{User.ID} select {week}{day} 101'),
                    InlineKeyboardButton(text="1 - суп",
                                                                callback_data=f'{User.ID} select {week}{day} 91'),
                    InlineKeyboardButton(text="2 + суп",
                                                                callback_data=f'{User.ID} select {week}{day} 102'),
                    InlineKeyboardButton(text="2 - суп",
                                                                callback_data=f'{User.ID} select {week}{day} 92'))

                    await bot.send_message(User.ChatID, f'Веберете вариант {week} нед. {day} день:'
                                                f'\nСУП - {lbr.getData(3, "Value", week*100 + day*10 + 3)[0]}'
                                                f'\nПЕРВОЕ - {lbr.getData(3, "Value", week*100 + day*10 + 1)[0]}'
                                                f'\nВТОРОЕ - {lbr.getData(3, "Value", week*100 + day*10 + 2)[0]}'
                                    , reply_markup=keyboard)
                elif Code[1:] == "29":
                    keyboard = InlineKeyboardMarkup(row_width = 3)
                    keyboard.add(
                    InlineKeyboardButton(text="суп",callback_data=f'{User.ID} select {week}{day} 1'),
                    InlineKeyboardButton(text="без супа",callback_data=f'{User.ID} select {week}{day} 0'),
                    InlineKeyboardButton(text="Не обедаю", callback_data=f'{User.ID} select {week}{day} -'),
                    InlineKeyboardButton(text="Назад", callback_data=f'{User.ID} select {week}{day} nazad'))
                    await bot.send_message(User.ChatID, f'Веберете вариант {week} нед. {day} день:'
                                                f'\nСУП - {lbr.getData(3, "Value", week*100 + day*10 + 1)[0]}'
                                                f'\nБЛЮДО - {lbr.getData(3, "Value", week*100 + day*10 + 2)[0]}', reply_markup=keyboard)
                    days = 6
                    await bot.edit_message_text('ОК',chat_id=User.ChatID, message_id=message.message_id)


        elif input[1] == "unban":
            if User.Mode == -2:
                lbr.writeData(1, "Mode", -2, User.ID)
                await bot.send_message(BanUser.ChatID, "Ты разбанен")
                for i in range(len(admins)):
                   await  bot.edit_message_text(f'''Пользователь {User.ID} {User.Name} {User.Klass}{User.KlassLit} - разбанен''', chat_id=User.ChatID, message_id=message.message_id)
            else:
               await  bot.edit_message_text(f'''Пользователь уже разбанен''', chat_id=User.ChatID, message_id=message.message_id)
            lbr.writeData(1, "Mode", 0, User.ID)
        elif input[1] == "ban":
            data = str(User.Inf).split("|")

            data[2] = bool(int(input[2]))
            print(data)
            BanUser = UserClass(int(data[1]))
            if input[3] == '1':
                lbr.writeData(1, "Mode", -2, BanUser.ID)
                await bot.send_message(BanUser.ChatID, f'''Ты забанен администратором {"" if data[2] else str(User.Name)}''')
                await  bot.edit_message_text(f'Пользователь успешно СЛОВИЛ БАН !!!', chat_id=User.ChatID, message_id=message.message_id)
            else:
                lbr.writeData(1, "Mode", 0, BanUser.ID)
                await bot.send_message(BanUser.ChatID, f'''Ты разбанен администратором {"" if data[2] else str(User.Name)}''')
                await  bot.edit_message_text(f'Пользователь успешно разбанен', chat_id=User.ChatID, message_id=message.message_id)
            lbr.writeData(1, "Mode", 0, User.ID)
        global cnt_Global
        cnt_Global += 1
    except Exception as e:
        if e is None:
            pass
        else:
            print(e)
            await bot.send_message(User.ID, "Произошла ошибка, повторите попытку")
            for i in adminsChatID:
                await bot.send_message(i, f"{sss}. \nОбработано {cnt_Global} сообщений\nОшибка:\n{e}")

stop = False

async def PollingLoaderFunc():
    await dp.start_polling()

async def ConsolLoaderFunc():
    while True:
        await Consol()

async def PINGLoaderFunc():
    await asyncio.sleep(2)
    while True:
        await PING()
        await asyncio.sleep(60 * 10)

async def PING():
    print("PING")
    timeProg = int(time.time() - start_time) // 60
    IDList = str(lbr.getData(3, "Value", '''ID = "PID"''')[0]).split("|")
    ChatIdList = []
    if IDList != [""]:
        for i in IDList:
            ChatIdList.append(lbr.getData(1, "ChatID", str(i))[0])
        for i in ChatIdList:
            print("Send information to", i)
            await bot.send_message(i, f"Стабильная работа, обработано {cnt_Global} запросов."
                                       f"\nВремя со старта:"
                                       f"\n{int(timeProg // 60 // 24)} сут."
                                       f"\n{int(timeProg // 60 % 24)} часов."
                                       f"\n{int(timeProg % 60)} минут.")
    else:
        print("Send information to noone")

async def Consol():
    inp = await aioconsole.ainput()
    if inp == "fall":
        admins = lbr.getData(1, "ChatID", "`Admin` = 1")
        timeProg = int(time.time() - start_time) // 60
        for i in admins:
            await bot.send_message(i, f"{sss}. \nЯ выключаюсь от консоли. \nОбработано {cnt_Global} запросов."
                                      f"\nВремя со старта:"
                                      f"\n{int(timeProg // 60 // 24)} сут."
                                      f"\n{int(timeProg // 60 % 24)} часов."
                                      f"\n{int(timeProg % 60)} минут.")
        await stopFunc()
    else:
        print("Команда не распознана(")

async def startFunc():
    global stop
    global start_time
    start_time = time.time()
    print("Start 'Polling'")
    polling_task = asyncio.create_task(PollingLoaderFunc())
    print("Start 'Polling' -> success")
    print("Start 'ConsolLoader'")
    consol_task = asyncio.create_task(ConsolLoaderFunc())
    print("Start 'ConsolLoader' -> success")
    print("Start 'PING'")
    ping_task = asyncio.create_task(PINGLoaderFunc())
    print("Start 'PING' -> success")
    print("All start without problems")
    admins = lbr.getData(1, "ChatID", "`Admin` = 1")
    for i in range(len(admins)):
        await bot.send_message(admins[i], f"{sss}. \nЯ запустился\n/ping")
    print("'fall' to stop ALL")
    print("Он пишет все на английском, потому что прикольно, типо хацкеры")
    while not stop:
        await asyncio.sleep(1)
    exit(0)

async def stopFunc():
    print("STOP")
    global stop
    stop = True
    await dp.stop_polling()
    await bot.close()

if __name__ == '__main__':
    asyncio.run(startFunc())


