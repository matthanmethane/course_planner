import sqlite3
from urllib.request import pathname2url
from os.path import isfile
import json

def create_connection(db_path):
    try:
        # Checks if Database exists, if not then create one and create relevant tables
        if not isfile(db_path):
            sqliteConnection = sqlite3.connect(db_path)
            print("Database created and connected successfully.")
            cursor = sqliteConnection.cursor()
            initialise_tables(sqliteConnection, cursor)
        else:
            # Opens Database in read-write mode
            db_uri = 'file:{}?mode=rw'.format(pathname2url(db_path))
            sqliteConnection = sqlite3.connect(db_uri, uri=True)
            cursor = sqliteConnection.cursor()
            print("Database connected successfully.")

        return sqliteConnection, cursor

    except sqlite3.Error:
        print("Error: Fail to connect to sqlite", error)
        return

def close_connection(conn):
    conn.close()
    print("SQLite connection is closed.")
    return

def initialise_tables(conn, cursor):
    try:
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS loginCredentials( 
            student_id text PRIMARY KEY, 
            password text NOT NULL 
        );

        CREATE TABLE IF NOT EXISTS studentInfo( 
            student_id text PRIMARY KEY, 
            name text, 
            email text,
            gender text,
            course text,
            year integer,
            FOREIGN KEY (student_id) REFERENCES loginCredentials (student_id) 
        );

        CREATE TABLE IF NOT EXISTS courseInfo( 
            student_id text PRIMARY KEY, 
            plan_type text, 
            course_list blob,
            FOREIGN KEY (student_id) REFERENCES loginCredentials (student_id) 
        );
        """)
    except sqlite3.DatabaseError:
        print("Error: Fail to create tables")
    finally:
        conn.commit()
        return

def get_credentials(cursor, student_id):
    result_dict = {}
    loginCredentials_columns = ["student_id", "password"]

    cursor.execute("SELECT * FROM loginCredentials WHERE student_id=:student_id", {"student_id": student_id})
    # Entry: list of tuples in the order of column values i.e. [("id","password")]
    entry = cursor.fetchall()
    
  # Should never happen, if printed means something is wrong with the create table logic
    if len(entry) > 1:
        print("Error: Student credentials saved multiple times, please check database")
        return
    elif entry == []:
        return None

    # Order into dict
    for i in range(len(entry[0])):
        result_dict[loginCredentials_columns[i]] = entry[0][i]

    return result_dict

def get_student_info(cursor, student_id):
    result_dict = {}
    student_info_columns = ["student_id", "name", "email", "gender", "course", "year"]

    cursor.execute("SELECT * FROM studentInfo WHERE student_id=:student_id", {"student_id": student_id})
    entry = cursor.fetchall()

    # Should never happen, if printed means something is wrong with the create table logic
    if len(entry) > 1:
        print("Error: Student Info saved multiple times, please check database")
        return
    elif entry == []:
        return None

    # Order into dict
    for i in range(len(entry[0])):
        result_dict[student_info_columns[i]] = entry[0][i]

    return result_dict

def get_plan(cursor, student_id, plan_type):
    if plan_type not in ['plan_1', 'plan_2', 'registered']:
        print("Error: Invalid plan type.")
        return

    cursor.execute("SELECT course_list FROM courseInfo WHERE student_id=:student_id AND plan_type=:plan_type", {"student_id": student_id, "plan_type": plan_type})
    entry = cursor.fetchall()
    print(entry)

    if entry == []:
        print("Error: No entries for requested student_id and plan type")
    else:
        return json.loads(entry[0][0])

def save_plan(conn, cursor, student_id, course_dict, plan_type):
    ### course_dict: dict where key is course name and value is index i.e. {"cz4042":123456}
    ### plan_type: string i.e. plan_1, plan_2, registered
    if plan_type not in ['plan_1', 'plan_2', 'registered']:
        print("Error: Invalid plan type.")
        return

    # Delete all related entries if in table
    cursor.execute("DELETE FROM courseInfo WHERE student_id=:student_id AND plan_type=:plan_type", {"student_id": student_id, "plan_type": plan_type})
    # Insert entry
    cursor.execute("INSERT OR IGNORE INTO courseInfo VALUES (:student_id, :plan_type, :course_list)", {"student_id": student_id, "plan_type": plan_type, "course_list": json.dumps(course_dict)})
    conn.commit()

    ''' Use only after successfully enable foreign key constraints
    # Check if entry is inserted
    cursor.execute("SELECT changes()")
    no_changes = cursor.fetchone()[0]
    print(no_changes)

    if no_changes > 0:
        print("Plan saved into courseInfo table.")
    else:
        print("Error: Plan not saved, may be due to foreign key constraints")
    '''
    return

def save_credentials(conn, cursor, student_id, password):
    # Check if there is an existing entry, returns -1 if there is
    entry = get_credentials(cursor, student_id)

    if entry == None:
        cursor.execute("INSERT INTO loginCredentials VALUES (:student_id, :password)", {"student_id": student_id, "password": password})
        print("Credentials saved into loginCredentials table.")
        conn.commit()
        return
    else:
        print("Error: Existing username")
        return -1

def save_student_info(conn, cursor, student_id, student_name, email, gender, course, year):
    cursor.execute("INSERT INTO studentInfo VALUES (:student_id, :student_name, :email, :gender, :course, :year)",
     {"student_id": student_id, "student_name": student_name, "email": email, "gender": gender, "course": course, "year": year})
    print("Plan saved into studentInfo table.")
    conn.commit()

    ''' Use only after successfully enable foreign key constraints
    # Check if entry is inserted
    cursor.execute("SELECT changes()")
    no_changes = cursor.fetchone()[0]
    print(no_changes)

    if no_changes > 0:
        print("Student information saved into studentInfo table.")
    else:
        print("Error: Student information not saved, may be due to foreign key constraints")
    '''
    return

def update_student_info(conn, cursor, student_id, column_names, new_values):
    ## column_names: list of valid column names
    ## new_values: list of values, index corresponds to column_names list
    update_query= 'UPDATE studentInfo SET '
    if len(column_names) != len(new_values):
        print("Error: Mismatch in number of attributes and values provided")
        return
    
    for i in range(len(column_names)):
        if column_names[i] not in ['name', 'email', 'gender', 'course','year']:
            print("Error: Invalid column name")
            return
        elif column_names[i] != column_names[-1] :
            update_query = update_query + f'{column_names[i]}="{new_values[i]}",'
        else:
            update_query = update_query + f'{column_names[i]}="{new_values[i]}" WHERE student_id="{student_id}";'

    try:
        cursor.execute(update_query)
    except:
        print("Error: Unable to update studentInfo table.")
        return
    
    print("Plan saved into studentInfo table.")
    conn.commit()

'''Test cases'''
'''
def test_credentials():
    # If able to retreive existing credentials or rejction if non-existing

    # If rejection is sent when registering an existing acc

    # If able to successfully register a non-existing acc

def test_save_plan():
    # If able to save plan

    # If able to overwrite saved plan and old plan is deleted

def test_get_plan():

def test_student_info():
    # If able to get student info or none in non-existing

    # If able to save student info

    # If able to update student info

def main():
    db_path = r"ASE_Project.db"

    # Database connection
    conn, cursor = create_connection(db_path)

    # Testing
    
    close_connection(conn)


if __name__ == '__main__':
    main()
'''