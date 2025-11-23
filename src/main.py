from places4students import getData as ps4
from udstudentrentals import getData as udr
import pandas as pd

print("Welcome to housingScraper!")
print("Which site would you like to search?")
print("1. UD Student Rentals")
print("2. Places4Students (UD only for now)")
print("3. All of the above")
print("4. Exit")
input = input("Enter a number: ")

data = None

match input:
    case "1":
        data = udr()
        pass
    case "2":
        data = ps4()
        pass
    case "3":
        pass
    case "4":
        print("Exiting...")

df = pd.DataFrame(data)
print(df)
