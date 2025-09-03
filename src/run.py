import os
import pandas as pd
from methods import load_and_preprocess, enn_test, port_test

def run(file_path, k_values=[5], label_col="Label", port_col="Destination Port"):
    """
    Runs ENN and Port Test on a dataset file.
    Returns a DataFrame with results.
    """
    print(f"Processing {file_path} ...")
    X_scaled, y, df = load_and_preprocess(file_path, label_col)

    results = []
    for k in k_values:
        y_pred, mis_mask, mis_rate = enn_test(X_scaled, y, k)
        per_class = {}
        for cls in pd.unique(y):
            idx = (y == cls)
            if sum(idx) > 0:
                per_class[cls] = (y_pred[idx] != y[idx]).mean()

        for cls, rate in per_class.items():
            results.append({
                "File": os.path.basename(file_path),
                "Class": cls,
                "Method": f"ENN_k={k}",
                "Value": rate
            })

    # Port Test
    port_results = port_test(df, label_col, port_col)
    for cls, val in port_results.items():
        results.append({
            "File": os.path.basename(file_path),
            "Class": cls,
            "Method": "PortTest",
            "Value": val
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run ENN + PortTest experiments on dataset")
    parser.add_argument("--file", type=str, required=True, help="Path to dataset CSV file")
    parser.add_argument("--out", type=str, default="results.csv", help="Path to save results CSV")
    parser.add_argument("--k", type=int, nargs="+", default=[3, 5, 7], help="Values of k for ENN")
    args = parser.parse_args()

    df_results = run(args.file, k_values=args.k)
    df_results.to_csv(args.out, index=False)

