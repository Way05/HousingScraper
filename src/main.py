from places4students import getData as ps4
from udstudentrentals import getData as udr
import pandas as pd

print("Welcome to housingScraper!")
school = input("What school? (please time exact name): ")
print("Which site would you like to search?")
print("1. UD Student Rentals")
print("2. Places4Students (UD only for now)")
print("3. All of the above")
print("4. Exit")
input = input("Enter a number: ")

data = None


def formatPrice(df):
    df["Price ($)"] = (
        df["Price ($)"]
        .map(lambda x: x.replace(",", "").rstrip("+").lstrip("$").strip())
        .astype(float)
    )
    df.sort_values(by=["Price ($)"], inplace=True)


match input:
    case "1":
        data = udr()
        df = pd.DataFrame(data)
        formatPrice(df)
        pass
    case "2":
        data = ps4()
        df = pd.DataFrame(data)
        formatPrice(df)
        pass
    case "3":
        pass
    case "4":
        print("Exiting...")

if df.empty:
    print("No results found.")
else:
    print(df)
