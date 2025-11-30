from places4students import getSchoolPage as p4s
from udstudentrentals import getData as udr
import pandas as pd
import os

run = True
dfs = []


os.system("cls")


def formatData(*raw_data):
    for data in raw_data:
        if data:
            df = pd.DataFrame(data)
            df["Price ($)"] = (
                df["Price ($)"]
                .map(lambda x: x.replace(",", "").rstrip("+").lstrip("$").strip())
                .astype(float)
            )
            df.sort_values(by=["Price ($)"], inplace=True, ignore_index=True)
            dfs.append(df)
    merged_df = pd.concat([*dfs], ignore_index=True)
    merged_df.dropna()
    return merged_df


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
            merged_df = formatData(data)
        case "2":
            print("Fetching data...")
            data = p4s(name)
            merged_df = formatData(data)
        case "3":
            print("Fetching data...")
            data1 = udr()
            data2 = p4s(name)
            merged_df = formatData(data1, data2)
        case _:
            print("Exiting...")
            return None
    print("Data fetched.")
    return merged_df


merged_df = fetchData()

while True and merged_df is not None:
    cmd = input(
        "Enter CMD: (D) Display, (E) Export, (F) Filter, (S) Sort, (Q) Quit\n"
    ).upper()
    match cmd:
        case "D":
            print(merged_df)
        case "E":
            if len(dfs) > 1:
                ask = input("(S) Separate or (T) together?: ").upper()
                print("Exporting...")
                if ask == "S":
                    count = 1
                    for df in dfs:
                        df.to_csv(f"out_0{count}.csv", index=False)
                        count += 1
                elif ask == "T":
                    merged_df.to_csv("merged_out.csv", index=False)
                else:
                    print("Invalid.")
            else:
                merged_df.to_csv("out_01.csv", index=False)
            print("Export complete.")
        case "F":
            filter_by = input(
                "What do you want to filter? (P) Price, (R) Rooms, (B) Bathrooms: "
            ).upper()
            match filter_by:
                case "P":
                    pass
                case "R":
                    pass
                case "B":
                    pass
                case _:
                    print("Invalid.")
        case "S":
            sort_by = input(
                "What do you want to sort? (P) Price, (R) Rooms, (B) Bathrooms: "
            )
            match sort_by:
                case "P":
                    order = input("(A) Ascending // (D) Descending: ").upper()
                    if order == "A":
                        merged_df.sort_values(
                            by=["Price ($)"], inplace=True, ignore_index=True
                        )
                    elif order == "D":
                        merged_df.sort_values(
                            by=["Price ($)"],
                            ascending=False,
                            inplace=True,
                            ignore_index=True,
                        )
                    else:
                        print("Invalid.")
                case "R":
                    pass
                case "B":
                    pass
                case _:
                    print("Invalid.")
        case "Q":
            print("Exiting...")
            break
        case _:
            print("Unrecognized Command, try again.")
