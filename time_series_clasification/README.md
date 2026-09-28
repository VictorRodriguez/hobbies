# From Intel PCM Time Series to PID-Level Ransomware Candidate Detection

## A practical introduction to window characterization, frequency-domain features, and PCA

This tutorial explains a practical way to turn **per-PID microarchitectural telemetry** into features that can be used for workload characterization and, later, ransomware-candidate detection.

The goal is not to declare that a process *is* ransomware from PMU data alone. The goal is to continuously monitor processes and identify **candidate PIDs whose microarchitectural behavior deserves further inspection**.

The accompanying figures were generated from **synthetic educational data**. They illustrate the methodology only; they are not measured ransomware signatures.

---

## 1. Overall idea

For each active PID, Intel PCM or another PMU collection mechanism provides repeated measurements such as:

\[
\mathbf{x}_p(t)=
[CPI(t),\ IPC(t),\ LLCMPKI(t),\ BranchMPKI(t),\ldots].
\]

Instead of waiting until the process finishes, execution is divided into short observation windows:

\[
W_{p,k}=\{\mathbf{x}_p(t_k),\mathbf{x}_p(t_k+1),\ldots,\mathbf{x}_p(t_k+N-1)\}.
\]

Each window is treated as a **small workload instance** and converted into a fixed-length feature vector.

```text
PID
 |
 v
PCM / PMU samples
 |
 v
Short time windows
 |
 +----------------------+
 |                      |
 v                      v
Time-domain         Frequency-domain
features            features
 |                      |
 +----------+-----------+
            |
            v
       Hybrid features
            |
            v
      Standardization
            |
            v
            PCA
            |
            v
        PC1 vs PC2
```

---

## 2. Raw per-PID time series

The first step is simply to look at the raw telemetry over time.

### CPI over time

![Synthetic CPI time series](pcm_demo_output/01_raw_cpi_timeseries.png)

This figure shows several synthetic process classes. The important point is that a workload is no longer represented by a single CPI value. It produces a **CPI trajectory over time**.

### LLC MPKI over time

![Synthetic LLC MPKI time series](pcm_demo_output/02_raw_llc_mpki_timeseries.png)

The same applies to cache behavior. Each process may exhibit a different average level, variability, burstiness, or periodicity.

The classification problem therefore becomes:

> Can short segments of these signals be characterized well enough to separate different workload behaviors?

---

## 3. Why use time windows?

Suppose the sampling rate is \(f_s\) samples/s and we use a window of duration \(T_w\). The number of samples in one window is:

\[
N=f_sT_w.
\]

For example, if:

\[
f_s=20\ \text{samples/s},\qquad T_w=5\ \text{s},
\]

then:

\[
N=100\ \text{samples/window}.
\]

The detector can characterize every 5-second interval independently rather than waiting for the complete process lifetime.

### Example window

![Single CPI window](pcm_demo_output/03_single_window_mean.png)

The dashed line is the mean CPI of the window.

---

## 4. Time-domain characterization: mean + standard deviation

For a PMU metric \(x\), the mean is:

\[
\mu_x=\frac{1}{N}\sum_{i=1}^{N}x_i.
\]

The standard deviation is:

\[
\sigma_x=
\sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i-\mu_x)^2}.
\]

The mean tells us the typical value during the window. The standard deviation tells us how much that metric varied.

For each metric, the first baseline representation is therefore:

\[
[\mu_x,\sigma_x].
\]

For several PMU metrics:

\[
\mathbf{f}_{time}=
[\mu_{CPI},\sigma_{CPI},
\mu_{IPC},\sigma_{IPC},
\mu_{LLCMPKI},\sigma_{LLCMPKI},
\mu_{BranchMPKI},\sigma_{BranchMPKI},\ldots].
\]

---

## 5. Why mean and standard deviation may still be insufficient

Two windows may have similar statistical summaries but very different temporal organization.

![Similar statistics, different temporal structure](pcm_demo_output/04_similar_stats_different_structure.png)

One signal in the figure is periodic, while the other is noisy. Their means and standard deviations can be similar, but one clearly contains a repetitive structure.

This is exactly where the **frequency domain** becomes useful.

---

