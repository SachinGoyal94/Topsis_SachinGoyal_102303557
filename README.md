# TOPSIS Implementation (Sachin Goyal)

Simple TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) implementation in Python.

Project structure
- data.csv                 (example input)
- setup.py                 (packaging / install - optional)
- topsis/                  (package)
  - __init__.py
  - topsis.py              (main implementation and CLI)

Summary
- Reads a CSV where the first column is an identifier (name) and the remaining columns are numeric criteria.
- Computes TOPSIS scores and ranks using provided weights and impacts.
- Writes an output CSV that includes the original data plus `Topsis Score` and `Rank` columns.

Prerequisites
- Python 3.6+
- pandas and numpy

Quick install (no virtualenv):

Open a terminal and run:

    python -m pip install pandas numpy

Or create a virtual environment first, then install the same packages.

Usage

There are two simple ways to run the script.

1) Run as a module (from project root):

    python -m topsis.topsis <InputFile> "<Weights>" "<Impacts>" <OutputFile>

2) Run the script file directly:

    python topsis\topsis.py <InputFile> "<Weights>" "<Impacts>" <OutputFile>

Arguments
- <InputFile>: path to the input CSV file.
- <Weights>: comma-separated numeric weights for each criterion (e.g. "1,1,1,1").
- <Impacts>: comma-separated + or - for each criterion (e.g. "+,+,-, +").
- <OutputFile>: path for the output CSV.

Input CSV format
- Must have at least 3 columns (first column: identifier; at least two criteria columns).
- All columns from the 2nd to last must contain numeric values.
- Example:

    Name,Cost,Performance,Reliability
    A,250,8,9
    B,200,7,8

Example

    python -m topsis.topsis data.csv "1,1,1" "+,+,-" result.csv

This will produce `result.csv` with two extra columns:
- `Topsis Score` (higher is better)
- `Rank` (1 = best)

Common errors and messages
- "Input file not found": the specified input file path doesn't exist.
- "Unable to read input file": input file not a valid CSV.
- "Input file must contain at least 3 columns": CSV missing required columns.
- "All columns from 2nd to last must contain numeric values": non-numeric values in criteria columns.
- "Number of weights must be equal to number of criteria": mismatch between provided weights and criteria count.
- "Number of impacts must be equal to number of criteria": mismatch between provided impacts and criteria count.
- "Impacts must be either + or -": impacts should be "+" or "-" only.
- "Weights must be numeric": weights should be numbers.

Notes
- Weights are normalized implicitly by the algorithm's normalization step.
- The implementation uses Euclidean normalization.

Author
- Sachin Goyal (student project)

License
- Use or adapt as needed for learning or coursework.
