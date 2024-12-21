# НЕДОЧЕТЫ
#Ещё относительно технической части, не знаю с чем конкретно связано и задумано так, но если достаточно быстро отвечать на вопросы, то предыдущие сообщения не удалялись
#
#
#
#
#
#
#
#
#




import telebot
from telebot import types
from pprint import pprint
from time import sleep
from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dbblock import *

path = "C://VSCODEaaa/BOT_bmSCARY/bot_v2/images/"
# путь к тексту нажатой кнопки callback.message.json['reply_markup']['inline_keyboard'][0][0]['text']
token = "7832340173:AAEB-UulMur740MaTcRqfInNvLANvWom0oE"
admin = 568037949
# ilia 1691708961
admins = [admin]
quest1_correct = ['студент', '9,3', 'раскольников', 'леший', 'лихо']
para_quest = ['6', '3', '18', '3', '7', '7', '2']
bot = telebot.TeleBot(token)
door_code = '6666'


# Админка + старт бота
@bot.message_handler(commands=['start'])
def starter_pack(message):
    try:
        add_user_to_db(message.from_user.id)
        UsrInfo = bot.get_chat_member(message.from_user.id, message.from_user.id).user
        bot.send_message(admin, "New user @" + str(UsrInfo.username))
    except (Exception,) as e:
        print(f"raised {e}")
        reload_user_data(message.from_user.id)
    try:
        add_user_to_user_message(message.from_user.id, message.from_user.id)
    except (Exception,) as e:
        pass

    try:
        ttu, txt_callbacks, command_callback = get_data_from_db("none")
        btn = create_callbacks_data(txt_callbacks, command_callback)
        with open(f'{path}image_1.jpg', 'rb') as ph:
            sent_message = bot.send_photo(chat_id=message.from_user.id, photo=ph, caption=ttu, timeout=10,
                                          reply_markup=btn)
            add_user_to_user_message(sent_message.message_id, message.from_user.id)
    except (Exception,) as e:
        ttu, txt_callbacks, command_callback = get_data_from_db("smth_went_wrong")
        btn = create_callbacks_data(txt_callbacks, command_callback)

        sent_message = bot.send_message(message.from_user.id,
                                        text=ttu,
                                        reply_markup=btn, timeout=30)
        add_user_to_user_message(sent_message.message_id, message.from_user.id)


@bot.message_handler(commands=["getuser"])
def answer(message):
    if message.from_user.id == admin:
        userid = int(message.text.split(maxsplit=1)[1])
        UsrInfo = bot.get_chat_member(userid, userid).user
        sent_message = bot.send_message(admin,
                                        "Id: " + str(UsrInfo.id) +
                                        "\nFirst Name: " + str(UsrInfo.first_name) +
                                        "\nLast Name: " + str(UsrInfo.last_name) +
                                        "\nUsername: @" + str(UsrInfo.username), timeout=30)


@bot.message_handler(commands=['restart'])
def restarter_user(message):
    try:
        reload_user_data(message.from_user.id)
    except (Exception,) as e:
        print(e)
        # bot.send_message(admin, e)
    try:
        ttu, txt_callbacks, command_callback = get_data_from_db("none")
        btn = create_callbacks_data(txt_callbacks, command_callback)
        try:
            with open(f'{path}image_1.jpg', 'rb') as ph:

                sent_message = bot.send_photo(chat_id=message.from_user.id, photo=ph, caption=ttu, timeout=10,
                                              reply_markup=btn)
                delete_user_message(message.from_user.id)
                add_user_to_user_message(sent_message.message_id, message.from_user.id)
        except (Exception,) as e:
            print(e)
        # sent_message = bot.send_message(message.from_user.id, ttu, reply_markup=btn)
    except Exception as e:
        ttu, txt_callbacks, command_callback = get_data_from_db("smth_went_wrong")
        btn = create_callbacks_data(txt_callbacks, command_callback)

        sent_message = bot.send_message(message.from_user.id,
                                        text=ttu,
                                        reply_markup=btn, timeout=30)
        delete_user_message(message.from_user.id)
        add_user_to_user_message(sent_message.message_id, message.from_user.id)


