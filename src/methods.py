import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier

# Data Preprocessing
def load_and_preprocess(file_path, label_col="Label"):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    if label_col not in df.columns:
        raise ValueError(f"Label column '{label_col}' not found in {file_path}")

    X = df.drop(label_col, axis=1, errors="ignore")
    y = df[label_col].values

    # Convert to numeric
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    # Normalize
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, df

# ENN Test
def enn_test(X, y, k=5):
    """
    Edited Nearest Neighbour (ENN) test using k-NN classifier.
    Returns: y_pred, misclassified_mask, misclassification_rate
    """
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X, y)
    y_pred = knn.predict(X)

    misclassified = (y_pred != y)
    mis_rate = np.mean(misclassified)

    return y_pred, misclassified, mis_rate


# Port Test
BG_PORTS = {0, 53, 67, 68, 111, 123, 137, 161, 179, 389, 427, 520, 1723, 1900}

def port_test(df, label_col="Label", port_col="Destination Port"):
    """
    Port Test: checks for flows using background ports and computes UGT_C per class.
    Returns dict: {class: ratio of unclear flows}
    """
    results = {}
    for cls, group in df.groupby(label_col):
        total = len(group)
        unclear = group[group[port_col].isin(BG_PORTS)]
        results[cls] = len(unclear) / total if total > 0 else 0
    return results
