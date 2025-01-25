from datetime import datetime
from sql_con import get_connection
import decimal


def calculate_bill(user_id, unit):
    # Calculate the bill amount based on units consumed
    if unit <= 20:
        price = unit * 4
    elif unit <= 50:
        price = 20 * 4 + (unit - 20) * 7.30
    elif unit <= 150:
        price = 20 * 4 + 30 * 7.30 + (unit - 50) * 8.60
    else:  # unit > 150
        price = 20 * 4 + 30 * 7.30 + 100 * 8.60 + (unit - 150) * 9.50

    conn = get_connection()
    cursor = conn.cursor()

    try:
        #reset the paid_amounts values
        cursor.execute(
            "UPDATE total_amounts SET paid_amount = 0.0 WHERE user_id = %s",
            (user_id,)
        )
        # Check if there is an existing record for the user
        cursor.execute(
            "SELECT user_id FROM total_amounts WHERE user_id = %s",
            (user_id,)
        )
        result = cursor.fetchone()

        if result:
          
            cursor.execute(
                """
                UPDATE total_amounts
                SET total_amount = %s, payment_status = %s
                WHERE user_id = %s
                """,
                (price, 'Unpaid', user_id)
            )
        else:
            # If no record exists, create a new record
            print(f"No record found for user_id {user_id}. Creating new record.")
            cursor.execute(
                """
                INSERT INTO total_amounts (user_id, total_amount, paid_amount, payment_status)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, price, 0.0, 'Unpaid')
            )

        # Check if the current date is past the 15th of the month to apply fine
        current_date = datetime.now().date()
        if current_date.day > 15:
            # Fetch total amount, paid amount, and payment status
            cursor.execute(
                "SELECT total_amount, paid_amount, payment_status FROM total_amounts WHERE user_id = %s",
                (user_id,)
            )
            amount_result = cursor.fetchone()

            if amount_result:
                total_amount, paid_amount, payment_status = amount_result

                # Convert amounts to float if they are of type decimal.Decimal
                total_amount = float(total_amount) if isinstance(total_amount, decimal.Decimal) else total_amount
                paid_amount = float(paid_amount) if isinstance(paid_amount, decimal.Decimal) else paid_amount

                # Apply fine if payment is overdue
                if paid_amount < total_amount and payment_status == 'Unpaid':
                    fine_amount = total_amount * 0.05  # 5% fine
                    fine_reason = "Late payment after the 15th of the month"
                    fine_date = current_date
                    print(f"Late payment detected. A fine of {fine_amount} is applied.")

                    # Insert fine into fines table
                    cursor.execute(
                        """
                        UPDATE fines
                        SET fine_amount = %s, fine_date = %s, reason = %s
               
                                 WHERE user_id = %s
                        """,
                        (fine_amount, fine_date, fine_reason, user_id)
                    )


        conn.commit()
        print(f"Bill calculated for user_id: {user_id}, Amount: {price}")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()
