from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")


def call_upsert():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (username, phone))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted/updated successfully.")


def search_by_pattern():
    pattern = input("Enter search pattern: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def show_paginated():
    limit_value = int(input("Enter limit: "))
    offset_value = int(input("Enter offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit_value, offset_value)
    )
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def call_delete():
    value = input("Enter username or phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted if it existed.")


def call_bulk_insert():
    n = int(input("How many users do you want to insert? "))

    usernames = []
    phones = []

    for i in range(n):
        print(f"\nUser {i + 1}")
        username = input("Enter username: ")
        phone = input("Enter phone: ")

        usernames.append(username)
        phones.append(phone)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_users(%s, %s)", (usernames, phones))

    conn.commit()
    cur.close()
    conn.close()
    print("Bulk insert finished.")


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 - Create table")
        print("2 - Insert or update contact")
        print("3 - Search contacts by pattern")
        print("4 - Show contacts with pagination")
        print("5 - Delete contact")
        print("6 - Bulk insert users")
        print("0 - Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            call_upsert()
        elif choice == "3":
            search_by_pattern()
        elif choice == "4":
            show_paginated()
        elif choice == "5":
            call_delete()
        elif choice == "6":
            call_bulk_insert()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    menu()