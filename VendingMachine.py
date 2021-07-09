


def add_dicts(dict1, dict2):
    for elem in dict1:
        dict2[elem] = dict2.get(elem, 0) + dict1[elem]

def sub_dicts(dict1, dict2):
    for elem in dict1:
        dict2[elem] -= dict1[elem]


class Item:

    def __init__(self, name: str, price: int, count: int = 0):
        self.name = name
        self.price = price
        self.count = count

    def __str__(self):
        return self.name



class VendingMachine:

    def __init__(self):
        self.item_list = []
        self.total_items = 0
        self.coin_list = [1, 5, 10, 25, 50, 100, 200]
        self.coins_count = {1: 1, 5: 1, 10: 1, 25: 1, 50: 1, 100: 1, 200: 1}
        self.total_money = sum(self.coins_count.values())


    def add_item(self, name, price, count):
        item = Item(name, price, count)
        self.item_list.append(item)
        self.total_items += 1
        
    def get_item_list(self):
        return self.item_list

    def get_total(self):
        return self.total_money

    def display_menu(self):
        print("MENU:")
        for i, item in enumerate(self.item_list):
            print("{}. {}: Rs {}".format(i + 1, item.name, str(item.price)))
        print("{}. Exit".format(len(self.item_list) + 1))


    def get_choice(self):
        choice = input("Choose the Item you want: ")
        choice_range = self.total_items + 1
        while not self.validate_choice(choice, choice_range):
            choice = self.get_choice()

        return int(choice)


    @staticmethod
    def validate_choice(choice, choice_range):
        try:
            choice = int(choice)
        except:
            print("Invalid Choice")
            return False

        if choice < 1 or choice > choice_range:
            print("Please Enter from the options in the Menu")
            return False

        return True


    @staticmethod
    def exit_machine(choice, exit_choice):
        if choice == exit_choice:
            print("Thank You for buying from us")
            return True
        return False


    @staticmethod
    def check_stock(item):
        return item.count > 0


    @staticmethod
    def get_item_price(item):
        return item.price

    @staticmethod
    def update_count(item):
        item.count -= 1


    def get_change(self, ammount, ind, available_denominations, denominations):

        if ammount == 0:
            return True
        if ind == -1:
            return False

        coin = self.coin_list[ind]
        if coin > ammount:
            return self.get_change(ammount, ind-1, available_denominations, denominations)

        required_coins = ammount // coin
        coin_count = min(available_denominations[coin], required_coins)
        ammount_deducted = coin_count * coin
        new_ammount = ammount - ammount_deducted
        denominations[coin] = coin_count
        if self.get_change(new_ammount, ind-1, available_denominations, denominations):
            return True
        del denominations[coin]
        return self.get_change(ammount, ind-1, available_denominations, denominations)


    def validate_denominations(self, required_price, denominations):
        print("We accept denominations of 1, 5, 10, 25, 50, 100, 200")
        print("Enter Denominations: ", end="")
        try:
            coins = list(map(int, input().split()))
        except:
            return False

        total_ammount_entered = sum(coins)
        if total_ammount_entered < required_price:
            print("Ammount Entered is too low")
            print("Transaction Failed")
            return False

        for coin in coins:
            if coin not in self.coins_count:
                print("We Do not accept that denomination")
                return False
            denominations[coin] = denominations.get(coin, 0) + 1

        return True


    def initiate_transaction(self, item):
        price = self.get_item_price(item)
        print("The Price of the {} is Rs {}".format(item.name, price))

        choice = input("Do You Wish to Cointinue(Y/N): ")
        while choice.lower() != 'n' and choice.lower() != 'y':
            print("Invalid Choice")
            choice = input("Do You Wish to Cointinue(Y/N): ")

        if choice == 'n':
            return False

        input_denominations = {}
        if not self.validate_denominations(price, input_denominations):
            return False


        ammount_entered = sum([key * input_denominations[key] for key in input_denominations])
        ammount_to_return = ammount_entered - price

        new_denominations = self.coins_count.copy()
        add_dicts(input_denominations, new_denominations)

        print("Change to return is Rs {}".format(ammount_to_return))
        denominations = {}
        ind = len(self.coin_list)-1
        if not self.get_change(ammount_to_return, ind, new_denominations, denominations):
            print("Sorry! Change not available")
            return False

        sub_dicts(denominations, new_denominations)
        self.coins_count = new_denominations
        print("Please take your change")
        return True


    def get_item(self, choice):
        chosen_item = self.item_list[choice-1]
        if not self.check_stock(chosen_item):
            print("The selected item is out of stock")

        transaction_success = self.initiate_transaction(chosen_item)
        if not transaction_success:
            print("Transaction Failed")
        else:
            print("Thank You for Visiting")
        self.update_count(chosen_item)


    def vending_machine_menu(self):
        exit_machine = False
        exit_choice = len(self.item_list) + 1

        while not exit_machine:
            self.display_menu()
            choice = self.get_choice()

            if self.exit_machine(choice, exit_choice):
                exit_machine = True
                continue

            self.get_item(choice)




myVendor = VendingMachine()
myVendor.add_item('Candy', 10, 20)
myVendor.add_item('Snack', 50, 10)
myVendor.add_item('Nuts', 90, 5)
myVendor.add_item('Coke', 25, 5)
myVendor.add_item('Pepsi', 35, 5)
myVendor.add_item('Soda', 45, 5)


myVendor.vending_machine_menu()

