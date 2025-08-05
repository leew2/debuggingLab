import os
import random
import re
import string
import time
import numpy as np
import pandas as pd

fast_logs = []
slow_logs = []

def main():
    print("Starting debugSelf.py...")

    # Run slow mode 100 times
    required_columns = ["Origin", "Destination", "Status", "Passenger", "PNR"]
    for i in range(100):
        start_time = time.time()
        df = fake_flight(200)
        start_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
        # Check for required columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"[ERROR] Missing columns in DataFrame: {missing_cols}. Skipping iteration {i+1} (slow mode).")
            continue
        # Optionally comment out the next line to avoid printing all data
        print_dataframe(df) # prints the data to show differences in time differences
        df = df.drop_duplicates()  # Drop duplicates before removing nulls
        df = fill_missing_integers_with_mean(df)
        df = remove_null(df)
        end_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
        end_time = time.time()
        log_run("slow", start_memory, end_memory, start_time, end_time)
    
    # Run fast mode 100 times
    for i in range(100):
        start_time = time.time()
        df = fake_flight(200)
        start_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
        # Check for required columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"[ERROR] Missing columns in DataFrame: {missing_cols}. Skipping iteration {i+1} (fast mode).")
            continue
        # Optionally comment out the next line to avoid printing all data
        print(df) # prints the data to show differences in time differences
        df = df.drop_duplicates()  # Drop duplicates before removing nulls
        df = fill_missing_integers_with_mean(df)
        df = df.dropna(subset=required_columns)
        end_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
        end_time = time.time()
        log_run("fast", start_memory, end_memory, start_time, end_time)

    metrics()

# End of main function ------------------------------------------------

def metrics():   
    slow_times = extract_time(slow_logs)
    fast_times = extract_time(fast_logs)
    slow_memory = extract_memory(slow_logs)
    fast_memory = extract_memory(fast_logs)
    if slow_memory:
        print(f"Average slow memory usage: {sum(slow_memory)/len(slow_memory):.4f} MB")
    if fast_memory:
        print(f"Average fast memory usage: {sum(fast_memory)/len(fast_memory):.4f} MB")
    if slow_times:
        print(f"Average slow execution time: {sum(slow_times)/len(slow_times):.4f} seconds")
    if fast_times:
        print(f"Average fast execution time: {sum(fast_times)/len(fast_times):.4f} seconds")
    if slow_times and fast_times:
        print(f"Slow is {sum(slow_times)/len(slow_times) / (sum(fast_times)/len(fast_times)):.2f} times slower than fast")


def extract_time(log_list):
    times = []
    for entry in log_list:
        match = re.search(r"Execution time: ([\d.]+) seconds", entry)
        if match:
            times.append(float(match.group(1)))
    return times


def extract_memory(log_list):
    memory_usage = []
    for entry in log_list:
        match = re.search(r"Difference: ([\d.]+) MB", entry)
        if match:
            memory_usage.append(float(match.group(1)))
    return memory_usage


def log_run(label, start_memory, end_memory, start_time, end_time):
    """Log the run to the appropriate log file in the log folder."""
    import os
    log_file = f"log/{label}_log.txt"
    log_entry = (f"Memory usage before removing nulls: {start_memory:.4f} MB\n"
                 f"Memory usage after removing nulls: {end_memory:.4f} MB\n"
                 f"Difference: {start_memory - end_memory:.4f} MB\n"
                 f"Execution time: {end_time - start_time} seconds\n")
    if label == "fast":
        fast_logs.append(log_entry)
    elif label == "slow":
        slow_logs.append(log_entry)
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        # Append the new log entry
        with open(log_file, "a") as f:
            f.write(log_entry)
        # Limit the log file to the last 500 lines
        with open(log_file, "r") as f:
            lines = f.readlines()
        if len(lines) > 500:
            with open(log_file, "w") as f:
                f.writelines(lines[-500:])
    except Exception as e:
        print(f"[ERROR] Could not write to log file {log_file}: {e}")

# end of metric related functions ------------------------------------------------

# printing dataframe via loop(slow)
def print_dataframe(df):
    """Print Passenger, Origin, Destination, Fare, and Status for each row using a for loop, spaced evenly."""
    header = f"{'Passenger':<15} {'Origin':<10} {'Destination':<15} {'Fare':>10} {'Status':<12}"
    print(header)
    print('-' * len(header))
    for idx, row in df.iterrows():
        print(f"{str(row.get('Passenger', '')):<15} {str(row.get('Origin', '')):<10} {str(row.get('Destination', '')):<15} {str(row.get('Fare', '')):>10} {str(row.get('Status', '')):<12}")


# removing null values via loop("slow")
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


# ----------------------------------------------------------------------------
# Generate a DataFrame with fake flight reservation data via copilot
# "Create 200 fake flight reservations with fields: PNR, Passenger, Origin, Destination, Fare, Status"
def fake_flight(n):
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