@bot.message_handler(commands=['contact'])
def starter_pack(message):
    try:
        bot.send_message(message.from_user.id, "Если возникли вопросы, пишите https://vk.com/sheil24"
                                               "или можно сюда. https://t.me/aarby_off")

    except (Exception,) as e:
        print(f"raised {e}")


# Техническая составляющая бота

def create_callbacks_data(callbacks_txt, callback_commands):
    btns = dict()
    value = 2
    if callbacks_txt[0] == 'Поискать ответ':
        ans = InlineKeyboardButton(text=callbacks_txt[0], url=callback_commands[0])
        markup = InlineKeyboardMarkup()
        markup.add(ans)
        return markup
    for i in range(len(callbacks_txt)):
        if len(callbacks_txt[i]) >= 25:
            value = 1
        btns[callbacks_txt[i]] = {"callback_data": callback_commands[i]}
    ans = quick_markup(values=btns, row_width=value)
    return ans


def sender_messages(ttu, txt_callbacks, command_callback, user_id, photo=None, message_id=None):
    if photo is None:
        if command_callback[0].lower() == "none":

            sent_message = bot.send_message(chat_id=user_id,
                                            text=ttu, timeout=10)
            delete_user_message(user_id)
            add_user_to_user_message(sent_message.message_id, user_id)

        else:
            if 'open_door_by' in command_callback[0]:
                markup = special_callback_data(txt_callbacks, command_callback, user_id)
            else:
                markup = create_callbacks_data(txt_callbacks, command_callback)

            sent_message = bot.send_message(chat_id=user_id,
                                            text=ttu,
                                            reply_markup=markup, timeout=10)
            delete_user_message(user_id)
            add_user_to_user_message(sent_message.message_id, user_id)
    else:
        if command_callback[0].lower() == "none":
            with open(f'{path}/{photo}', 'rb') as ph:

                sent_message = bot.send_photo(chat_id=user_id, photo=ph, caption=ttu, timeout=10)
                delete_user_message(user_id)
                add_user_to_user_message(sent_message.message_id, user_id)
        elif 'Иду в библиотеку' in ttu:
            if command_callback[0].lower() != "left_1":
                markup = create_callbacks_data(txt_callbacks, command_callback)
                bot.edit_message_text(
                    chat_id=user_id, text=ttu, reply_markup=markup, message_id=message_id
                )
            else:
                markup = create_callbacks_data(txt_callbacks, command_callback)
                with open(f'{path}/{photo}', 'rb') as ph:

                    bot.send_photo(chat_id=user_id, photo=ph, timeout=10)
                    sent_message = bot.send_message(chat_id=user_id, text=ttu, reply_markup=markup, timeout=10)
                    delete_user_message(user_id)
                    add_user_to_user_message(sent_message.message_id, user_id)
        else:
            if 'open_door_by' in command_callback[0]:
                markup = special_callback_data(txt_callbacks, command_callback, user_id)
            else:
                markup = create_callbacks_data(txt_callbacks, command_callback)
            with open(f'{path}/{photo}', 'rb') as ph:

                sent_message = bot.send_photo(chat_id=user_id, photo=ph, caption=ttu, timeout=10, reply_markup=markup)
                delete_user_message(user_id)
                add_user_to_user_message(sent_message.message_id, user_id)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("restart"))
def restarter(callback):
    reload_user_data(callback.message.chat.id)
    try:
        ttu, txt_callbacks, command_callback = get_data_from_db("none")
        btn = create_callbacks_data(txt_callbacks, command_callback)

        sent_message = bot.send_message(callback.message.chat.id, ttu, reply_markup=btn)
        delete_user_message(callback.message.chat.id)
        add_user_to_user_message(sent_message.message_id, callback.message.chat.id)
    except Exception as e:
        ttu, txt_callbacks, command_callback = get_data_from_db("smth_went_wrong")
        btn = create_callbacks_data(txt_callbacks, command_callback)

        sent_message = bot.send_message(callback.message.chat.id,
                                        text=ttu,
                                        reply_markup=btn, timeout=30)
        delete_user_message(callback.message.chat.id)
        add_user_to_user_message(sent_message.message_id, callback.message.chat.id)


