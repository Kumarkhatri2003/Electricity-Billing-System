from billing import calculate_bill
from user_managment import add_user,view_user,remove_user
from pay_bill import pay_bill
# from datetime import datetime


def main():
   while True:
        print("\n--- Electricity Billing System ---")
        print("1. Add New User")
        print("2. View All Users")
        print("3. Calculate Bill")
        print("4. Pay the Bills")
        print("5. Remove Users")

        choice = input("Enter your choice: ")

        if choice == "1":
            
            name = input("Enter the full name of customer:")
            address =input("Enter the address:")
            contact_number= input("Enter the contact number:")
            email=input("Enter the email:")

            add_user(name,address,contact_number,email)
        
        elif choice == "2":
            view_user()

             
        
        elif choice =="3":
            user_id = int(input("Enter the user_id:"))
            unit =int(input("Enter electricity units consumed: "))
            bill_amt = calculate_bill(user_id,unit)
           

        elif choice == "4":
            user_ID = int(input("Enter user ID to pay the bill: "))
            pay_bill(user_ID)
        
        elif choice == "5":
            user_Id = int(input("Enter the user to removed from the system:"))
            remove_user(user_Id)
        
        else:
            print("Invalid choice. Please try again.")

           
if __name__ == "__main__":
    main()