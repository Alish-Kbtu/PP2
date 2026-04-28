import csv
import json
import psycopg2
from connect import get_connection


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    with open("schema.sql", "r", encoding="utf-8") as file:
        cur.execute(file.read())

    with open("procedures.sql", "r", encoding="utf-8") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()
    print("Tables and procedures created.")


def get_group_id(cur, group_name):
    if not group_name:
        return None

    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    username = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")

    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts (username, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (username, email, birthday, group_id)
    )

    contact_id = cur.fetchone()[0]

    cur.execute(
        """
        INSERT INTO phones (contact_id, phone, type)
        VALUES (%s, %s, %s)
        """,
        (contact_id, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")


def add_phone_to_contact():
    username = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL add_phone(%s, %s, %s)",
        (username, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Phone added.")


def move_contact_to_group():
    username = input("Contact name: ")
    group_name = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL move_to_group(%s, %s)",
        (username, group_name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact moved to group.")


def search_contacts():
    query = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    print_contacts(rows)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            c.id, c.username, c.email, c.birthday,
            g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
        ORDER BY c.username
        """,
        (group_name,)
    )

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by created date")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.username"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        print("Wrong choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT 
            c.id, c.username, c.email, c.birthday,
            g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY {order_by}
        """
    )

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def show_with_pagination():
    limit = 5
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    while True:
        cur.execute(
            """
            SELECT 
                c.id, c.username, c.email, c.birthday,
                g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )

        rows = cur.fetchall()
        print_contacts(rows)

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Wrong command.")

    cur.close()
    conn.close()


def import_from_csv():
    filename = input("CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row["username"]
            email = row["email"]
            birthday = row["birthday"]
            group_name = row["group"]
            phone = row["phone"]
            phone_type = row["type"]

            group_id = get_group_id(cur, group_name)

            cur.execute(
                """
                INSERT INTO contacts (username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (username, email, birthday, group_id)
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
                """,
                (contact_id, phone, phone_type)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported.")


def export_to_json():
    filename = input("JSON filename: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            c.id, c.username, c.email, c.birthday,
            g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
        """
    )

    rows = cur.fetchall()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4],
            "phone": row[5],
            "type": row[6]
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    cur.close()
    conn.close()
    print("JSON exported.")


def import_from_json():
    filename = input("JSON filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

        for item in data:
            username = item["username"]
            email = item["email"]
            birthday = item["birthday"]
            group_name = item["group"]
            phone = item["phone"]
            phone_type = item["type"]

            group_id = get_group_id(cur, group_name)

            cur.execute(
                """
                INSERT INTO contacts (username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (username, email, birthday, group_id)
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
                """,
                (contact_id, phone, phone_type)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("JSON imported.")


def delete_contact():
    username = input("Contact name to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE username = %s",
        (username,)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted.")


def update_contact():
    old_name = input("Current name: ")
    new_name = input("New name: ")
    new_email = input("New email: ")
    new_birthday = input("New birthday YYYY-MM-DD: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE contacts
        SET username = %s,
            email = %s,
            birthday = %s
        WHERE username = %s
        """,
        (new_name, new_email, new_birthday, old_name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    print("-" * 80)

    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Email: {row[2]}")
        print(f"Birthday: {row[3]}")
        print(f"Group: {row[4]}")
        print(f"Phone: {row[5]}")
        print(f"Type: {row[6]}")
        print("-" * 80)


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Create tables and procedures")
        print("2. Add contact")
        print("3. Add phone to contact")
        print("4. Move contact to group")
        print("5. Search contacts")
        print("6. Filter by group")
        print("7. Sort contacts")
        print("8. Show contacts with pagination")
        print("9. Import from CSV")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Update contact")
        print("13. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_tables()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            add_phone_to_contact()
        elif choice == "4":
            move_contact_to_group()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            sort_contacts()
        elif choice == "8":
            show_with_pagination()
        elif choice == "9":
            import_from_csv()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "12":
            update_contact()
        elif choice == "13":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Wrong choice.")


if __name__ == "__main__":
    menu()