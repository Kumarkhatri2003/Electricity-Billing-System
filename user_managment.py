from sql_con import get_connection
from datetime import datetime
def add_user(name,address,cont_num,email):
    conn =get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(name,address,contact_number,email) VALUES(%s,%s,%s,%s)",(name,address,cont_num,email))
    conn.commit()

    user_id = cursor.lastrowid  #get the user_id of newly added user

    #inserting default values to "fine tables"
    fine_query = """
    INSERT INTO fines(user_id,fine_amount,fine_date,reason)
    VALUES(%s, %s, %s, %s)
    """
    fine_values = (user_id, 0.00, datetime.now().date(),'No payment before 15th')
    cursor.execute(fine_query, fine_values)

    #insert default total amount to "total_amount" table
    total_query = """
    INSERT INTO total_amounts (user_id, billing_month, total_amount, paid_amount, payment_status, payment_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    total_values = (user_id, datetime.now().date(), 0.00, 0.00, 'Unpaid', None)
    cursor.execute(total_query, total_values)


     # Insert default due amount into the 'due_amounts' table (set to 0 initially)
    due_query = """
    INSERT INTO due_amounts (user_id, due_amount, due_date, fine_included)
    VALUES (%s, %s, %s, %s)
    """
    due_values = (user_id, 0.00, datetime.now().date(), 0.00)
    cursor.execute(due_query, due_values)

    credits_query = """
        INSERT INTO credits (user_id, credit_balance)
        VALUES (%s, %s)
        """
    credits_values = (user_id, 0.00)
    cursor.execute(credits_query, credits_values)

    conn.commit()
    conn.close()
    print(f"user {name} added sucessfully!")

def view_user():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    user = cursor.fetchall()

    if user:
        print("\n--- List of Users ---")
        for user_record in user:
            print(f"User Id: {user_record[0]}, Name: {user_record[1]}, Address: {user_record[2]}, Contact: {user_record[3]}, Email: {user_record[4]}\n")
    
    else:
        print("No user found.")

    conn.close()

def remove_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        
        cursor.execute("DELETE FROM fines WHERE user_id = %s", (user_id,))
        
        cursor.execute("DELETE FROM total_amounts WHERE user_id = %s", (user_id,))
        
       
        cursor.execute("DELETE FROM due_amounts WHERE user_id = %s", (user_id,))

        cursor.execute("DELETE FROM credits where user_id = %s", (user_id))
        
        # Delete from users table
        
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        
        cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
        # Commit changes
        conn.commit()
        print(f"User with ID {user_id} and all associated records are removed successfully.")

    except Exception as e:
        print(f"An error occurred while removing the user with ID {user_id}: {e}")
        conn.rollback()
    
    finally:
        conn.close()

        
