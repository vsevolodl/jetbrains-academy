# Write your code here
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class Bank:

    def __init__(self):
        self.INN: int = 400000  # 6 digits
        self.states = ['waiting', 'new', 'login', 'authorized', 'transfer']
        self.actual_state = 'waiting'
        self.login_states = ['waiting', 'card', 'pin', 'authorized']
        self.actual_login_state = 'waiting'
        self.transfer_states = ['waiting', 'card', 'amount']
        self.actual_transfer_state = 'waiting'
        self.main_prompts: dict = dict(new="1. Create an account",
                                       login="2. Log into account",
                                       exit="0. Exit")
        self.authorized_prompts: dict = dict(balance="1. Balance",
                                             add='2. Add income',
                                             transfer='3. Do transfer',
                                             close='4. Close account',
                                             logout="5. Logout",
                                             exit="0. Exit")
        self.bank_users: dict = dict()
        self.actual_user = None
        self.actual_pin = None
        self.actual_card = None
        self.actual_money = None
        self.transfer_user = None
        self.transfer_card = None
        self.transfer_money = None
        self.transfer_amount = None

    @staticmethod
    def db_init():
        cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0 );')
        return

    def db_user_fetch(self):
        cur.execute(f'SELECT number, pin, balance FROM card WHERE number = {self.actual_card};')
        self.actual_user = cur.fetchall()
        return

    def db_transfer_fetch(self):
        cur.execute(f'SELECT number, pin, balance FROM card WHERE number = {self.transfer_card};')
        self.transfer_user = cur.fetchall()
        return

    def generate_user(self):
        locals()
        new_id: int = int(random.randint(100, 999))
        new_card: str = str(self.generate_card())
        new_pin: str = str(self.generate_pin())
        new_money: int = 0
        cur.execute(f'INSERT INTO card VALUES ({new_id}, {new_card}, {new_pin}, {new_money});')
        print(f'Your card has been created\nYour card number:\n{new_card}')
        print(f'Your card PIN:\n{new_pin}\n')
        self.actual_state = self.states[0]
        conn.commit()
        return

    def generate_card(self):
        locals()
        control_n: int = 0
        checksum: int = 0
        check: int = 0
        counter: int = 0
        raw_card_luhn: list = []
        raw_card: str = ''.join(str(self.INN) + str(random.randint(99999999, 999999999)))
        for char in raw_card:
            if counter % 2 == 0:
                char = str(int(char) * 2)
                if int(char) > 9:
                    char = str(int(char) - 9)
            counter += 1
            raw_card_luhn.append(char)
        for item in raw_card_luhn:
            control_n += int(item)
            check += int(item)
        while (control_n + checksum) % 10 != 0:
            checksum += 1
        raw_card = raw_card + str(checksum)
        return str(raw_card)

    @staticmethod
    def generate_pin():
        locals()
        show_pin: str = ''
        new_pin: int = int(random.randint(0000, 9999))
        if 100 <= new_pin <= 999:
            show_pin = ''.join(str('0' + str(new_pin)))
        elif new_pin < 100:
            show_pin = ''.join(str('00' + str(new_pin)))
        else:
            show_pin = str(new_pin)
        return str(show_pin)

    def transfer(self, operation):
        if self.actual_transfer_state == self.transfer_states[0]:
            print('Transfer\nEnter card number:')
            self.actual_transfer_state = self.transfer_states[1]
            return
        elif self.actual_transfer_state == self.transfer_states[1]:
            self.transfer_card = int(operation)
            if self.transfer_card == self.actual_card:
                print("You can't transfer money to the same account!\n")
                self.transaction_clean()
                return
            elif not self.check_card(self.transfer_card):
                print('Probably you made a mistake in the card number. Please try again!\n')
                self.transaction_clean()
            elif not self.client_card(self.transfer_card):
                print('Such a card does not exist.\n')
                self.transaction_clean()
                return
            elif self.check_card(self.transfer_card):
                print('Enter how much money you want to transfer:')
                self.actual_transfer_state = self.transfer_states[2]
                return
        elif self.actual_transfer_state == self.transfer_states[2]:
            self.transfer_amount = int(operation)
            if self.transfer_amount <= self.actual_user[0][2]:
                self.transaction()
                return
            else:
                print('Not enough money!\n')
                self.transaction_clean()
                return

    def transaction(self):
        self.db_transfer_fetch()
        self.db_user_fetch()
        self.actual_money: int = int(self.actual_user[0][2]) - self.transfer_amount
        self.transfer_money: int = int(self.transfer_user[0][2]) + self.transfer_amount
        cur.execute(f'UPDATE card SET balance = {self.actual_money} WHERE number = {self.actual_card};')
        cur.execute(f'UPDATE card SET balance = {self.transfer_money} WHERE number = {self.transfer_card};')
        conn.commit()
        print('Success!\n')
        self.transaction_clean()
        return

    def transaction_clean(self):
        self.actual_transfer_state = self.transfer_states[0]
        self.actual_state = self.states[3]
        self.transfer_user = None
        self.transfer_card = None
        self.transfer_money = None
        self.transfer_amount = None
        return

    @staticmethod
    def check_card(destination_card):
        locals()
        counter: int = 0
        raw_card: str = str(destination_card)[0:-1]
        last_digit: int = int(str(destination_card)[-1])
        checksum: int = 0
        raw_card_luhn: list = []
        control_n: int = 0
        check: int = 0
        for char in raw_card:
            if counter % 2 == 0:
                char = str(int(char) * 2)
                if int(char) > 9:
                    char = str(int(char) - 9)
            counter += 1
            raw_card_luhn.append(char)
        for item in raw_card_luhn:
            control_n += int(item)
            check += int(item)
        while (control_n + checksum) % 10 != 0:
            checksum += 1
        if checksum == last_digit:
            return True
        else:
            return False

    @staticmethod
    def client_card(destination_card):
        locals()
        cur.execute(f'SELECT EXISTS(SELECT number, pin, balance FROM card WHERE number = {destination_card});')
        if cur.fetchone()[0] == 0:
            return False
        else:
            return True

    def check_amount(self, operation):
        pass

    def login(self, operation):
        if self.actual_login_state == self.login_states[0]:
            print('Enter your card number:')
            self.actual_login_state = self.login_states[1]
            return
        elif self.actual_login_state == self.login_states[1]:
            self.actual_card = int(operation)
            print('Enter your PIN:')
            self.actual_login_state = self.login_states[2]
            return
        elif self.actual_login_state == self.login_states[2]:
            self.actual_pin = int(operation)
            self.authorization()
            return
        self.actual_login_state = self.login_states[3]
        self.actual_state = self.states[3]
        return

    def banking(self, operation):
        self.db_user_fetch()
        if operation == '1':
            print(f'\nBalance: {int(self.actual_user[0][2])}\n')
            return
        elif operation == '2':
            self.actual_money: int = int(self.actual_user[0][2]) + int(input('Enter income:\n'))
            cur.execute(f'UPDATE card SET balance = {self.actual_money} WHERE number = {self.actual_card};')
            print('Income was added!\n')
            conn.commit()
            return
        elif operation == '3':
            self.actual_state = self.states[4]
            self.transfer(operation)
            return
        elif operation == '4':
            cur.execute(f'DELETE FROM card WHERE number = {self.actual_card};')
            print('You account has been closed!\n')
            conn.commit()
            self.clean()
            return
        elif operation == '5':
            self.clean()
            print('You have successfully logged out!\n')
            return
        elif operation == '0':
            self.clean()
            self.bank_exit()
            return

    def authorization(self):
        self.db_user_fetch()
        if len(self.actual_user) != 0:
            if self.actual_pin == int(self.actual_user[0][1]):
                print('You have successfully logged in!\n')
                self.actual_login_state = self.login_states[3]
                self.actual_state = self.states[3]
                return
            else:
                print('Wrong card number or PIN!\n')
                self.clean()
                return
        else:
            print('Wrong card number or PIN!\n')
            self.clean()
            return

    @staticmethod
    def bank_exit():
        conn.commit()
        print('Bye!')
        exit()
        return

    def clean(self):
        self.actual_state = self.states[0]
        self.actual_login_state = self.login_states[0]
        self.actual_card = None
        self.actual_pin = None
        self.actual_user = None
        return

    def start(self):
        self.db_init()
        while True:
            if self.actual_state == self.states[0]:
                for key in self.main_prompts:
                    print(self.main_prompts.get(key))
            elif self.actual_state == self.states[3]:
                for key in self.authorized_prompts:
                    print(self.authorized_prompts.get(key))
            operation = input()
            if self.actual_state == self.states[0]:
                if operation == '1':
                    self.actual_state = self.states[1]
                    self.generate_user()
                elif operation == '2':
                    self.actual_state = self.states[2]
                    self.login(operation)
                elif operation == '0':
                    self.bank_exit()
            elif self.actual_state == self.states[2]:
                self.login(operation)
            elif self.actual_state == self.states[3]:
                self.banking(operation)
            elif self.actual_state == self.states[4]:
                self.transfer(operation)


if __name__ == '__main__':
    my_bank = Bank()
    my_bank.start()
