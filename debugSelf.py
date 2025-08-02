def main():
    print("Hello, world!")
    df = generate_random_dataframe()
    print(df)

def generate_random_dataframe(rows=5, cols=3):
    import pandas as pd
    import numpy as np
    data = np.random.randint(0, 100, size=(rows, cols))
    df = pd.DataFrame(data, columns=[f"data {i+1}" for i in range(cols)])
    return df

if __name__ == "__main__":
    main()