import csv
from datetime import datetime
import os

from good import Good
from table import print_table

goods: list[Good] = []
cart: dict[Good, int] = {}

def prompt_loop():
    yield "list"
    print("Type '?' for help")
    while True:
        cmd = input("\n> ")
        yield cmd


def main():
    # Open the CSV file and parse it into a list of Good objects
    with open("goods.csv", "r") as file:
        reader = csv.DictReader(file)
        global goods; goods = [Good(**row) for row in reader]
    
    # Prompt loop
    for cmd in prompt_loop():
        try:
            match cmd:
                # List all the goods
                case "list":
                    title = ["Number", "Name", "Price ($)", "Fat (kcal)"]
                    rows = tuple(map(lambda x: [goods.index(x), x.name, x.price, x.fat], goods))
                    print_table(title, rows)

                # List the goods in the cart
                case "cart":
                    title = ["Number", "Name", "Price ($)", "Fat (kcal)", "Quantity", "Total Price ($)", "Total Fat (kcal)"]
                    rows = list(map(lambda x: [goods.index(x), x.name, x.price, x.fat, cart[x], x.price * cart[x], x.fat * cart[x]], cart))
                    rows.append(["", "", "", "", "", "", ""])
                    rows.append(["", "Total", "", "", sum(cart.values()), sum(x.price * cart[x] for x in cart), sum(x.fat * cart[x] for x in cart)])
                    print_table(title, rows)
                
                # Add a good to the cart
                case "add":
                    good = goods[int(input("Enter the number of the good: "))]
                    quantity = int(input("Enter the quantity: "))
                    if quantity > 0:
                        cart[good] = cart.get(good, 0) + quantity
                
                # Remove a good from the cart
                case "remove":
                    good = goods[int(input("Enter the number of the good: "))]
                    quantity = int(input("Enter the quantity: "))
                    cart[good] -= quantity
                    if cart[good] <= 0:
                        del cart[good]
                
                # Save the cart to a CSV file
                case "save":
                    os.makedirs("saves", exist_ok=True)
                    time_str = datetime.now().strftime("%Y%m%d_%H%M%S_")
                    filename = time_str + input("Enter the filename: ")
                    with open(f"saves/{filename}.csv", "w") as file:
                        writer = csv.writer(file)
                        writer.writerow(["Name", "Price ($)", "Fat (kcal)", "Quantity"])
                        for good, quantity in cart.items():
                            writer.writerow([good.name, good.price, good.fat, quantity])
                
                # Help
                case "?":
                    print_table(
                        ["Command", "Description"],
                        [
                            ["list", "List all the goods"],
                            ["cart", "List the goods in the cart"],
                            ["add", "Add a good to the cart"],
                            ["remove", "Remove a good from the cart"],
                            ["save", "Save the cart to a CSV file"],
                            ["exit", "Exit the program"],
                            ["?", "Show this help message"],
                        ]
                    )
                
                # Exit the program
                case "exit":
                    break
                    
                # Invalid command
                case _:
                    print("Type '?' for help")
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as e:
            print(f"{e}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        pass
