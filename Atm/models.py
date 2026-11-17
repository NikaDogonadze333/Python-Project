class User:
    def __init__(self, username, password, role="client"):
        self.username = username
        self.__password = password
        self.role = role

    def check_password(self, password):
        return self.__password == password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.__password,
            "role": self.role
        }

class Client(User):
    def __init__(self, username, password, balance=0.0, loans=None):
        super().__init__(username, password, role="client")
        self.balance = float(balance)
        self.loans = loans if loans else []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("თანხა უნდა იყოს 0-ზე მეტი")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("თანხა უნდა იყოს 0-ზე მეტი")
        if amount > self.balance:
            raise ValueError("არასაკმარისი თანხა ანგარიშზე")
        self.balance -= amount

    def request_loan(self, amount):
        if amount <= 0:
            raise ValueError("სესხის თანხა უნდა იყოს 0-ზე მეტი")
        self.loans.append({"amount": amount, "status": "pending"})

    def to_dict(self):
        data = super().to_dict()
        data["balance"] = self.balance
        data["loans"] = self.loans
        return data

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="admin")

    def approve_loan(self, client, loan_index):
        if 0 <= loan_index < len(client.loans):
            if client.loans[loan_index]["status"] == "pending":
                client.loans[loan_index]["status"] = "approved"
                client.balance += client.loans[loan_index]["amount"]
                return True
        return False