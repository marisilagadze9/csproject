from auth import register, log_in

while True:
    print("\n1. Register\n2. Login\n3. Exit")
    choice=input("Choose: ")

    if choice=="1":
        register()
    elif choice=="2":
        log_in()
    elif choice=="3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
