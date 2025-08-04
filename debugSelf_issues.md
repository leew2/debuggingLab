# debugSelf.py Issues Documentation

## Overview
This document outlines known and potential issues, design decisions, and improvement opportunities for `debugSelf.py`, a benchmarking script for DataFrame cleaning methods (slow/for-loop vs fast/vectorized) on synthetic flight reservation data.

---

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
- Logs are written to both in-memory lists and files, but there is no log rotation or size management.
- If the script is run many times, log files may grow large.

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
- Consider using pandas' built-in memory profiling tools for more accurate memory usage.
- Add unit tests for helper functions.

---

## Summary
While the script fulfills its benchmarking purpose, addressing the above issues would improve performance, maintainability, and usability.
