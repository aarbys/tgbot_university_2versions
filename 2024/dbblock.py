# fields = tuple('id', 'correct_ans', "sudoku_pass", 'status', 'birka', 'elektrotok', 'obezvojen', 'got_chocolatka',
#                'bomjara', 'podymal', 'read_book', 'true_konec'


def add_user_to_db(user_id):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    con.execute("insert into users "
                "(id,correct_ans,sudoku_pass,status,birka, elektrotok,obezvojen,got_chocolatka,bomjara,podymal,read_book,true_konec,powerbank,other_enter,otmyc,wrong_code) "
                "values (?,?,?,?,?,?,?,?,?,?,?,?,?, ?,?,?)",
                (user_id, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    con.commit()
    con.close()


def upgrade_user_quest(user_id, correct: bool):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    num = con.execute("select correct_ans from users where id=?", (user_id,)).fetchone()[0]
    if correct:
        num = int(num) + 1
        con.execute("UPDATE users SET correct_ans=? WHERE id=?", (num, user_id,))

    con.commit()
    con.close()
    return num


def upgrade_user_sudoku(user_id):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    num = con.execute("select correct_ans from users where id=?", (user_id,)).fetchone()[0]
    num = int(num) + 1
    con.execute("UPDATE users SET sudoku_pass=? WHERE id=?", (1, user_id,))

    con.commit()
    con.close()
    return num


def get_data_from_db(callback_text):
    print(callback_text)
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    ttu = con.execute("select ttu from text where defiant_callback=?", (callback_text,)).fetchone()[0]
    txt_callbacks = con.execute("select txt_callbacks from text where defiant_callback=?", (callback_text,)).fetchone()[
        0].split("!/!")
    command_callback = \
        con.execute("select command_callback from text where defiant_callback=?", (callback_text,)).fetchone()[0].split(
            "!/!")
    con.close()
    return ttu, txt_callbacks, command_callback


# def get_user_sudoku(user_id):
#     import sqlite3 as sl
#     con = sl.connect("database_all.db")
#     num = con.execute("select status from users where id=?", (user_id,)).fetchone()[0]
#     print(num)
#     con.execute("UPDATE users SET sudoku_pass=? WHERE id=?", (1, user_id,))
#
#     con.commit()
#     con.close()
#     return num


def reload_user_data(user_id):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    con.execute("UPDATE users "
                "SET correct_ans=?,sudoku_pass=?,status=?,birka=?, elektrotok=?,obezvojen=?,got_chocolatka=?,"
                "bomjara=?,podymal=?,read_book=?,true_konec=?,wrong_code=?,powerbank=?,other_enter=?,otmyc=? WHERE id=?",
                (0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, user_id))
    con.commit()
    con.close()


def update_user_status(user_id, status):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    con.execute("UPDATE users SET status=? WHERE id=?", (status, user_id,))
    con.commit()
    con.close()


def get_user_status(user_id):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    ans = con.execute("select status from users WHERE id=?", (user_id,)).fetchone()[0]
    con.commit()
    con.close()
    return ans


def get_user_sudoku_pass(user_id):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    ans = con.execute("select sudoku_pass from users WHERE id=?", (user_id,)).fetchone()[0]
    con.commit()
    con.close()
    return ans


def update_user_checkpoints(user_id, field):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    ind = con.execute("select {} from users where id=?".format(field), (user_id,)).fetchone()[0]
    ind = int(ind) + 1
    con.execute("UPDATE users SET " + field + '=? WHERE id=?', (ind, user_id,))
    con.commit()
    con.close()
    return ind


def get_field_from_users(user_id, field):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    ans = con.execute("select {} from users WHERE id=?".format(field), (user_id,)).fetchone()[0]
    con.commit()
    con.close()
    return ans


def get_photo_from_db(data):
    import sqlite3 as sl
    con = sl.connect("database_all.db", timeout=4)
    img = con.execute("select image from text where defiant_callback=?", (data,)).fetchone()[0]
    con.close()
    return img


def add_user_to_user_message(message_id, user_id):
    import sqlite3 as sl
    con = sl.connect("user_and_message.db", timeout=4)
    try:
        img = con.execute("insert into user_message (user_id, message_id) values (?,?)", (user_id, message_id,))
        con.commit()
        con.close()
        return img
    except (Exception,) as e:
        print(f"1Problem in db :{e}")
    try:
        img = con.execute("UPDATE user_message set message_id=? where user_id=?", (message_id, user_id,))
        con.commit()
        con.close()
        return img
    except (Exception,) as e1:
        print(f"2Problem in db :{e1}")



def get_message_from_user_message(user_id):
    import sqlite3 as sl
    con = sl.connect("user_and_message.db", timeout=4)
    img = con.execute("select message_id from user_message where user_id=?", (user_id,)).fetchone()[0]
    con.commit()
    con.close()
    return img
