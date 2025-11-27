from places4students import getSchoolPage as p4s
from udstudentrentals import getData as udr
import pandas as pd
import os
import platform

run = True
dfs = []

os.system("cls")


def formatData(*raw_data):
    for data in raw_data:
        df = pd.DataFrame(data)
        df["Price ($)"] = (
            df["Price ($)"]
            .map(lambda x: x.replace(",", "").rstrip("+").lstrip("$").strip())
            .astype(float)
        )
        df.sort_values(by=["Price ($)"], inplace=True, ignore_index=True)
        dfs.append(df)


def fetchData():
    print("Welcome to housingScraper!")
    # name = input("What school?: ")
    name = "ud"
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
            formatData(data)
        case "2":
            print("Fetching data...")
            data = p4s(name)
            formatData(data)
        case "3":
            print("Fetching data...")
            data1 = udr()
            data2 = p4s(name)
            formatData(data1, data2)
        case "4":
            print("Exiting...")
            return False
    print("Data fetched.")
    return True


run = fetchData()

while True and run:
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