@bot.callback_query_handler(
    func=lambda callback: not callback.data.startswith("quest") and not callback.data.startswith("uquest"))
def answer_to_users(callback):
    data = callback.data.lower()
    data = special_actions(data, callback.message.chat.id)

    updating_if_passing_checkpoint(data, callback.message.chat.id)
    # То что нажал мой друг, callback command
    txt = callback.message.json['reply_markup']['inline_keyboard'][0][0]['text']
    ttu, txt_callbacks, command_callback = get_data_from_db(data)
    ttu = '\n'.join(ttu.split('!/!'))
    # print(f"{ttu}\n, {txt_callbacks}\n, {command_callback}\n")

    update_user_status_helper(txt, callback, command_callback[0])

    try:
        photo = "image_" + get_photo_from_db(data) + '.jpg'
        sender_messages(ttu, txt_callbacks, command_callback, callback.message.chat.id, photo, callback.message.id)
    except (Exception,) as e:
        sender_messages(ttu, txt_callbacks, command_callback, callback.message.chat.id)
        print(e)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("uquest"))
def quest_callbacks(callback):
    question_num = int(callback.data.lower().split('quest')[1]) - 2

    num = upgrade_user_quest(callback.message.chat.id, False)
    data = callback.data.lower()
    print(f'Pizda {question_num, data, num}')
    if question_num == 6 and num == len(para_quest):
        data = data[1:] + '_2'
    elif question_num == 6 and num >= 2:
        data = data[1:] + '_1'
    elif question_num == 6:
        data = data[1:] + '_0'

    ttu, txt_callbacks, command_callback = get_data_from_db(data)

    ttu = '\n'.join(ttu.split('!/!'))
    markup = create_callbacks_data(txt_callbacks, command_callback)

    sent_message = bot.send_message(chat_id=callback.message.chat.id,
                                    text=ttu,
                                    reply_markup=markup, timeout=10)
    delete_user_message(callback.message.chat.id)
    add_user_to_user_message(sent_message.message_id, callback.message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("quest"))
def quest_callbacks(callback):
    question_num = int(callback.data.lower().split('quest')[1]) - 2
    num = upgrade_user_quest(callback.message.chat.id, True)
    data = callback.data.lower()
    if question_num == 6 and num == len(para_quest):
        data = data + '_2'
    elif question_num == 6 and num >= 2:
        data = data + '_1'
    elif question_num == 6:
        data = data + '_0'

    ttu, txt_callbacks, command_callback = get_data_from_db(data)

    ttu = '\n'.join(ttu.split('!/!'))
    markup = create_callbacks_data(txt_callbacks, command_callback)

    sent_message = bot.send_message(chat_id=callback.message.chat.id,
                                    text=ttu,
                                    reply_markup=markup, timeout=10)
    delete_user_message(callback.message.chat.id)
    add_user_to_user_message(sent_message.message_id, callback.message.chat.id)


# Логика самого квеста

