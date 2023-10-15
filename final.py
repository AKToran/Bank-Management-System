class Bank:
    total_balance = 0
    accounts_list = []
    loan_given = 0
    loan_available = True
    is_bankrupt = False

class User:
    def __init__(self, name, email, address, account_type) -> None:
        self.name = name 
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.loan_count = 0
        self.history = {}
        self.account_no = f'{self.name}-{self.email}'
        Bank.accounts_list.append(self)
        print("\nAccount creation Successful.")
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            Bank.total_balance += amount
            self.history["Deposited"] = amount
            print(f"\nSuccessfully deposited {amount}/=Tk to account: {self.name}")
        else:
            print("Invalid amount")
    
    def withdraw(self, amount):
        if Bank.is_bankrupt:
            print("\nThe Bank is bankrupt!!!")
        elif amount > self.balance:
            print("\nWithdrawal amount exceeded")
        elif amount <= self.balance and amount > Bank.total_balance:
            print("\nThe bank is Bankrupt!!!")
        elif amount > 0 and amount <= self.balance:
            self.balance -= amount
            Bank.total_balance -= amount
            self.history["Withdrawn"] = amount
            print(f"\nSuccessfully withdrawn {amount}/=Tk from account: {self.name}")
        else:
            print("Invalid whithdraw amount!")
       
    def check_balance(self):
        print(f"\n{self.name}s balance is {self.balance}/=Tk")

    def transaction_history(self):
        print(f"{self.name}s Transaction History:")
        for key, value in self.history.items():
            print(f'{key} - {value}')
    
    def take_loan(self, amount):
        if Bank.loan_available is False:
            print("\nLoan service is not available.")
        elif self.loan_count < 2 :
            self.balance += amount
            Bank.loan_given += amount
            self.history["Loan taken"] = amount
            self.loan_count += 1
            print(f"{amount}/=Tk loan added to the Account of {self.name}")
        else:
            print("\nLoan limit Exited!")
        
    def transfer_money(self, amount, acc_name):
        flag = True
        for account in Bank.accounts_list:
            if account.name == acc_name:
                flag = False
                if amount <= self.balance:
                    self.withdraw(amount)
                    account.deposit(amount)
                else:
                    print("\nNot enough money!")
        if flag:
            print("\nAccount does not exist!")

class Admin(User):
    name = "admin"
    password = "123"

    def __init__(self, name, email, address, account_type) -> None:
        super().__init__(name, email, address, account_type)

    @staticmethod
    def delete_account(acc_name):
        flag = True
        for account in Bank.accounts_list:
            if account.name == acc_name:
                flag = False
                Bank.accounts_list.remove(account)
                print(f"\nDeleted Account named: {acc_name}")
        if flag:
            print(f"\nNo account found.")

    @staticmethod
    def see_all_accounts():
        print("\n\t----------All acounts List-----------\n")
        print("Name ", " Email    ", "   Address ", "Account Type")
        for account in Bank.accounts_list:
            print(f"{account.name}   {account.email}    {account.address}      {account.account_type}")

    @staticmethod
    def bank_balance():
        print(f"\nTotal amount of money in the bank is: {Bank.total_balance}/=Tk")
    
    @staticmethod
    def total_loan():
        print(f"\nTotal amount of loan given from the bank: {Bank.loan_given}/=Tk")
    
    @staticmethod
    def change_loan_availability(flag):
        if flag:
            Bank.loan_available = True
            print("\nLoan service is available.")
        else:
            Bank.loan_available = False
            print("\nLoan service is no longer available.")

    @staticmethod
    def announce_bankrupt():
        Bank.is_bankrupt = True
        print("\nThe bank is bankrupt!!!")

admin = Admin
user = User
logged_in = None

while True:
    if logged_in == None:
        person = input("\nAre you an user or admin?: ")
        if person == "user":
            op = input("Log in or Register(L/R): ")
            if op == "R":
                print("\nRequired informations to Create an Account: ")
                name = input("Name: ")
                email = input("Email: ")
                address = input("Address: ")
                acc_type = input("Account type(savings/current): ")
                user = User(name, email, address, acc_type)
                logged_in = user
            else:
                user_name = input("What is your account name?: ")
                flag = True
                for account in Bank.accounts_list:
                    if account.name == user_name:
                        flag = False
                        user = account
                        print("\nUser Log in successful")
                
                if flag:
                    print(f"No account named: {user_name}")
                    continue
                else:
                    logged_in = user

        else:
            password = input("Enter Password(123): ")
            if password == Admin.password:
                print("\nAdmin Log in successful")
                logged_in = admin
            else:
                continue

    elif logged_in == user:
        print("\n\t-----------Welcome to the Bank of Aolia---------\n")
        print("Available Actions:")
        print("1: Deposit Money.")
        print("2: Withdraw Money.")
        print("3: Check available balance.")
        print("4: Check transaction history.")
        print("5: Take loan.")
        print("6: Transfer money.")
        print("7: Log Out.")
        op = int(input("Choose an Option: "))
        
        if op == 1:
            amount = int(input("Enter amount to deposit: "))
            user.deposit(amount)
        elif op == 2:
            amount = int(input("Enter amount to withdraw: "))
            user.withdraw(amount)
        elif op == 3:
            user.check_balance()
        elif op == 4:
            user.transaction_history()
        elif op == 5:
            amount = int(input("Enter amount of loan: "))
            user.take_loan(amount)
        elif op == 6:
            amount = int(input("Enter amount to transfer: "))
            name = input("Enter recipient name: ")
            user.transfer_money(amount, name)
        else:
            print("Log Out successful")
            logged_in = None

    elif logged_in == admin:
        print("\n\t-----------Welcome to the Bank of Aolia---------\n")
        print("Available Actions for Admin:")
        print("1: Create an Account.")
        print("2: Delete user account.")
        print("3: See all user accounts list.")
        print("4: Check total balance of the Bank of Aolia.")
        print("5: Check total loan given from the Bank of Aolia.")
        print("6: Change Loan feature of the Bank of Aolia.")
        print("7: Log Out.")
        op = int(input("Choose an Option: "))

        if op == 1:
            print("\nRequired informations to Create an Account: ")
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            acc_type = input("Account type(savings/current): ")
            user = Admin(name, email, address, acc_type)
            logged_in = user

        elif op == 2:
            name = input("Enter name of account to be deleted: ")
            admin.delete_account(name)
        
        elif op == 3:
            admin.see_all_accounts()

        elif op == 4:
            admin.bank_balance()
        elif op == 5:
            admin.total_loan()
        elif op == 6:
            flag = input("Loan feature(on/off): ")
            if flag == "on":
                admin.change_loan_availability(True)
            else: 
                admin.change_loan_availability(False)
        else:
            print("Log Out successful")
            logged_in = None
     