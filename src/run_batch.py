import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.run import run

def run_batch(dataset_folder, dataset_name=None, out_dir="results", k_values=[3,5,7]):
    """
    Runs ENN + PortTest on all CSVs in a folder.
    Saves a summary CSV + plots named after the dataset.
    """
    os.makedirs(out_dir, exist_ok=True)
    plots_dir = os.path.join(out_dir, "plots", dataset_name if dataset_name else "dataset")
    os.makedirs(plots_dir, exist_ok=True)

    if dataset_name is None:
        dataset_name = os.path.basename(dataset_folder.strip("/"))

    results = []

    for file in os.listdir(dataset_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(dataset_folder, file)
            try:
                df_result = run(file_path, k_values=k_values)
                results.append(df_result)
            except Exception as e:
                print(f" Skipping {file} due to error: {e}")

    # Save combined summary
    summary_df = pd.concat(results, ignore_index=True)
    out_file = os.path.join(out_dir, f"{dataset_name}_ENN_PortTest_Summary.csv")
    summary_df.to_csv(out_file, index=False, encoding="utf-8")
    print(f"\n Saved summary for {dataset_name} → {out_file}")


    # 1) Heatmap of ENN misrates
    enn_df = summary_df[summary_df["Method"].str.contains("ENN")]
    if not enn_df.empty:
        pivot_df = enn_df.pivot(index="Class", columns="File", values="Value")
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_df, annot=True, fmt=".3f", cmap="Reds", cbar_kws={'label': 'ENN misrate'})
        plt.title(f"{dataset_name} - ENN Misclassification Rates")
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()
        heatmap_file = os.path.join(plots_dir, f"{dataset_name}_ENN_heatmap.png")
        plt.savefig(heatmap_file, dpi=300)
        plt.close()
        print(f" Saved ENN heatmap  {heatmap_file}")

    # 2) Barplot of PortTest results
    port_df = summary_df[summary_df["Method"] == "PortTest"]
    if not port_df.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=port_df, x="Class", y="Value", hue="File", dodge=True)
        plt.title(f"{dataset_name} - PortTest UGT_C Ratios")
        plt.ylabel("UGT_C (unclear traffic ratio)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        portplot_file = os.path.join(plots_dir, f"{dataset_name}_PortTest_barplot.png")
        plt.savefig(portplot_file, dpi=300)
        plt.close()
        print(f"Saved PortTest barplot  {portplot_file}")

    return summary_df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run ENN + PortTest on all CSVs in a dataset folder")
    parser.add_argument("--folder", type=str, required=True, help="Path to dataset folder with CSVs")
    parser.add_argument("--out", type=str, default="results", help="Output folder for summaries/plots")
    parser.add_argument("--k", type=int, nargs="+", default=[3,5,7], help="Values of k for ENN")
    parser.add_argument("--name", type=str, default=None, help="Dataset name for summary file/plots")
    args = parser.parse_args()

    run_batch(args.folder, dataset_name=args.name, out_dir=args.out, k_values=args.k)
