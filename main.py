import psycopg2


def create_db(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Clients(
        client_id SERIAL PRIMARY KEY,
        first_name VARCHAR(40),
        last_name VARCHAR(40),
        email VARCHAR(40))
        ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Phones(
        phone_id SERIAL PRIMARY KEY,
        number VARCHAR(11),
        client_id INTEGER REFERENCES Clients(client_id))
        ''')
    return


def add_phone(cur, client_id, phone):
    cur.execute('''
        INSERT INTO Phones(number, client_id)
        VALUES (%s, %s)
        ''', (phone, client_id))
    return


def add_client(cur, first_name, last_name, email, phone=None):
    cur.execute('''
        INSERT INTO Clients(first_name, last_name, email)
        VALUES (%s, %s, %s)
        ''', (first_name, last_name, email))
    cur.execute('''
        SELECT client_id FROM Clients
        ORDER BY client_id DESC
        LIMIT 1
        ''')
    id = cur.fetchone()[0]
    if phone is None:
        return id
    else:
        add_phone(conn, id, phone)
        return id


def change_client(cur, client_id, first_name=None, last_name=None, email=None):
    cur.execute('''
        SELECT * FROM Clients
        WHERE client_id = %s
        ''', (id, ))
    data = cur.fetchone()
    if first_name is None:
        first_name = data[1]
    if last_name is None:
        last_name = data[2]
    if email is None:
        email = data[3]
    cur.execute('''
        UPDATE Clients
        SET first_name = %s, last_name = %s, email =%s 
        WHERE client_id = %s
        ''', (first_name, last_name, email, id))
    return id


def delete_phone(cur, client_id, phone):
    cur.execute('''
        DELETE FROM Phones
        WHERE client_id = %s AND number = %s
        ''', (client_id, phone))
    return


def delete_client(cur, client_id):
    cur.execute('''
        DELETE FROM Phones
        WHERE client_id = %s
        ''', (client_id))
    cur.execute('''
        DELETE FROM Clients
        WHERE client_id = %s
        ''', (client_id))
    return


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    if first_name is None:
        first_name = '%'
    else:
        first_name = '%' + first_name + '%'
    if last_name is None:
        last_name = '%'
    else:
        last_name = '%' + last_name + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone is None:
        cur.execute('''
            SELECT c.client_id, c.fist_name, c.last_name, c.email, p.number FROM Clients c
            LEFT JOIN Phones p ON c.client_id = p.client_id
            WHERE c.first_name LIKE %s AND c.last_name LIKE %s
            AND c.email LIKE %s
            ''', (first_name, last_name, email))
    else:
        cur.execute('''
            SELECT c.client_id, c.fist_name, c.last_name, c.email, p.number FROM clients c
            LEFT JOIN phonenumbers p ON c.client_id = p.client_id
            WHERE c.first_name LIKE %s AND c.last_name LIKE %s
            AND c.email LIKE %s AND p.number like %s
            ''', (first_name, last_name, email, phone))
        return cur.fetchall()


with psycopg2.connect(database='clients_db', user='postgres', password='postgres') as conn:
    with conn.cursor() as cur:
        pass
conn.close()