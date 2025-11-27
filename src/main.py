from places4students import getSchoolPage as p4s
from udstudentrentals import getData as udr
import pandas as pd

print("Welcome to housingScraper!")
print("Which site would you like to search?")
print("1. UD Student Rentals")
print("2. Places4Students")
print("3. All of the above")
print("4. Exit")
choice = input("Enter a number: ")

data = None
dfs = []


def formatPrice(df):
    df["Price ($)"] = (
        df["Price ($)"]
        .map(lambda x: x.replace(",", "").rstrip("+").lstrip("$").strip())
        .astype(float)
    )
    df.sort_values(by=["Price ($)"], inplace=True)


def fetchData():
    match choice:
        case "1":
            data = udr()
            df = pd.DataFrame(data)
            formatPrice(df)
            dfs.append(df)
        case "2":
            data = p4s()
            df = pd.DataFrame(data)
            formatPrice(df)
            dfs.append(df)
        case "3":
            data1 = udr()
            df1 = pd.DataFrame(data1)
            data2 = p4s()
            df2 = pd.DataFrame(data2)
            formatPrice(df1)
            formatPrice(df2)
            dfs.append(df1)
            dfs.append(df2)
        case "4":
            print("Exiting...")


while True:
    cmd = input(
        "Enter CMD: (D) Display, (E) Export, (F) Filter, (S) Sort, (Q) Quit"
    ).upper()
    match cmd:
        case "D":
            if dfs is None:
                print("No results found.")
            else:
                for df in dfs:
                    print(df)
        case "E":
            pass
        case "F":
            pass
        case "S":
            pass
        case "Q":
            break
        case _:
            print("Unrecognized Command, try again.")
