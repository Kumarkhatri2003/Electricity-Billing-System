from billing import calculate_bill
from user_managment import add_user,view_user


def main():
   while True:
        print("\n--- Electricity Billing System ---")
        print("1. Add New User")
        print("2. View All Users")
        print("3. Calculate Bill")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter the name: ")
            meter_id = int(input("Enter the meter id: "))
            add_user(name,meter_id)
        
        elif choice == "2":
            view_user()
        
        elif choice =="3":
            unit =int(input("Enter electricity units consumed: "))
            bill_amt = calculate_bill(unit)
            print(f"Total Bill Amount:Rs.{bill_amt:.2f}")

        elif choice =="4":
            print("Thank you for using the system!\n")
            print("----Have a great day---")
        else:
            print("Invalid choice.Please try again")

if __name__ == "__main__":
    main()