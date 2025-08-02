
import pandas as pd
import numpy as np

def main():
    loop = True
    while loop:
        print("0: Exit\n1: List\n2: DataFrame")
        choice = input("Enter your choice (0/1/2): ").strip()
        if choice == '0' or choice.lower() == 'exit' or choice.lower() == 'stop':
            print("Exiting the program.")
            break
        elif choice == '1' or choice.lower() == 'list':
            length = int(input("Enter list length (default 10): ") or 10)
            min_val = int(input("Enter min value (default 0): ") or 0)
            max_val = int(input("Enter max value (default 100): ") or 100)
            lst = generate_random_list(length, min_val, max_val)
            print("Random List:", lst)
        elif choice == '2' or choice.lower() == 'df':
            rows = int(input("Enter number of rows (default 5): ") or 5)
            cols = int(input("Enter number of columns (default 3): ") or 3)
            df = generate_random_dataframe(rows, cols)
            print("Random DataFrame:")
            print(df)
        else:
            print("Invalid input. Please choose one of the options.")

def generate_random_list(length=10, min=0, max=100):
    lst = np.random.randint(min, max, size=length)
    return lst.tolist()

def generate_random_dataframe(rows, cols):
    data = np.random.randint(0, 100, size=(rows, cols))
    df = pd.DataFrame(data, columns=[f"data {i+1}" for i in range(cols)])
    return df

if __name__ == "__main__":
    main()