@bot.message_handler(content_types=['text'])
def quest_logic(message):
    if check_if_admin(message):
        return
    text = message.text.lower()
    status = get_user_status(message.from_user.id)
    sudoku_pass = get_user_sudoku_pass(message.from_user.id)
    # print('here i am')
    # print(text)
    # print(status)
    text = text.replace(" ", '')
    if status == "ask_students" and text != quest1_correct[0]:
        callback_data = 'uncorrect_ans'
    elif status == "ask_students" and text == quest1_correct[0]:
        upgrade_user_sudoku(user_id=message.from_user.id)
        callback_data = 'correct_ans_water'
    elif text != quest1_correct[1] and status == "find_mates" and sudoku_pass == 0:
        callback_data = 'not_cool_bro_skip'
    elif text != quest1_correct[1] and status == "find_mates" and sudoku_pass == 1:
        callback_data = 'not_cool_bro_pass'
    elif text == quest1_correct[1] and status == "find_mates":
        callback_data = 'cool_bro'
    elif text == quest1_correct[3] and status == 'leshii':
        callback_data = 'leshii'
    elif status == "leshii":
        callback_data = 'ne_leshii'
    elif text == quest1_correct[2] and status == 'raskolnikov':
        callback_data = 'raskolnikov'
    elif status == "raskolnikov":
        callback_data = 'ne_raskolnikov'
    elif text == quest1_correct[4] and status == 'lixo':
        callback_data = 'lixo'
    elif status == "lixo":
        callback_data = 'ne_lixo'
    elif status == "wrong_code" and text != door_code:
        num = update_user_checkpoints(user_id=message.from_user.id, field="wrong_code")
        callback_data = 'wrong_code_' + str(num)
    elif status == "wrong_code":
        update_user_checkpoints(user_id=message.from_user.id, field="powerbank")
        callback_data = 'right_code'
    else:
        callback_data = 'smth_went_wrong'

    ttu, txt_callbacks, command_callback = get_data_from_db(callback_data)
    ttu = '\n'.join(ttu.split('!/!'))

    if command_callback[0].lower() == 'none':
        try:
            photo = get_photo_from_db(callback_data)
            with open(f'{path}/image_{photo}.jpg', 'rb') as ph:
                sent_message = bot.send_photo(chat_id=message.from_user.id, photo=ph, caption=ttu, timeout=10)
                delete_user_message(message.from_user.id)
                add_user_to_user_message(sent_message.message_id, message.from_user.id)
        except (Exception,) as e:

            sent_message = bot.send_message(chat_id=message.from_user.id, text=ttu, timeout=10)
            delete_user_message(message.from_user.id)
            add_user_to_user_message(sent_message.message_id, message.from_user.id)

    else:
        try:
            photo = get_photo_from_db(callback_data)
            btns = create_callbacks_data(txt_callbacks, command_callback)
            with open(f'{path}/image_{photo}.jpg', 'rb') as ph:
                sent_message = bot.send_photo(chat_id=message.from_user.id, photo=ph, caption=ttu, timeout=10,
                                              reply_markup=btns)
                delete_user_message(message.from_user.id)
                add_user_to_user_message(sent_message.message_id, message.from_user.id)
        except (Exception,) as e:
            sent_message = bot.send_message(chat_id=message.from_user.id, text=ttu, timeout=10, reply_markup=btns)
            delete_user_message(message.from_user.id)
            add_user_to_user_message(sent_message.message_id, message.from_user.id)


def updating_if_passing_checkpoint(data, user_id):
    if data == 'come_to_teach':
        field = 'birka'
    elif data == 'i_dont_want':
        field = 'elektrotok'
    elif data == "stop_looking":
        field = 'obezvojen'
    elif data == "check_vendor":
        field = 'got_chocolatka'
    elif data == "less_unlucky":
        field = 'bomjara'
    #  or data == ''
    elif data == "draw_smth" or data == 'kvas_da_1':
        field = 'true_konec'
    elif data == "think_a_lot":
        field = 'podymal'
    elif data == "read_book":
        field = 'read_book'
    elif data == 'find_another_way':
        field = 'other_enter'
    elif data == 'find_another_way':
        field = 'other_enter'
    elif 'open_door_by' in data:
        field = 'otmyc'
    else:
        return
    update_user_checkpoints(user_id, field)


def update_user_status_helper(txt, callback, command):
    status = get_user_status(callback.message.chat.id)
    print("")
    if txt == 'Поспрашивать студентов рядом':
        update_user_status(callback.message.chat.id, 'ask_students')
    elif txt == 'Поискать знакомых':
        update_user_status(callback.message.chat.id, 'find_mates')
    elif txt == "Поздороваться":
        update_user_status(callback.message.chat.id, 'raskolnikov')
    elif txt == "— Что за вопрос?":
        update_user_status(callback.message.chat.id, 'leshii')
    elif txt == "Ну и ладно" or txt == "Зайти в 5334":
        update_user_status(callback.message.chat.id, 'lixo')
    elif txt == 'Ввести код':
        update_user_status(callback.message.chat.id, "wrong_code")
    else:
        return


def give_food_helper(user_id, field):
    read = get_field_from_users(user_id, field)
    if read == 1:
        return "give_food_1"
    return "give_food_2"


