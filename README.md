# debugSelf.py Project

## Overview
This project benchmarks two methods (slow/for-loop and fast/vectorized) for cleaning synthetic flight reservation data using pandas DataFrames. It simulates real-world data quality issues and logs performance and memory usage for each method.

## Features
- Generates synthetic flight reservation data with:
  - Unique PNRs, passenger names, random US airport codes, fares, and statuses
  - Randomly introduced nulls, invalid airport codes, and duplicate rows
- Cleans data using two approaches:
  - Slow: for-loop based null removal
  - Fast: pandas vectorized dropna
- Drops duplicates before null removal in both modes
- Logs memory usage and execution time for each run
- Limits log files to the last 500 lines
- Prints average memory and execution time for both methods
- Error handling for missing columns and log file issues

## File Structure
- `debugSelf.py` — Main benchmarking script
- `doc/debugSelf_issues.md` — Documentation of issues, data assumptions, and error table
- `log/` — Log files for slow and fast runs
- `data/` — (Optional) For saving generated CSVs if needed

## How to Run
1. Ensure you have Python 3.x and the following packages:
   - pandas
   - numpy
2. Run the script:
   ```bash
   python debugSelf.py
   ```
3. Review printed output for average memory and execution time.
4. Check the `log/` directory for detailed logs.

## Data Assumptions
See the `doc/debugSelf_issues.md` for detailed data generation and corruption assumptions.

## Error Table
See the `doc/debugSelf_issues.md` for a table of errors introduced and their handling.

## Customization
- To change the number of runs, rows, or corruption percentages, edit the relevant values in `debugSelf.py`.
- To save generated data, use the `save_dataframe_to_csv` function.

## License
This project is for educational and benchmarking purposes.
