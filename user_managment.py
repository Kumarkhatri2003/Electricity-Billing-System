import csv

#for adding the new users
def add_user(name,meter_id):
    with open("data.csv","a",newline="") as f:
       my_writer = csv.writer(f) 
       my_writer.writerow([name,meter_id])
       print(f"User {name} added successfully!")

#for viewing the user in csv file
def view_user():
    try:
        with open("data.csv","r") as f:
            my_reader = csv.reader(f)
            print("User list:\n")
            for el in my_reader:
                if len(el) >=2:
                    print(f"Name : {el[0]},Meter Id:{el[1]}")
                else:
                    print("skipping an invalid row:",el)

    except FileNotFoundError:
        print("No data found! Add a user first")
