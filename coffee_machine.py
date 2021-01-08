class CoffeeMachine:

    def __init__(self):
        self.covfefe = None
        self.item = 'water'
        self.espresso: dict = dict(water=250, milk=0, beans=16, cups=1, money=-4)
        self.latte: dict = dict(water=350, milk=75, beans=20, cups=1, money=-7)
        self.cappuccino: dict = dict(water=200, milk=100, beans=12, cups=1, money=-6)
        self.resources: dict = dict(water=400, milk=540, beans=120, cups=9, money=550)
        self.fill_prompts: dict = dict(water="Write how many ml of water do you want to add:",
                                       milk="Write how many ml of milk do you want to add:",
                                       beans="Write how many grams of coffee beans do you want to add:",
                                       cups="Write how many disposable cups of coffee do you want to add:")
        self.states = ['buy', 'fill', 'waiting']
        self.actual_state = 'waiting'
        self.buying_state: bool = False
        self.fill_states = ['water', 'milk', 'beans', 'cups']
        self.fill_counter = 1
        self.actual_fill_state = 'waiting'

    def operate(self, operation):
        if self.actual_state == self.states[0]:  # buy
            self.buy_operate(operation)
        elif self.actual_state == self.states[1]:  # fill
            self.fill_operate(operation)
        elif self.actual_state == self.states[2]:  # waiting
            if operation == 'buy':
                self.actual_state = self.states[0]  # set state to buy
                self.buy_operate(operation)
            elif operation == 'fill':
                self.actual_state = self.states[1]  # set state to fill
                self.fill_operate(operation)
            elif operation == 'take':
                self.take()
            elif operation == 'remaining':
                self.remaining()
        return

    def buy_operate(self, operation):
        if self.buying_state is False:
            self.buying_state = not self.buying_state
            print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        elif operation in ['1', '2', '3']:
            self.make_covfefe(operation)
        elif operation == 'back':
            self.actual_state = self.states[2]  # set state back to waiting
            self.buying_state = not self.buying_state
        return

    def fill_operate(self, operation):
        if self.actual_fill_state == 'waiting':
            print(self.fill_prompts.get('water'))
            self.actual_fill_state = 'water'
        elif self.actual_fill_state == 'water':
            self.resources[self.actual_fill_state]: int = self.resources[self.actual_fill_state] + int(operation)
            print(self.fill_prompts.get('milk'))
            self.actual_fill_state = 'milk'
        elif self.actual_fill_state == 'milk':
            self.resources[self.actual_fill_state]: int = self.resources[self.actual_fill_state] + int(operation)
            print(self.fill_prompts.get('beans'))
            self.actual_fill_state = 'beans'
        elif self.actual_fill_state == 'beans':
            self.resources[self.actual_fill_state]: int = self.resources[self.actual_fill_state] + int(operation)
            print(self.fill_prompts.get('cups'))
            self.actual_fill_state = 'cups'
        elif self.actual_fill_state == 'cups':
            self.resources[self.actual_fill_state]: int = self.resources[self.actual_fill_state] + int(operation)
            self.actual_state = self.states[2]
        return

    def make_covfefe(self, operation):
        if operation == '1':
            self.covfefe = self.espresso
        elif operation == '2':
            self.covfefe = self.latte
        elif operation == '3':
            self.covfefe = self.cappuccino
        for key in self.resources.keys():
            if self.resources[key] < self.covfefe.get(key):
                print(f"Sorry, not enough {key}!\n")
                self.actual_state = self.states[2]
                self.buying_state = not self.buying_state
                self.covfefe = None
                return
        print("I have enough resources to make you a coffee!\n")
        for key in self.resources.keys():
            self.resources[key] = self.resources.get(key) - self.covfefe.get(key)
        self.actual_state = self.states[2]
        self.buying_state = not self.buying_state
        self.covfefe = None
        return

    def remaining(self):
        print("The coffee machine has:")
        print("{} of water".format(self.resources['water']))
        print("{} of milk".format(self.resources['milk']))
        print("{} of coffee beans".format(self.resources['beans']))
        print("{} of disposable cups".format(self.resources['cups']))
        print("${} of money\n".format(self.resources['money']))
        return

    def take(self):
        print("I gave you ${}\n".format(self.resources['money']))
        self.resources['money'] = 0
        return

    def start(self):
        while True:
            if self.actual_state == self.states[2]:
                print("Write action (buy, fill, take, remaining, exit):")
            operation = input()
            if operation != 'exit':  # exit
                my_coffee_machine.operate(operation)
            else:
                break
        return


if __name__ == '__main__':
    my_coffee_machine = CoffeeMachine()
    my_coffee_machine.start()
