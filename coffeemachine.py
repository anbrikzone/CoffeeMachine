import json

# class for read and save to json file - our database
class Database:
    def __init__(self) -> None:
        self.DB = "db.json"
    
    # open and read json file
    def read(self) -> object:
        with open(self.DB, "r") as f:
             data = json.load(f)
        return data
    
    # save and close json file
    def save(self, data) -> None:
        with open(self.DB, "w") as f:
            json.dump(data, f, indent=4)

# MenuItem class for getting info about a drink
class MenuItem:
    #initialize with attributes name, cost and ingredients
    def __init__(self, name) -> None:
        self.name = name
        self.cost = Database().read()["MenuItem"][name]["cost"]
        self.ingredients = Database().read()["MenuItem"][name]["ingredients"]

# Menu class for getting info about all drinks
class Menu: 
    def __init__(self) -> None:
        self.db = Database().read()
        self.data = self.db["MenuItem"]

    def get_items(self) -> str:
        return "/".join(self.data)
    
    def find_drink(self, order_name) -> object:
        try:
            order = MenuItem(order_name)
        except:
            order = None
        return order

# CoffeeMaker class for making drink, checking resources and providing report about resources
class CoffeeMaker:
    def __init__(self) -> None:
        self.db = Database().read()
        self.elements = self.db["Ingredients"]
        self.money = MoneyMachine().report()

    def report(self) -> str:
        elem = []
        for key, value in self.elements.items():
            elem.append(f"{key}: {value[0]}{value[1]}")
        elem.append(self.money)
        return "\n".join(elem)

    def is_resource_sufficient(self, drink) -> bool:
        water, coffee, milk = MenuItem(drink).ingredients.values()
        i_water, i_coffee, i_milk = self.elements.values()

        if water < i_water[0] and coffee < i_coffee[0] and milk < i_milk[0]:
            return True
        else:
            return False

    def make_coffee(self, order):
        drink = Menu().find_drink(order)
        if drink is not None:
            if self.is_resource_sufficient(drink.name):
                water, coffee, milk = MenuItem(drink.name).ingredients.values()
                i_water, i_coffee, i_milk = self.elements
                self.elements[i_water][0] = self.elements[i_water][0] - water
                self.elements[i_coffee][0] = self.elements[i_coffee][0] - coffee
                self.elements[i_milk][0] = self.elements[i_milk][0] - milk
                Database().save(self.db)
                return True
            else:
                return False
        else:
            return False
        
# MoneyMachine for add_money, convert string to float and print report
class MoneyMachine:
    def __init__(self) -> None:
        self.db = Database().read()
        self.money = self.db["Money"]

    def report(self):
        return f"${format(self.money, ".2f")}"
    
    def make_payment(self, drink, cost):
        cost_item = MenuItem(drink).cost
        if cost > cost_item:
            return True
        else:
            return False
    
    def money2float(self, money_string) -> float:
        cost = 0
        try:
            parts = money_string.split(",")
            coin_names = {"quar": 0.25, "dime": 0.1, "nick": 0.05, "penn": 0.01}
            for item in parts:
                coin, coin_name = item.strip().split(" ")
                coin = int(coin)
                for part, val in coin_names.items():
                    if part in coin_name:
                        cost += coin * val
            return cost
        except: 
            return 0.0

    def add_money(self, cost):
        self.db.update({"Money": self.money + cost})
        Database().save(self.db)
        return True