## 6. Frequency-domain characterization

For sampled values:

\[
x[0],x[1],\ldots,x[N-1],
\]

the Discrete Fourier Transform is:

\[
X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}.
\]

The FFT is simply an efficient algorithm for computing this transform.

A simple power spectrum is:

\[
P[k]=|X[k]|^2.
\]

Before the FFT, it is usually useful to subtract the mean:

\[
x_c[n]=x[n]-\mu_x.
\]

This removes the DC component and makes the spectrum emphasize **variation around the mean**.

### Same statistics, different spectra

![FFT comparison](pcm_demo_output/05_fft_periodic_vs_noise.png)

The periodic signal contains a strong spectral peak. The noisy signal spreads its energy across many frequencies.

This demonstrates why FFT-derived features may add information that \(\mu\) and \(\sigma\) alone cannot capture.

---

## 7. Example CPI power spectra

![CPI power spectra](pcm_demo_output/06_cpi_power_spectra.png)

Different synthetic workload classes exhibit different distributions of spectral energy.

The goal is not necessarily to feed the complete spectrum into the classifier. Instead, useful spectral descriptors can be extracted.

### Peak frequency

\[
f_{peak}=\underset{f>0}{\operatorname{argmax}}\ P(f).
\]

### Peak power

\[
P_{peak}=\max_{f>0}P(f).
\]

### Total spectral energy

\[
E=\sum_{f>0}P(f).
\]

### Spectral entropy

Normalize the power values:

\[
p_k=\frac{P[k]}{\sum_jP[j]}.
\]

Then:

\[
H_s=-\sum_k p_k\log_2 p_k.
\]

Low spectral entropy means energy is concentrated in a few frequencies. Higher entropy means the spectrum is more distributed.

---

## 8. Sampling rate and window duration matter

If the sampling rate is \(f_s\), the Nyquist frequency is:

\[
f_{Nyquist}=\frac{f_s}{2}.
\]

The approximate frequency resolution is:

\[
\Delta f=\frac{f_s}{N}=\frac{1}{T_w}.
\]

This leads to an important design tradeoff:

- Increasing **sampling rate** increases the maximum frequency that can be observed.
- Increasing **window duration** improves frequency resolution.
- Short windows reduce detection latency but provide less spectral information.

A 5-second window sampled only once per second contains only five points, which is usually too little for meaningful spectral analysis. Frequency-domain experiments therefore need a sufficiently high sampling cadence.

---

## 9. Three feature representations to compare

A clean experiment should compare three feature sets.

### A. Time-domain features

\[
F_{time}=[\mu,\sigma].
\]

### B. Frequency-domain features

\[
F_{freq}=[f_{peak},P_{peak},E,H_s].
\]

### C. Hybrid features

\[
\boxed{F_{hybrid}=[F_{time},F_{freq}]}
\]

This creates a direct research question:

> Does adding spectral information improve the separation of workload classes beyond conventional PMU statistics?

---

## 10. Standardization before PCA

The extracted features have very different units and ranges. CPI, MPKI, spectral energy, and entropy should not be directly compared numerically.

Each feature should therefore be standardized:

\[
z_{ij}=\frac{f_{ij}-\mu_j}{\sigma_j}.
\]

This produces a standardized matrix \(Z\).

---

## 11. PCA

Given standardized feature matrix \(Z\), PCA analyzes the covariance structure:

\[
C=\frac{1}{M-1}Z^TZ.
\]

PCA solves:

\[
C\mathbf{v}_i=\lambda_i\mathbf{v}_i.
\]

The eigenvectors define the principal-component directions and the eigenvalues indicate the variance explained.

### Cumulative explained variance

![Hybrid PCA explained variance](pcm_demo_output/07_hybrid_pca_explained_variance.png)

This plot indicates how many principal components are needed to explain most of the variance in the hybrid feature representation.

---

## 12. PCA using only time-domain features

![PCA time domain](pcm_demo_output/08_pca_time_domain.png)

Each point represents **one PID during one observation window**.

The time-domain representation uses only features such as:

\[
\mu_{CPI},\sigma_{CPI},\mu_{LLCMPKI},\sigma_{LLCMPKI},\ldots
\]

