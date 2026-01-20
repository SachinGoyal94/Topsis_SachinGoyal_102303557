import sys
import os
import pandas as pd
import numpy as np

def error(msg):
    print("Error:", msg)
    sys.exit(1)

def topsis(input_file, weights, impacts, output_file):

    if not os.path.isfile(input_file):
        error("Input file not found")

    try:
        df = pd.read_csv(input_file)
    except:
        error("Unable to read input file")

    if df.shape[1] < 3:
        error("Input file must contain at least 3 columns")

    data = df.iloc[:, 1:]

    if not np.all(data.applymap(np.isreal)):
        error("All columns from 2nd to last must contain numeric values")

    weights = weights.split(',')
    impacts = impacts.split(',')

    if len(weights) != data.shape[1]:
        error("Number of weights must be equal to number of criteria")

    if len(impacts) != data.shape[1]:
        error("Number of impacts must be equal to number of criteria")

    for i in impacts:
        if i not in ['+', '-']:
            error("Impacts must be either + or -")

    try:
        weights = np.array(weights, dtype=float)
    except:
        error("Weights must be numeric")

    norm = data / np.sqrt((data ** 2).sum())

    weighted = norm * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False)

    df.to_csv(output_file, index=False)
    print("TOPSIS analysis completed successfully!")

def main():
    if len(sys.argv) != 5:
        error("Usage: topsis <InputFile> <Weights> <Impacts> <OutputFile>")

    topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
    main()
