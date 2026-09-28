#!/usr/bin/env python3
"""
Educational demo:
Per-PID microarchitectural time-series characterization in
time domain, frequency domain, and PCA.

IMPORTANT:
The generated classes are synthetic. They illustrate the methodology
and are NOT measured ransomware signatures.

Dependencies:
    pip install numpy pandas matplotlib scikit-learn

Run:
    python pcm_time_frequency_demo.py

Outputs are written to ./pcm_demo_output/
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


RNG = np.random.default_rng(42)

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
FS = 20.0                 # samples/second
DURATION_S = 60           # seconds per synthetic PID
WINDOW_S = 5              # seconds/window
WINDOW_N = int(FS * WINDOW_S)
N_PIDS_PER_CLASS = 5

METRICS = ["CPI", "IPC", "LLC_MPKI", "BRANCH_MPKI"]
CLASSES = ["web", "database", "compression", "ransomware_like"]

OUT = Path("pcm_demo_output")
OUT.mkdir(exist_ok=True)


# ---------------------------------------------------------------------
# Synthetic telemetry
# ---------------------------------------------------------------------
def generate_pid_trace(label: str, pid: int) -> pd.DataFrame:
    """
    Generate one synthetic PID trace.

    The formulas intentionally create different combinations of:
      - average level
      - variance
      - periodicity
      - noise

    They are chosen for teaching/visualization only.
    """
    n = int(FS * DURATION_S)
    t = np.arange(n) / FS

    phase1, phase2 = RNG.uniform(0, 2*np.pi, size=2)

    if label == "web":
        cpi = 1.05 + 0.05*np.sin(2*np.pi*0.35*t + phase1) + RNG.normal(0, 0.08, n)
        llc = 3.2 + 0.30*np.sin(2*np.pi*0.20*t + phase2) + RNG.normal(0, 0.35, n)
        branch = 2.0 + RNG.normal(0, 0.18, n)

    elif label == "database":
        cpi = 1.45 + 0.12*np.sin(2*np.pi*0.18*t + phase1) + RNG.normal(0, 0.10, n)
        llc = 10.5 + 1.0*np.sin(2*np.pi*0.25*t + phase2) + RNG.normal(0, 0.65, n)
        branch = 1.35 + RNG.normal(0, 0.14, n)

    elif label == "compression":
        cpi = 0.88 + 0.13*np.sin(2*np.pi*1.2*t + phase1) + RNG.normal(0, 0.07, n)
        llc = 5.5 + 0.45*np.sin(2*np.pi*1.2*t + phase2) + RNG.normal(0, 0.32, n)
        branch = 2.6 + 0.25*np.sin(2*np.pi*0.8*t) + RNG.normal(0, 0.13, n)

    elif label == "ransomware_like":
        # Deliberately repetitive synthetic pattern for demonstrating
        # how frequency-domain features can expose periodic structure.
        cpi = 0.92 + 0.18*np.sin(2*np.pi*2.0*t + phase1) + RNG.normal(0, 0.06, n)
        llc = 5.8 + 0.65*np.sin(2*np.pi*2.0*t + phase2) + RNG.normal(0, 0.28, n)
        branch = 1.0 + 0.12*np.sin(2*np.pi*2.0*t) + RNG.normal(0, 0.10, n)

    else:
        raise ValueError(label)

    # IPC is approximately reciprocal to CPI, with measurement noise.
    ipc = 1.0 / np.clip(cpi, 0.2, None) + RNG.normal(0, 0.025, n)

    return pd.DataFrame({
        "time_s": t,
        "pid": pid,
        "class": label,
        "CPI": cpi,
        "IPC": ipc,
        "LLC_MPKI": np.clip(llc, 0, None),
        "BRANCH_MPKI": np.clip(branch, 0, None),
    })


def make_dataset() -> pd.DataFrame:
    frames = []
    pid = 1000
    for label in CLASSES:
        for _ in range(N_PIDS_PER_CLASS):
            frames.append(generate_pid_trace(label, pid))
            pid += 1
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------
# Windowing and feature extraction
# ---------------------------------------------------------------------
def iter_windows(df: pd.DataFrame):
    for (pid, label), g in df.groupby(["pid", "class"], sort=False):
        g = g.sort_values("time_s").reset_index(drop=True)
        n_windows = len(g) // WINDOW_N

        for w in range(n_windows):
            start = w * WINDOW_N
            stop = start + WINDOW_N
            win = g.iloc[start:stop].copy()
            yield pid, label, w, win


def spectral_features(x: np.ndarray, fs: float) -> dict:
    """
    Compute compact FFT-based features after mean removal.
    Uses a one-sided real FFT.
    """
    x = np.asarray(x, dtype=float)
    centered = x - x.mean()

    fft = np.fft.rfft(centered)
    freqs = np.fft.rfftfreq(len(centered), d=1.0/fs)
    power = np.abs(fft) ** 2

    # Exclude DC (0 Hz).
    freqs_nd = freqs[1:]
    power_nd = power[1:]

    total_power = power_nd.sum()
    if total_power <= 1e-15:
        return {
            "peak_freq": 0.0,
            "peak_power": 0.0,
            "spectral_energy": 0.0,
            "spectral_entropy": 0.0,
        }

    peak_idx = np.argmax(power_nd)
    p = power_nd / total_power
    entropy = -(p * np.log2(p + 1e-15)).sum()

    return {
        "peak_freq": float(freqs_nd[peak_idx]),
        "peak_power": float(power_nd[peak_idx]),
        "spectral_energy": float(total_power),
        "spectral_entropy": float(entropy),
    }


def extract_features(raw: pd.DataFrame):
    time_rows = []
    freq_rows = []

    for pid, label, w, win in iter_windows(raw):
        meta = {
            "pid": pid,
            "class": label,
            "window": w,
            "start_s": float(win["time_s"].iloc[0]),
        }

        trow = dict(meta)
        frow = dict(meta)

        for metric in METRICS:
            x = win[metric].to_numpy()

            # Time-domain features.
            trow[f"{metric}_mean"] = float(np.mean(x))
            trow[f"{metric}_std"] = float(np.std(x))

            # Frequency-domain features.
            sf = spectral_features(x, FS)
            for name, value in sf.items():
                frow[f"{metric}_{name}"] = value

        time_rows.append(trow)
        freq_rows.append(frow)

    time_df = pd.DataFrame(time_rows)
    freq_df = pd.DataFrame(freq_rows)

    key = ["pid", "class", "window", "start_s"]
    hybrid_df = time_df.merge(freq_df, on=key, how="inner")
    return time_df, freq_df, hybrid_df


# ---------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------
def savefig(name):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=180, bbox_inches="tight")
    plt.close()


def plot_raw_examples(raw):
    # One representative PID per class.
    fig, ax = plt.subplots(figsize=(11, 5))
    for label in CLASSES:
        pid = raw.loc[raw["class"] == label, "pid"].iloc[0]
        g = raw[raw["pid"] == pid]
        ax.plot(g["time_s"], g["CPI"], label=f"{label} (PID {pid})", linewidth=1.2)
    ax.set_title("Synthetic per-PID CPI time series")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CPI")
    ax.legend()
    ax.grid(alpha=0.25)
    savefig("01_raw_cpi_timeseries.png")

    fig, ax = plt.subplots(figsize=(11, 5))
    for label in CLASSES:
        pid = raw.loc[raw["class"] == label, "pid"].iloc[0]
        g = raw[raw["pid"] == pid]
        ax.plot(g["time_s"], g["LLC_MPKI"], label=f"{label} (PID {pid})", linewidth=1.2)
    ax.set_title("Synthetic per-PID LLC MPKI time series")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("LLC MPKI")
    ax.legend()
    ax.grid(alpha=0.25)
    savefig("02_raw_llc_mpki_timeseries.png")


def plot_window_example(raw):
    label = "ransomware_like"
    pid = raw.loc[raw["class"] == label, "pid"].iloc[0]
    g = raw[raw["pid"] == pid].sort_values("time_s").reset_index(drop=True)
    win = g.iloc[:WINDOW_N]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(win["time_s"], win["CPI"], marker="o", markersize=2)
    ax.axhline(win["CPI"].mean(), linestyle="--",
               label=f"mean={win['CPI'].mean():.3f}")
    ax.set_title(f"One {WINDOW_S}-second CPI window — PID {pid}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CPI")
    ax.legend()
    ax.grid(alpha=0.25)
    savefig("03_single_window_mean.png")


def plot_same_mean_different_structure():
    # Similar mean/std, different organization in time.
    n = WINDOW_N
    t = np.arange(n) / FS
    a = 1.0 + 0.18*np.sin(2*np.pi*2.0*t)
    b = 1.0 + RNG.normal(0, np.std(a), n)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(t, a, label=f"Periodic: mean={a.mean():.2f}, std={a.std():.2f}")
    ax.plot(t, b, label=f"Noisy: mean={b.mean():.2f}, std={b.std():.2f}", alpha=0.8)
    ax.set_title("Similar time-domain statistics, different temporal structure")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Illustrative CPI")
    ax.legend()
    ax.grid(alpha=0.25)
    savefig("04_similar_stats_different_structure.png")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    for x, label in [(a, "Periodic"), (b, "Noisy")]:
        centered = x - x.mean()
        freq = np.fft.rfftfreq(n, 1/FS)
        power = np.abs(np.fft.rfft(centered)) ** 2
        ax.plot(freq[1:], power[1:], label=label)
    ax.set_title("FFT exposes the difference")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power")
    ax.legend()
    ax.grid(alpha=0.25)
    savefig("05_fft_periodic_vs_noise.png")


def plot_fft_examples(raw):
    fig, ax = plt.subplots(figsize=(10, 5))
    for label in CLASSES:
        pid = raw.loc[raw["class"] == label, "pid"].iloc[0]
        g = raw[raw["pid"] == pid].sort_values("time_s").reset_index(drop=True)
        x = g.iloc[:WINDOW_N]["CPI"].to_numpy()
        centered = x - x.mean()
        freq = np.fft.rfftfreq(len(x), 1/FS)
        power = np.abs(np.fft.rfft(centered)) ** 2
        ax.plot(freq[1:], power[1:], label=label)
    ax.set_title(f"CPI power spectra for one {WINDOW_S}-second window")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power")
    ax.legend()
    ax.grid(alpha=0.25)
    savefig("06_cpi_power_spectra.png")


def pca_plot(df, title, filename):
    meta_cols = {"pid", "class", "window", "start_s"}
    feature_cols = [c for c in df.columns if c not in meta_cols]

    X = df[feature_cols].to_numpy()
    Xz = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2)
    pcs = pca.fit_transform(Xz)

    pca_df = df[["pid", "class", "window", "start_s"]].copy()
    pca_df["PC1"] = pcs[:, 0]
    pca_df["PC2"] = pcs[:, 1]
    pca_df.to_csv(OUT / filename.replace(".png", ".csv"), index=False)

    fig, ax = plt.subplots(figsize=(8, 6))
    for label in CLASSES:
        m = pca_df["class"] == label
        ax.scatter(pca_df.loc[m, "PC1"], pca_df.loc[m, "PC2"],
                   label=label, alpha=0.75, s=35)

    evr = pca.explained_variance_ratio_ * 100
    ax.set_title(title)
    ax.set_xlabel(f"PC1 ({evr[0]:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({evr[1]:.1f}% variance)")
    ax.legend()
    ax.grid(alpha=0.25)
    savefig(filename)

    return pca, pca_df


def plot_explained_variance(df, title, filename):
    meta_cols = {"pid", "class", "window", "start_s"}
    feature_cols = [c for c in df.columns if c not in meta_cols]
    Xz = StandardScaler().fit_transform(df[feature_cols])
    pca = PCA().fit(Xz)
    cumulative = np.cumsum(pca.explained_variance_ratio_) * 100

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(np.arange(1, len(cumulative)+1), cumulative, marker="o")
    ax.axhline(90, linestyle="--", linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Number of principal components")
    ax.set_ylabel("Cumulative explained variance (%)")
    ax.set_ylim(0, 102)
    ax.grid(alpha=0.25)
    savefig(filename)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    print("Generating synthetic PCM-like telemetry...")
    raw = make_dataset()
    raw.to_csv(OUT / "synthetic_pcm_telemetry.csv", index=False)

    print("Extracting window features...")
    time_df, freq_df, hybrid_df = extract_features(raw)
    time_df.to_csv(OUT / "features_time_domain.csv", index=False)
    freq_df.to_csv(OUT / "features_frequency_domain.csv", index=False)
    hybrid_df.to_csv(OUT / "features_hybrid.csv", index=False)

    print("Generating explanatory charts...")
    plot_raw_examples(raw)
    plot_window_example(raw)
    plot_same_mean_different_structure()
    plot_fft_examples(raw)

    plot_explained_variance(
        hybrid_df,
        "PCA cumulative explained variance — hybrid features",
        "07_hybrid_pca_explained_variance.png",
    )

    print("Generating 2-D PCA plots...")
    pca_plot(
        time_df,
        "PCA — time-domain features (mean + standard deviation)",
        "08_pca_time_domain.png",
    )
    pca_plot(
        freq_df,
        "PCA — frequency-domain features",
        "09_pca_frequency_domain.png",
    )
    pca_plot(
        hybrid_df,
        "PCA — hybrid time + frequency features",
        "10_pca_hybrid.png",
    )

    print(f"\nDone. Outputs written to: {OUT.resolve()}")
    print("Important: synthetic classes are educational, not measured ransomware signatures.")


if __name__ == "__main__":
    main()

