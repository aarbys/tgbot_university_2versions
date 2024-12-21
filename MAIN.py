import telebot
from telebot import types
from pprint import pprint
from time import sleep

token = "6301426760:AAHMY4pFHJD0RcalBXcDNqI-6p_-CNMPlqs"

bot = telebot.TeleBot(token)

# прикол с 30-ой фоткой


door_password = str(31415)
zagadka_1 = "каменный"
zagadka_2 = "корова"
zagadka_3 = "стекло"

correct_doors = ["=", "-", "^", "-", "*", "^"]
helps_doors = ["-", "*", "*", "=", "=", "*"]
# + * - ^
admin = "568037949"
admins = [admin]
correct_doors_text = [
    "Удивительно, ты остался цел и невредим. Куда ступать будешь дальше?",
    "Возможно, сегодня твой счастливый день. Я сделаю всё, чтобы это исправить.",
    "Следующая дверь будет с таким значком: -",
    "Ты мне поверил? Зачем? Я воплощение зла! (Но милое)",
    "НЕЕЕТ. НЕ НАДО, НЕ ИДИ ТУДА. НЕЕЕЕЕЕЕЕЕТ..."
]
helps_doors_text = [
    "Я никому не расскажу, что ты решил нарушить правила. Надеюсь, мы подружимся. Я помогу тебе выйти.",
    "Я уверен, что вместе нас ждут крутые приключения. Какая следующая дверь?",
    "Сейчас мне кажется, что верная дверь будет со знаком ^ !",
    'Ты мне не поверил? Обидно, конечно, но спасибо, что не погубил нас обоих.',
    'Постой, ты уверен? Я беспокоюсь за тебя, столько всего прошли вместе, не рискуй жизнью... Выбирай с умом.'
]

    


