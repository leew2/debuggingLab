
import pandas as pd
import numpy as np

def main():
    print("Hello, world!")
    df = generate_random_dataframe(5, 3) # rows, cols
    lst = generate_random_list(10, 0, 100) # length, min, max
    print(lst)
    print(df)

def generate_random_list(length=10, min=0, max=100):
    lst = np.random.randint(min, max, size=length)
    return lst.tolist()

def generate_random_dataframe(rows, cols):
    data = np.random.randint(0, 100, size=(rows, cols))
    df = pd.DataFrame(data, columns=[f"data {i+1}" for i in range(cols)])
    return df

if __name__ == "__main__":
    main()