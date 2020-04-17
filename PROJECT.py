import sqlite3 as sql


def open_bd():
    con = sql.connect("BD.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS 'BD' (ID STRING, flag STRING, photo BLOB, photo_flag String) ")

    return con, cur


def input_base(id, flag, photo, photo_flag):
    con, cur = open_bd()
    cur.execute(
        f"INSERT INTO 'BD' VALUES ('{id}', '{flag}', '{photo}','{photo_flag}')")
    con.commit()
    cur.close()


def delet_base(id):
    con, cur = open_bd()
    cur.execute(f"DELETE FROM 'BD' WHERE id='{id}'")
    con.commit()
    cur.close()


def flag_true(id):
    con, cur = open_bd()
    cur.execute(f"UPDATE BD SET flag = 'True' WHERE id ='{id}'")
    con.commit()
    cur.close()


def flag_false(id):
    con, cur = open_bd()
    cur.execute(f"UPDATE BD SET flag = 'False' WHERE id ='{id}'")
    con.commit()
    cur.close()


def out_flag(id):
    con, cur = open_bd()
    cur.execute(f"SELECT * FROM BD WHERE id = '{id}'")
    row = cur.fetchall()
    con.commit()
    cur.close()
    return row[0][1]


def insert_photo(id, text):
    con, cur = open_bd()
    cur.execute(
        f"UPDATE BD SET photo = (?), photo_flag = (?) WHERE id = '{id}'", (text, "True"))
    con.commit()
    cur.close()


def out_data():
    con, cur = open_bd()
    cur.execute("SELECT id, photo, photo_flag FROM BD ")
    row = cur.fetchall()
    cur.close()
    return row

# def out_photo(id):
#     con, cur = open_bd()
#     cur.execute(f"SELECT * FROM BD WHERE WHERE id = '{id}'")
#     row = cur.fetchall()
#     con.commit()
#     cur.close()
#     return row[0][2]


def main():
    a = input(">")
    if a == "1":
        id = input("Введите id\n>")
        st1 = input("Введите данные\n>")
       # input_base(id, st1)
    if a == "2":
        id = input("Введите id\n>")
        delet_base(id)
    if a == "3":
        id = input("Введите id\n>")
        flag_true(id)
    if a == "4":
        id = input("Введите id\n>")
        print(out_flag(id))


if __name__ == "__main__":
    main()