@bot.message_handler(commands=['start'])
def starter_pack(message):
    try:
        restarter(message)
    except Exception as e:
        print(f"error in starter {e}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('Я готов!!!')
        markup.add(btn)
        sent_message = bot.send_message(message.from_user.id,
                         text='Вы готовы к приключению перед bmScary?',
                         reply_markup=markup, timeout=30)


@bot.message_handler(commands=['bot_update'])
def send_message_about_update(message):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    users = con.execute("select id from users").fetchall()
    # print(users)
    for i in users:
        bot.send_message(int(i[0]), text="Предупреждаю, скоро бот будет перегружен. Прошу не бить меня палками <3", timeout=30)
    con.close()

@bot.message_handler(commands=['users'])
def send_users(message):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    users = con.execute("select id from users").fetchall()
    data = []
    for i in users:
        UsrInfo = bot.get_chat_member(i[0], i[0]).user
        data.append(f"{i[0]} @{UsrInfo.username}")
    ui = str(message.from_user.id)
    if ui == admin:
        bot.send_message(int(ui), text='\n'.join(data), timeout=30)
    con.close()


@bot.message_handler(commands=['restart'])
def restarter(message):
    ui = str(message.from_user.id)
    update_user_fulldata(ui, "rdy", 1, "ВСТАТЬ С КРОВАТИ", {
        "ПРОЙТИ МИ  МО": 0,
        "ПОСТУЧАТЬ В ДВЕРЬ": 0,
        "ИДТИ ДАЛЬШЕ": 0,
        "ПЕРЕЛИСТНУТЬ ДАЛЬШЕ": 0,
        "ДА": 0,
        "НЕТ": 0,
        "СЧЕТЧИК": 0
    }, 0, 0)
    patter_job(1, ui)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    ui = str(message.from_user.id)
    try:
        add_users_to_db(ui)
    except Exception:
        pass
    user_input = message.text.lower()
    try:
        user = list(get_user_data_from_db(ui))
    except Exception as e:
        print(f"error is {e}")
        return

    try:
        if user[1] == 33 or user[1] == 7 or (
                user_input.upper() == "ЗАБРАТЬ ШЕСТЕРНЮ, ЗАМЕНИВ ЕЁ ГАЙКОЙ И УКРАСИТЬ КРОВАТКУ ЛОСКУТАМИ ТКАНИ" and
                user[3]["СЧЕТЧИК"] == 2 and user[1] == 55):
            user[3]["СЧЕТЧИК"] += 1
    except Exception:
        pass
    # print("user stat after schtchik update")
    # print(user)

    if str(ui) in admins:
        try:
            patter_job(user_input, ui)
            return
        except Exception:
            pass
    #
    #
    #
    #
    #
    #
    #
    #
    #
    if user_input.lower().split('!')[0] == 'я готов':
        bot.send_message(int(admin), text="В игру добавился " + str(message.from_user.username), timeout=30)

        try:
            # user = list(get_user_data_from_db(ui))
            patter_job(1, ui)
        except Exception as e:
            print(f"error is {e}")
            bot.send_message(int(ui), text='Попробуйте /restart', timeout=30)

    elif user[0] == "input":
        if user_input in user[2]:
            patter_job(25, ui)
        else:
            patter_job(26, ui)

    elif user[0] == "doors":
        ebka_doors(user_input, ui, user[-2], user[-1], user[3])

    elif 'zagadka' in user[0]:
        ebka_zagadka(user_input, ui, user[0])

    elif user_input.upper() in user[2]:
        for i in user[2]:
            if i.upper() in list(user[3].keys()):
                user[3][i.upper()] += 1
        try:
            if user_input.upper() == "ПРОЙТИ МИМО" and user[3][user_input.upper()] <= 3 and (
                    int(user[1]) not in [9]):
                user[3]["ИДТИ ДАЛЬШЕ"] += 1
            elif user_input.upper() == "НЕ ПОДХОДИТЬ К НЕМУ И ИДТИ ДАЛЬШЕ":
                user[3]["ИДТИ ДАЛЬШЕ"] += 1
            elif user_input.upper() == "ИДТИ ДАЛЬШЕ" and user[3][user_input.upper()] == 1 and user[1] not in [7, 8]:
                if int(user[1] == 33):
                    user[3]["ИДТИ ДАЛЬШЕ"] += 1
                user[3]["ПРОЙТИ МИМО"] += 1
            amount = user[3][user_input.upper()] * -1

        except Exception:
            amount = 0
        idshka = get_id_to_move(user_input)[amount][0]
        # print(f"idshka is {idshka}")
        if int(idshka) == 9999:
            if user[3]["СЧЕТЧИК"] >= 3:
                patter_job(79, ui, user[3])
            else:
                patter_job(77, ui, user[3])

        else:
            patter_job(idshka, ui, user[3])

    else:
        patter_job(user[1], ui, user[3])
        # bot.send_message(int(ui),
        #                  text="Такого действия нет, вы уверены в правильности выбора?")


def ebka_doors(user_input, ui, door_id, door_var, slovar):
    if user_input[-1] == correct_doors[door_id] and door_var != 2:
        door_id += 1
        door_var = 1
        update_ebka_doors(ui, door_id, door_var)

        if door_id == 6:
            patter_job(78, ui)
        else:
            bot.send_message(int(ui), text=correct_doors_text[door_id - 1], timeout=30)
    elif user_input[-1] == helps_doors[door_id] and door_var != 1:
        door_id += 1
        door_var = 2
        update_ebka_doors(ui, door_id, door_var)

        if door_id == 6:
            patter_job(63, ui)
        elif door_id != 6:
            bot.send_message(int(ui), text=helps_doors_text[door_id - 1], timeout=30)
    else:
        patter_job(64, ui)


def update_ebka_doors(ui, door_id, door_var):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    con.execute("UPDATE users SET door_pos=? ,door_var=? WHERE id=?",
                (door_id, door_var, int(ui)))
    con.commit()
    con.close()


def ebka_zagadka(user_input, ui, status):
    if "1" in status:
        if user_input.lower() == zagadka_1:
            patter_job(49, ui)
        else:
            patter_job(48, ui)
    elif "2" in status:
        if user_input.lower() == zagadka_2:
            patter_job(51, ui)
        else:
            patter_job(50, ui)
    else:
        # print(f"user input is {user_input}")
        if user_input.lower() == zagadka_3:
            patter_job(53, ui)
        else:
            patter_job(52, ui)


def patter_job(idshka, ui, slovar=None):
    # print(f"idshka is {idshka}")
    # print(f"ui is {ui}")
    user = list(get_user_data_from_db(ui))
    if slovar is None:
        slovar = user[3]
    else:
        slovar = slovar
    pr_answers = []
    text, moves = get_data_from_db(idshka)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in moves[0].split("!/!"):
        if i == "Net":
            markup = types.ReplyKeyboardRemove()
            break
        elif i == door_password:
            pr_answers.append(i.lower())
            markup = types.ReplyKeyboardRemove()
            break
        elif i in [zagadka_1, zagadka_2, zagadka_3]:
            pr_answers.append(i.lower())
            markup = types.ReplyKeyboardRemove()
            break
        elif i.upper() == "ЗАБРАТЬ ШЕСТЕРНЮ, ЗАМЕНИВ ЕЁ ГАЙКОЙ И УКРАСИТЬ КРОВАТКУ ЛОСКУТАМИ ТКАНИ":
            if user[3]["СЧЕТЧИК"] != 2:
                continue
        btn = types.KeyboardButton(i)
        markup.add(btn)
        pr_answers.append(i.lower())
    # try:
    #     markup.add(types.KeyboardButton("/restart"))
    # except Exception:
    #     pass

    if moves[0].split("!/!")[0] == door_password:
        status = "input"
    elif moves[0].split("!/!")[0] == zagadka_1:
        status = "zagadka_1"
    elif moves[0].split("!/!")[0] == zagadka_2:
        status = "zagadka_2"
    elif moves[0].split("!/!")[0] == zagadka_3:
        status = "zagadka_3"

    elif moves[0].split("!/!")[0] == "ДВЕРЬ =":
        status = "doors"
        user[4], user[5] = 0, 0

    else:
        status = "rdy"
    update_user_fulldata(ui, status, idshka, moves[0], slovar, user[4], user[5])
    photo = get_photos(idshka)
    if "NET" in photo:
        pass
    else:
        if any([i in photo for i in ["19", "27", "30", "33", "34"]]) == 1:
            pass
        elif "18" in photo:
            bot.send_photo(int(ui), photo=open("PHOTO_35.png", 'rb'), timeout=30)
            bot.send_photo(int(ui), photo=open(photo, 'rb'), timeout=30)
        else:
            bot.send_photo(int(ui), photo=open(photo, 'rb'), timeout=30)

    for txt in text[0].split("!/!"):
        if any(i in photo for i in ["19", "27", "34"]) and text[0].split("!/!").index(txt) == 1:
            bot.send_photo(int(ui), photo=open(photo, "rb"), timeout=30)
        bot.send_message(int(ui),
                         text=str(txt),
                         reply_markup=markup,
                         parse_mode="Markdown", timeout=30)
    if any(i in photo for i in ["30", "33"]):
        bot.send_photo(int(ui), photo=open(photo, "rb"), timeout=30)
    # print(f"After bot's answer user have tis {user}")


def get_data_from_db(idshka):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    text = con.execute("select text from trash where id=?", (idshka,)).fetchone()

    moves = con.execute("select moves from trash where id=?", (idshka,)).fetchone()

    con.close()
    return text, moves


def get_id_to_move(move):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    mvs = con.execute("select where_to_go from moves where move=?", (move.upper(),)).fetchall()
    con.close()
    return mvs


def get_photos(idshka):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    ph = con.execute(f"select photos from trash where id=?", (idshka,)).fetchone()[0]
    con.close()
    return f"PHOTO_{ph}.png"


# ДВЕРЬ =!/!ДВЕРЬ *!/!ДВЕРЬ -!/!ДВЕРЬ ^
def add_users_to_db(ui):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")

    con.execute("insert into users (id,status,position,answers,slovar,door_pos,door_var) values (?,?,?,?,?,?,?)",
                (int(ui), "rdy", 1, 'встать с кровати', "0,0,0,0,0,0,0", 0, 0,))
    con.commit()
    con.close()


def update_user_fulldata(ui, status, idshka, pr_answers, slovar, door_id, door_var):
    slovar_data = [str(slovar[i]) for i in list(slovar.keys())]
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    con.execute("UPDATE users SET status=?, position=?, answers=?, slovar=?, door_pos=?, door_var=? WHERE id=?",
                (status, idshka, pr_answers, ",".join(slovar_data), door_id, door_var, int(ui)))

    con.commit()    
    con.close()


def get_user_data_from_db(ui):
    import sqlite3 as sl
    con = sl.connect("USERSS.db")
    _, status, idshka, pr_answers, slovar_data, door_id, door_var = con.execute("select * from users where id=?",
                                                                                (int(ui),)).fetchone()
    slovar_data = [int(i) for i in slovar_data.split(",")]
    pr_answers = pr_answers.split("!/!")
    slovar = {
        "ПРОЙТИ МИМО": slovar_data[0],
        "ПОСТУЧАТЬ В ДВЕРЬ": slovar_data[1],
        "ИДТИ ДАЛЬШЕ": slovar_data[2],
        "ПЕРЕЛИСТНУТЬ ДАЛЬШЕ": slovar_data[3],
        "ДА": slovar_data[4],
        "НЕТ": slovar_data[5],
        "СЧЕТЧИК": slovar_data[6]
    }
    con.close()
    return status, idshka, pr_answers, slovar, door_id, door_var


while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"bot error is {e}")
        sleep(1)
