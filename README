# Analysis of CICIDS2017 with ENN and Port Test

This project applies two quality assessment methods from the paper *Bad Design Smells in Benchmark NIDS Datasets* to the **CICIDS2017 dataset**:

1. **Edited Nearest Neighbour Rule (ENN)** – detects mislabeled or noisy samples by checking whether each instance agrees with its *k* nearest neighbors.  
2. **Port Test** – flags potential ambiguity in dataset labeling when benign traffic uses well-known background service ports (e.g., DNS 53, NTP 123).

---

## Results Summary

We evaluated all CSV files in CICIDS2017 using both methods.

### ENN Misclassification Rate
- Most large attack classes (e.g., **DDoS, PortScan, DoS Hulk, DoS GoldenEye, Patator**) had **very low misclassification rates (≈ 0%)**, suggesting that these classes are well-separated and labels are clean.
- Smaller attack classes (e.g., **Infiltration, Web Attacks**) showed **very high misclassification rates (50–70%)**, indicating possible label noise or overlapping traffic patterns.
- Examples:
  - *Web Attack – SQL Injection*: **71%** misrate  
  - *Infiltration*: **55%** misrate  
  - *Web Attack – XSS*: **50%** misrate  

### Port Test (UGT_C ratio)
- For **attack traffic**, UGT_C ≈ 0 across all classes. This makes sense since attacks target application ports rather than background services.  
- For **benign traffic**, UGT_C was consistently high (≈ 0.3–0.5), showing that a significant fraction of benign flows are on background service ports (e.g., DNS 53, NTP 123).  
- Examples:
  - *BENIGN (Friday DDoS)*: UGT_C = **0.34**  
  - *BENIGN (Monday traffic)*: UGT_C = **0.42**  
  - *BENIGN (Tuesday traffic)*: UGT_C = **0.46**  

---

## Interpretation

- **ENN** highlights *label noise and class overlap*.  
  - Some small attack categories are not reliably separated, which may affect classifier training.  
- **Port Test** highlights *design issues in dataset construction*.  
  - Benign traffic is partially ambiguous because it heavily relies on background services, which can also be abused in real attacks.  

Together, the two methods reveal **complementary dataset weaknesses**:
- Large, simple attack classes (e.g., DDoS) are clean.  
- Smaller, complex attacks (e.g., SQL Injection, Infiltration) show labeling ambiguity.  
- Benign traffic shows systematic ambiguity due to background service ports.  

---

## Next Steps

- Extend analysis to other IDS datasets (e.g., Bot-IoT, AWID3) for comparison.  
- Visualize ENN vs. Port Test results with more plots.  
