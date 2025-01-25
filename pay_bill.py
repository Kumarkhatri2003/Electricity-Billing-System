from sql_con import get_connection
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def pay_bill(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Fetch total unpaid amount and due amount
        cursor.execute("SELECT total_amount, paid_amount FROM total_amounts WHERE user_id = %s AND payment_status = 'Unpaid'", (user_id,))
        total_result = cursor.fetchone()

        cursor.execute("SELECT due_amount FROM due_amounts WHERE user_id = %s", (user_id,))
        due_result = cursor.fetchone()

        cursor.execute("SELECT fine_amount FROM fines WHERE user_id = %s", (user_id,))
        fine_result = cursor.fetchone()

        cursor.execute("SELECT credit_balance FROM credits WHERE user_id = %s", (user_id,))
        credits_result = cursor.fetchone()

        if total_result:
            total_amount = Decimal(total_result[0]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            paid_amount = Decimal(total_result[1] or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            previous_due = Decimal(due_result[0] or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            fine_amount = Decimal(fine_result[0] or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            credit_balance = Decimal(credits_result[0] or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Apply credits to reduce the payable amount
            remaining_amount = (total_amount - paid_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            final_amount = (total_amount + previous_due + fine_amount - credit_balance).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            if final_amount < 0:
                final_amount = Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            print(f"User ID: {user_id}")
            print(f"Total Amount: {total_amount:.2f}")
            print(f"Previous Due: {previous_due:.2f}")
            print(f"Fine Amount: {fine_amount:.2f}")
            print(f"Credits Balance: {credit_balance:.2f}")
            print(f"Final Amount to be Paid: {final_amount:.2f}")

            # Take payment input
            payment_amount = Decimal(input("Enter the amount you want to pay: ")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            cursor.execute(
            "UPDATE credits SET credit_balance = 0.0 WHERE user_id = %s",
            (user_id,))

            cursor.execute(
            "UPDATE total_amounts SET total_amount = 0.0 WHERE user_id = %s",
            (user_id,))

            cursor.execute(
            "UPDATE fines SET fine_amount= 0.0 WHERE user_id = %s",
            (user_id,))
        
            if payment_amount >= final_amount:
                excess_payment = (payment_amount - final_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                # Full payment clears due and bill
                cursor.execute(
                    "UPDATE total_amounts SET paid_amount = %s, payment_status = 'Paid', payment_date = %s WHERE user_id = %s",
                    (total_amount, datetime.now(), user_id)
                )
                cursor.execute("UPDATE due_amounts SET due_amount = 0 WHERE user_id = %s", (user_id,))

                # Update credits balance with excess payment
                cursor.execute(
                    "UPDATE credits SET credit_balance = credit_balance + %s WHERE user_id = %s",
                    (excess_payment, user_id)
                )
                print(f"Full payment processed for User ID {user_id}. Total Paid: {payment_amount:.2f}. Excess Payment Credited: {excess_payment:.2f}")
            else:
                # Partial payment
                remaining_due = (final_amount - payment_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                cursor.execute(
                    "UPDATE total_amounts SET paid_amount = paid_amount + %s WHERE user_id = %s",
                    (payment_amount, user_id)
                )
                cursor.execute(
                    "UPDATE due_amounts SET due_amount = %s WHERE user_id = %s",
                    (remaining_due, user_id)
                )
                print(f"Partial payment processed for User ID {user_id}. Paid: {payment_amount:.2f}, Remaining Due: {remaining_due:.2f}")

            conn.commit()
        else:
            print(f"No unpaid bill found for user_id {user_id}.")
    except Exception as e:
        print(f"An error occurred while processing the payment for User ID {user_id}: {e}")
        conn.rollback()
    finally:
        conn.close()
