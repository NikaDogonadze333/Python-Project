from storage import load_users, save_users
from models import Client, Admin

def register_user(users):
    username = input("შეიყვანეთ მომხმარებლის სახელი: ").strip()
    if not username:
        raise ValueError("სახელი არ შეიძლება იყოს ცარიელი")
    
    for user in users:
        if user.username == username:
            raise ValueError("მომხმარებელი ამ სახელით უკვე არსებობს")

    password = input("შეიყვანეთ პაროლი: ").strip()
    if not password:
        raise ValueError("პაროლი არ შეიძლება იყოს ცარიელი")

    new_client = Client(username, password)
    users.append(new_client)
    save_users(users)
    print("რეგისტრაცია წარმატებით დასრულდა!")

def login(users):
    username = input("მომხმარებლის სახელი: ").strip()
    password = input("პაროლი: ").strip()

    for user in users:
        if user.username == username and user.check_password(password):
            return user
    raise ValueError("არასწორი სახელი ან პაროლი")

def client_menu(client, users):
    while True:
        print("\n--- კლიენტის მენიუ ---")
        print("1. ბალანსის ნახვა")
        print("2. თანხის შეტანა")
        print("3. თანხის გატანა")
        print("4. სესხის მოთხოვნა")
        print("5. სესხების სტატუსი")
        print("6. გასვლა")

        choice = input("აირჩიეთ მოქმედება: ").strip()

        try:
            if choice == "1":
                print(f"თქვენი ბალანსი: {client.balance} ლარი")
            elif choice == "2":
                amount = float(input("შეიყვანეთ შესატანი თანხა: "))
                client.deposit(amount)
                save_users(users)
                print("თანხა წარმატებით ჩაირიცხა!")
            elif choice == "3":
                amount = float(input("შეიყვანეთ გამოსატანი თანხა: "))
                client.withdraw(amount)
                save_users(users)
                print("თანხა წარმატებით გაიტანეთ!")
            elif choice == "4":
                amount = float(input("შეიყვანეთ სესხის თანხა: "))
                client.request_loan(amount)
                save_users(users)
                print("სესხის მოთხოვნა გაგზავნილია!")
            elif choice == "5":
                for i, loan in enumerate(client.loans):
                    print(f"{i}. თანხა: {loan['amount']} | სტატუსი: {loan['status']}")
            elif choice == "6":
                break
            else:
                print("არასწორი არჩევანი!")
        except ValueError as e:
            print(f"შეცდომა: {e}")

def admin_menu(admin, users):
    while True:
        print("\n--- ადმინის მენიუ ---")
        print("1. სესხების დამტკიცება")
        print("2. გასვლა")

        choice = input("აირჩიეთ მოქმედება: ").strip()

        if choice == "1":
            pending_loans = []
            for user in users:
                if isinstance(user, Client):
                    for i, loan in enumerate(user.loans):
                        if loan["status"] == "pending":
                            pending_loans.append((user, i, loan))

            if not pending_loans:
                print("მოლოდინში მყოფი სესხები არ არის.")
                continue

            for idx, (client, loan_idx, loan) in enumerate(pending_loans):
                print(f"{idx}. მომხმარებელი: {client.username} | თანხა: {loan['amount']}")

            sel = int(input("აირჩიეთ სესხის ნომერი დასამტკიცებლად: "))
            if 0 <= sel < len(pending_loans):
                target_client, target_loan_idx, _ = pending_loans[sel]
                admin.approve_loan(target_client, target_loan_idx)
                save_users(users)
                print("სესხი წარმატებით დამტკიცდა!")
            else:
                print("არასწორი ინდექსი!")
        elif choice == "2":
            break
        else:
            print("არასწორი არჩევანი!")

def main():
    users = load_users()
    while True:
        print("\n--- ბანკომატი ---")
        print("1. რეგისტრაცია")
        print("2. შესვლა")
        print("3. გასვლა")

        choice = input("აირჩიეთ მოქმედება: ").strip()

        try:
            if choice == "1":
                register_user(users)
            elif choice == "2":
                user = login(users)
                if user.role == "admin":
                    admin_menu(user, users)
                else:
                    client_menu(user, users)
            elif choice == "3":
                break
            else:
                print("არასწორი არჩევანი!")
        except ValueError as e:
            print(f"შეცდომა: {e}")

if __name__ == "__main__":
    main()