def open_door_by_helper(user_id, field):
    read = get_field_from_users(user_id, field)
    if read == 1:
        return "open_door_by_pass"
    return "open_door_by_skip"


def fighthem_helper(user_id, field):
    read = get_field_from_users(user_id, field)
    if read == 1:
        return "fighthem_1"
    return "fighthem_2"


def dogovor_helper(user_id, field):
    read = get_field_from_users(user_id, field)
    if read == 1:
        return "try_to_dogovor_1"
    return "try_to_dogovor_2"


def end_helper(user_id, field):
    read = get_field_from_users(user_id, field)
    if read == 3:
        return "true_konec"
    return "ne_true_konec"


def kvas_helper(user_id, field1, field2):
    read = get_field_from_users(user_id, field1)
    read2 = get_field_from_users(user_id, field2)
    if read == 1 or read2 == 1:
        return "kvas_da_1"
    return "kvas_da_2"


def room_5334_helper(user_id, field):
    read = get_field_from_users(user_id, field)
    if read == 1:
        return "enter_strange_room_1"
    return "enter_strange_room_2"


def phone_helper(user_id, field):
    read = get_field_from_users(user_id, field)
    if read == 1:
        update_user_checkpoints(user_id,"true_konec")
        return "vkl_telephone_1"
    return "vkl_telephone_2"


def special_actions(data, user_id):
    if data == "open_door_by":
        data = open_door_by_helper(user_id, "podymal")
    elif data == "give_food":
        data = give_food_helper(user_id, "got_chocolatka")
    elif data == "fighthem":
        data = fighthem_helper(user_id, "elektrotok")
    elif data == "try_to_dogovor":
        data = dogovor_helper(user_id, "read_book")
    elif data == "kvas_da":
        data = kvas_helper(user_id, "obezvojen", 'bomjara')
    elif data == "enter_strange_room":
        data = room_5334_helper(user_id, 'birka')
    elif data == "vkl_telephone":
        data = phone_helper(user_id, 'powerbank')
    elif data == 'pls_let_me_die':
        print("DATA IS CHE ZA PIZDEC")
        data = end_helper(user_id, 'true_konec')
    return data


def check_if_admin(message):
    if message.from_user.id in admins:
        try:
            data = message.text.lower()
            ttu, txt_callbacks, command_callback = get_data_from_db(data)

            ttu = '\n\n'.join(ttu.split('!/!'))
            markup = create_callbacks_data(txt_callbacks, command_callback)
            sent_message = bot.send_message(chat_id=message.from_user.id,
                                            text=ttu,
                                            reply_markup=markup, timeout=10)
            return True
        except Exception as e:
            sent_message = bot.send_message(message.from_user.id,
                                            "Если вы пытались перейти к нужному блоку и не сработало, проверьте правильность ключа или напишите Яше")

    return False


def special_callback_data(txt_callbacks, command_callback, user_id):
    status_other_enter = get_field_from_users(user_id, "other_enter")
    status_otmyc = get_field_from_users(user_id, "otmyc")
    print(isinstance(status_otmyc, str))
    try:
        if status_otmyc != 0:
            txt_callbacks.remove("Открыть дверь отмычкой")

            command_callback.remove("open_door_by")
    except (Exception,) as e:
        print(e)

    try:
        if status_other_enter != 0:
            txt_callbacks.remove("Поискать другой выход")
            command_callback.remove("find_another_way")
    except (Exception,) as e:
        print(e)

    print(txt_callbacks, command_callback, user_id)
    btns = dict()
    value = 2
    for i in range(len(txt_callbacks)):
        if len(txt_callbacks[i]) >= 25:
            value = 1
        btns[txt_callbacks[i]] = {"callback_data": command_callback[i]}
    ans = quick_markup(values=btns, row_width=value)
    return ans


def delete_user_message(user_id):
    message_id = get_message_from_user_message(user_id)
    bot.delete_message(chat_id=user_id, message_id=message_id)


# bot.polling()
while True:
    try:
        bot.polling()
    except (Exception,) as e:
        print(f"Bot polling error {e}")
        sent_message = bot.send_message(admin, text=e, timeout=10)
        sleep(5)
