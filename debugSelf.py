
import pandas as pd
import numpy as np
import time as time
import random
import string

log_lines = []

def main():
    print("Starting debugSelf.py...")
    
    while True:
        df = generate_fake_flight_reservations(200) # remakes dataframe each loop for fresh data
        option = input("Choose mode: (0)'stop', (1)'slow', or (2)'fast': ").strip().lower()
        
        if option == 'stop' or option == '0':
            print("Program stopped by user.")
            break
        elif option == 'slow' or option == '1':
            start_time = time.time()
            df = generate_fake_flight_reservations(200)
            start_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
            print_dataframe(df)  # "slower" method
            df = remove_null(df) # "slower" method
            end_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
            end_time = time.time()
            log_lines.append(f"Execution time: {end_time - start_time} seconds\n")
            print("\n".join(log_lines))
            log_run("slow", start_memory, end_memory, start_time, end_time)

        elif option == 'fast' or option == '2':
            start_time = time.time()
            start_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
            print(df) # "faster" method
            df = df.dropna(subset=["Origin", "Destination", "Status", "Passenger", "PNR"])  # "faster" method
            end_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
            end_time = time.time()
            log_lines.append(f"Execution time: {end_time - start_time} seconds\n")
            print("\n".join(log_lines))
            log_run("fast", start_memory, end_memory, start_time, end_time)
        else:
            print("Invalid option. Please enter '0', '1', '2', 'stop', 'slow', or 'fast'.")

def log_run(label, start_memory, end_memory, start_time, end_time):
    """Log the run to the appropriate log file in the log folder."""
    log_file = f"log/{label}_log.txt"
    with open(log_file, "a") as f:
        f.write(f"Memory usage before removing nulls: {start_memory:.4f} MB\n"
                 f"Memory usage after removing nulls: {end_memory:.4f} MB\n"
                 f"Difference: {start_memory - end_memory:.4f} MB\n"
                 f"Execution time: {end_time - start_time} seconds\n")



# printing dataframe via loop
def print_dataframe(df):
    """Print Passenger, Origin, Destination, Fare, and Status for each row using a for loop, spaced evenly."""
    header = f"{'Passenger':<15} {'Origin':<10} {'Destination':<15} {'Fare':>10} {'Status':<12}"
    print(header)
    print('-' * len(header))
    for idx, row in df.iterrows():
        print(f"{str(row.get('Passenger', '')):<15} {str(row.get('Origin', '')):<10} {str(row.get('Destination', '')):<15} {str(row.get('Fare', '')):>10} {str(row.get('Status', '')):<12}")

# removing null values via loop
def remove_null(df):
    """Remove rows with missing Origin, Destination, Status, Passenger, or PNR using a for loop."""
    indices_to_drop = []
    for idx, row in df.iterrows():
        if (
            pd.isnull(row["Origin"]) or
            pd.isnull(row["Destination"]) or
            pd.isnull(row["Status"]) or
            pd.isnull(row["Passenger"]) or
            pd.isnull(row["PNR"])
        ):
            indices_to_drop.append(idx)

    for drop_idx in indices_to_drop:
        df = df.drop(drop_idx)
    return df

def fill_missing_integers_with_mean(df):
    """Fill missing values in integer columns with the mean (rounded to int)."""
    int_cols = df.select_dtypes(include=[np.integer, 'Int64']).columns
    for col in int_cols:
        if df[col].isnull().any():
            mean_val = int(round(df[col].mean()))
            df[col] = df[col].fillna(mean_val)
    return df


def save_dataframe_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Generate a DataFrame with fake flight reservation data via copilot
# "Create 200 fake flight reservations with fields: PNR, Passenger, Origin, Destination, Fare, Status"
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

def introduce_duplicates(df, percent):
    """Randomly duplicate a percentage of rows and append them to the DataFrame."""
    n = len(df)
    num_duplicates = max(1, n * percent // 100)
    duplicate_rows = df.sample(n=num_duplicates, random_state=42)
    df_with_duplicates = pd.concat([df, duplicate_rows], ignore_index=True)
    return df_with_duplicates
# ----------------------------------------------------------------------------------------------------------  

if __name__ == "__main__":
    main()