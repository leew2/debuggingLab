# debugSelf.py Issues Documentation

## Overview
This document outlines known and potential issues, design decisions, and improvement opportunities for `debugSelf.py`, a benchmarking script for DataFrame cleaning methods (slow/for-loop vs fast/vectorized) on synthetic flight reservation data.

---

## Data Assumptions
The `fake_flight` function generates synthetic flight reservation data with the following assumptions:
  - Each reservation has a unique PNR (6-character alphanumeric string).
  - Passenger names are generated as 'Passenger_1', 'Passenger_2', ..., up to the number of rows requested.
  - Origin and Destination are randomly chosen from a fixed list of 10 major US airport codes, with Origin and Destination always different for a given row.
  - Fare is a random float between 100 and 1500 (rounded to 2 decimals).
  - Status is randomly assigned as 'Confirmed', 'Cancelled', or 'Pending'.
  - Data quality issues are introduced: 10% of rows have invalid airport codes, 10% have null values in random columns, and 10% of rows are duplicated.
  - The resulting DataFrame may contain missing, invalid, or duplicate data, simulating real-world data quality problems.

## Error Table
| Error Type         | Description                                                      | Root Cause                                                      | Solution/Handling                                    |
|--------------------|------------------------------------------------------------------|------------------------------------------------------------------|------------------------------------------------------|
| Null Values        | Some fields (Origin, Destination, Status, Passenger, PNR, etc.) are set to null in random rows. | Randomly introduced by `introduce_null_values` to simulate missing data. | Remove rows with nulls (slow: for-loop, fast: dropna). |
| Invalid Airport    | Origin or Destination contains invalid codes (e.g., 'XXX', '123'). | Randomly introduced by `introduce_invalid_airport_codes` to simulate data entry errors. | Validate airport codes or remove invalid rows.         |
| Duplicates         | Some rows are exact duplicates of others.                        | Randomly introduced by `introduce_duplicates` to simulate real-world duplication. | Use `drop_duplicates()` to remove duplicates.          |



## Known Issues

### 1. Performance (Slow Mode)
- The `remove_null` function uses a for-loop to iterate and drop rows, which is significantly slower than vectorized operations.
- For large DataFrames, this approach is not scalable and can lead to high execution times.

### 2. Memory Usage Calculation
- Memory usage is measured before and after null removal, but the difference may be small due to pandas' internal memory management and garbage collection.
- The memory difference may not always reflect the true reduction in memory usage after row removal.

### 3. Data Quality Simulation
- The script introduces nulls, invalid airport codes, and duplicates randomly. This randomness can make benchmarking results variable between runs unless random seeds are strictly controlled.
- The percentage of data corruption is hardcoded (10%).

### 4. Logging
- Logs are written to both in-memory lists and files. Each log file is now limited to the last 500 lines; older entries are trimmed automatically after each write.

### 5. Function Naming Consistency
- The function for generating fake data is named `fake_flight` in the latest version, but was previously `generate_fake_flight_reservations`. Consistency is important for maintainability.

### 6. Code Duplication
- The slow and fast benchmarking loops are nearly identical except for the cleaning method. This could be refactored to reduce duplication.

### 7. Error Handling
- Error handling for file I/O has been added: the script now attempts to create the log directory if it does not exist and prints an error message if writing to the log file fails.
- The script now checks for required DataFrame columns before cleaning; if columns are missing, it prints an error and skips the iteration.

### 8. Output Clarity
- The script prints average times and memory usage, but does not save summary statistics to a file for later analysis.
- The output does not include standard deviation or other statistical measures.

### 9. Hardcoded Parameters
- Number of runs (100), number of rows (200), and corruption percentages are hardcoded. Making these configurable would improve flexibility.

---

## Potential Improvements
- Refactor benchmarking loops into a single function with a cleaning method parameter.
- Add command-line arguments or config file for parameters (runs, rows, corruption %).
- Add error handling for file and DataFrame operations.
- Save summary statistics to a separate results file.
- Add more detailed logging (e.g., timestamp, run number).
- Make the log file line limit configurable (currently hardcoded to 500 lines).
- Consider using pandas' built-in memory profiling tools for more accurate memory usage.
- Add unit tests for helper functions.

---

## Summary
While the script fulfills its benchmarking purpose, addressing the above issues would improve performance, maintainability, and usability.
