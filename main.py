from coffeemachine import MenuItem, Menu, CoffeeMaker, MoneyMachine

# Run application
while True:
    drink = input(f"What would you like? {Menu().get_items()}: ")
    # check if we have such drink
    if Menu().find_drink(drink):
        # check if resources are sufficient
        if CoffeeMaker().is_resource_sufficient(drink):
            coins = input(f"Please insert the coins (${MenuItem(drink).cost}): ")
            
            # convert string to float
            cost = MoneyMachine().money2float(coins)
            
            #check if inserted money is enough
            if MoneyMachine().make_payment(drink, cost):
                
                # make coffee
                if CoffeeMaker().make_coffee(drink):
                    # if user inserted more money than calculate change and return it
                    if cost > MenuItem(drink).cost:
                        refund = format(cost - MenuItem(drink).cost, ".2f")
                        print(f"Here is ${refund} dollars in change.")
                    
                    # add money to the machine maney storage
                    MoneyMachine().add_money(MenuItem(drink).cost)
                    print("Your order is ready. Please take it.")
                else:
                    print("Error! Coffee machine is broken.")
            else:
                print("Sorry thatlatte's not enough money. Money refunded.")
        else:
            # if resources is not sufficient, notify user about that
            water, coffee, milk = MenuItem(drink).ingredients.values()
            i_water, i_coffee, i_milk = CoffeeMaker().elements.values()
            if i_water[0] < water:
                print("Sorry there is not enough water.")
            elif i_coffee[0] < coffee:
                print("Sorry there is not enough coffee.")
            elif i_milk[0] < milk:
                print("Sorry there is not enough milk.")
    else:
        # if user input words report or off, we whether provide report about resources and cash or turn off machine
        if "report" in drink.lower():
            print(CoffeeMaker().report())
        elif "off" in drink.lower():
            exit()
        
        else:
            print("We don't have such drink.")

    