
import pandas as pd
import numpy as np
import time as time
import random
import string

def main():
    print("Starting debugSelf.py...")
    start_time = time.time()
    df = generate_fake_flight_reservations(200)
    end_time = time.time()
    print(df)
    print(f"Execution time: {end_time - start_time} seconds")
    save_dataframe_to_csv(df, 'data/flight_reservations.csv')
    print("DataFrame saved to data/flight_reservations.csv")

    

def save_dataframe_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Generate a DataFrame with fake flight reservation data via copilot
def generate_fake_flight_reservations(n):
    
    pnr_list = ["".join(random.choices(string.ascii_uppercase + string.digits, k=6)) for _ in range(n)]
    passenger_list = [f"Passenger_{i+1}" for i in range(n)]
    airports = ['JFK', 'LAX', 'ORD', 'DFW', 'DEN', 'ATL', 'SFO', 'SEA', 'MIA', 'BOS']
    origin_list = [random.choice(airports) for _ in range(n)]
    destination_list = [random.choice([a for a in airports if a != origin_list[i]]) for i in range(n)]
    fare_list = [round(random.uniform(100, 1500), 2) for _ in range(n)]
    status_list = [random.choice(['Confirmed', 'Cancelled', 'Pending']) for _ in range(n)]
    data = {
        'PNR': pnr_list,
        'Passenger': passenger_list,
        'Origin': origin_list,
        'Destination': destination_list,
        'Fare': fare_list,
        'Status': status_list
    }
    df = pd.DataFrame(data)
    df = introduce_invalid_airport_codes(df, percent=10)
    df = introduce_null_values(df, percent=10)
    df = introduce_duplicates(df, percent=10)
    return df

# Introduce data quality issues ----------------------------------------------------------------------------
def introduce_null_values(df, percent):
    """Randomly introduce null values into random cells of the DataFrame."""
    n = len(df)
    num_nulls = max(1, n * percent // 100)
    columns = df.columns.tolist()
    np.random.seed(123)
    for _ in range(num_nulls):
        idx = np.random.randint(0, n)
        col = random.choice(columns)
        df.at[idx, col] = None
    return df

def introduce_invalid_airport_codes(df, percent):
    """Randomly introduce invalid airport codes into Origin or Destination columns."""
    n = len(df)
    num_invalid = max(1, n * percent // 100)
    invalid_codes = ['XXX', 'ZZZ', '123', '!!@', 'NONE']
    invalid_indices = df.sample(n=num_invalid, random_state=99).index
    for idx in invalid_indices:
        col = random.choice(['Origin', 'Destination'])
        df.at[idx, col] = random.choice(invalid_codes)
    return df

def introduce_duplicates(df, percent=10):
    """Randomly duplicate a percentage of rows and append them to the DataFrame."""
    n = len(df)
    num_duplicates = max(1, n * percent // 100)
    duplicate_rows = df.sample(n=num_duplicates, random_state=42)
    df_with_duplicates = pd.concat([df, duplicate_rows], ignore_index=True)
    return df_with_duplicates
# ----------------------------------------------------------------------------------------------------------  

if __name__ == "__main__":
    main()