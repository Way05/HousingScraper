from places4students import getSchoolPage as p4s
from udstudentrentals import getData as udr
import pandas as pd

data = None
dfs = []


def formatPrice(df):
    df["Price ($)"] = (
        df["Price ($)"]
        .map(lambda x: x.replace(",", "").rstrip("+").lstrip("$").strip())
        .astype(float)
    )
    df.sort_values(by=["Price ($)"], inplace=True, ignore_index=True)
    # df.reset_index(drop=True)


def fetchData():
    print("Welcome to housingScraper!")
    name = input("What school?: ")
    print("Which site would you like to search?")
    print("1. UD Student Rentals")
    print("2. Places4Students")
    print("3. All of the above")
    print("4. Exit")
    choice = input("Enter a number: ")
    match choice:
        case "1":
            print("Fetching data...")
            data = udr()
            df = pd.DataFrame(data)
            formatPrice(df)
            dfs.append(df)
        case "2":
            print("Fetching data...")
            data = p4s(name)
            df = pd.DataFrame(data)
            formatPrice(df)
            dfs.append(df)
        case "3":
            print("Fetching data...")
            data1 = udr()
            df1 = pd.DataFrame(data1)
            data2 = p4s(name)
            df2 = pd.DataFrame(data2)
            formatPrice(df1)
            formatPrice(df2)
            dfs.append(df1)
            dfs.append(df2)
        case "4":
            print("Exiting...")


fetchData()
print("Data fetched.")

while True:
    cmd = input(
        "Enter CMD: (D) Display, (E) Export, (F) Filter, (S) Sort, (Q) Quit\n"
    ).upper()
    match cmd:
        case "D":
            if dfs is None:
                print("No results found.")
            else:
                for df in dfs:
                    print(df)
        case "E":
            print("Exporting...")
            count = 1
            for df in dfs:
                df.to_csv(f"out_0{count}.csv", index=False)
                count += 1
            print("Export complete.")
        case "F":
            pass
        case "S":
            pass
        case "Q":
            print("Exiting...")
            break
        case _:
            print("Unrecognized Command, try again.")