This is the closest equivalent to a traditional workload-characterization pipeline.

---

## 13. PCA using only frequency-domain features

![PCA frequency domain](pcm_demo_output/09_pca_frequency_domain.png)

Now each point is described by spectral characteristics such as dominant frequency, spectral energy, and entropy.

If classes separate here but not in the time-domain PCA, that would suggest that temporal periodicity contains useful discriminative information.

---

## 14. PCA using hybrid time + frequency features

![PCA hybrid](pcm_demo_output/10_pca_hybrid.png)

The hybrid representation combines both kinds of information:

\[
\mathbf{f}_{hybrid}=
[\mathbf{f}_{time},\mathbf{f}_{freq}].
\]

This representation asks the ML model to consider both:

- the average microarchitectural state of the window;
- the way that state evolves or oscillates during the window.

The hybrid PCA is therefore a natural candidate for the first full experiment.

---

## 15. What the 2-D PCA plots do — and do not — prove

A useful PCA separation is encouraging, but PCA is **not a classifier**. It maximizes variance, not class separability.

Therefore, 2-D PCA should be used as an exploratory tool:

\[
\text{feature engineering}
\rightarrow
\text{PCA visualization}
\rightarrow
\text{clustering/classification}.
\]

The next stage should quantify performance using supervised models and metrics such as:

- precision;
- recall;
- false-positive rate;
- F1 score;
- time-to-detection.

---

## 16. Hard negative workloads are essential

The detector must not simply learn that high activity means ransomware.

Legitimate workloads that should be included in training and evaluation include:

- encryption;
- compression;
- backup;
- antivirus scanning;
- databases;
- compilers;
- memory-intensive applications;
- storage-intensive applications.

The difficult problem is:

\[
\boxed{
\text{ransomware-like behavior}
\quad vs \quad
\text{legitimate workloads with similar microarchitectural behavior}
}
\]

---

## 17. Proposed research pipeline

```text
Per-PID PCM telemetry
        |
        v
Fixed / sliding windows
        |
        +--------------------+
        |                    |
        v                    v
  Time domain          Frequency domain
  mean, std            FFT / spectrum
        |                    |
        +----------+---------+
                   |
                   v
             Hybrid features
                   |
                   v
             StandardScaler
                   |
                   v
                  PCA
                   |
                   v
             PC1 vs PC2
                   |
                   v
       K-means / classifier
                   |
                   v
        Candidate PID score
```

The online detector can then evaluate the same PID repeatedly:

```text
PID 4821

Window 1 -> benign
Window 2 -> benign
Window 3 -> suspicious
Window 4 -> suspicious
Window 5 -> suspicious
```

A practical system can require persistence across several windows before escalating the PID.

---

## 18. Files generated by the demo

The Python demo creates the following educational outputs:

```text
01_raw_cpi_timeseries.png
02_raw_llc_mpki_timeseries.png
03_single_window_mean.png
04_similar_stats_different_structure.png
05_fft_periodic_vs_noise.png
06_cpi_power_spectra.png
07_hybrid_pca_explained_variance.png
08_pca_time_domain.png
09_pca_frequency_domain.png
10_pca_hybrid.png

synthetic_pcm_telemetry.csv
features_time_domain.csv
features_frequency_domain.csv
features_hybrid.csv
08_pca_time_domain.csv
09_pca_frequency_domain.csv
10_pca_hybrid.csv
```

The CSV files make it possible to inspect exactly what was sent into PCA.

---

## 19. Main takeaway

The time-series nature of PCM data does not require starting with an LSTM or Transformer.

A strong and interpretable baseline is:

\[
\boxed{
\text{PID telemetry}
\rightarrow
\text{windows}
\rightarrow
\text{time + spectral features}
\rightarrow
\text{PCA}
\rightarrow
\text{classification}
}
\]

The most important first experiment is to compare:

\[
\boxed{Time\ Domain\quad vs\quad Frequency\ Domain\quad vs\quad Hybrid}
\]

using the same workloads, windows, and train/test protocol.

If the hybrid representation improves classification of difficult benign workloads versus ransomware candidates, then the frequency domain is adding genuinely useful information rather than simply producing visually interesting plots.

