import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_all_flights(fichier_parquet):
    """
    Trace les profils d'altitude de tous les vols contenus dans un fichier parquet.
    """
    df = pd.read_parquet(fichier_parquet)

    vols = df["record"].unique()

    plt.figure(figsize=(10, 6))

    for record in vols:
        df_vol = df[df["record"] == record].copy()
        df_vol = df_vol.reset_index(drop=True)

        t = range(len(df_vol))
        plt.plot(t, df_vol["ALT [ft]"], alpha=0.2)

    plt.xlabel("Temps (index)")
    plt.ylabel("Altitude (ft)")
    titre = str(fichier_parquet).replace(".parquet", "").replace("_", " ")
    plt.title(f"Profils d'altitude de tous les {titre}")
    plt.grid(True)
    plt.show()


def plot_takeoff_altitude_profiles(
    fichier_parquet,
    alt_max=None,
    t_max=None,
    seuil_detection=5,
    max_vols=None
):
    """
    Trace les profils de décollage (ALT) pour tous les vols,
    en normalisant chaque courbe pour qu'elle commence en (0, 0).
    """
    df = pd.read_parquet(fichier_parquet)

    plt.figure(figsize=(10, 6))

    vols = list(df["record"].unique())
    if max_vols is not None:
        vols = vols[:max_vols]

    nb_traces = 0

    for record in vols:
        df_vol = df[df["record"] == record].copy()
        df_vol = df_vol.reset_index(drop=True)

        if len(df_vol) < 2:
            continue

        dalt = df_vol["ALT [ft]"].diff()
        idx_takeoff_list = dalt[dalt > seuil_detection].index

        if len(idx_takeoff_list) == 0:
            continue

        idx_takeoff = idx_takeoff_list[0]

        df_vol["t_rel"] = np.arange(len(df_vol)) - idx_takeoff

        alt_takeoff = df_vol.loc[idx_takeoff, "ALT [ft]"]
        df_vol["alt_rel"] = df_vol["ALT [ft]"] - alt_takeoff

        df_vol = df_vol[df_vol["t_rel"] >= 0].copy()

        if alt_max is not None:
            df_vol = df_vol[df_vol["alt_rel"] <= alt_max]

        if t_max is not None:
            df_vol = df_vol[df_vol["t_rel"] <= t_max]

        if df_vol.empty:
            continue

        plt.plot(df_vol["t_rel"], df_vol["alt_rel"], alpha=0.3)
        nb_traces += 1

    plt.xlabel("Temps relatif au décollage")
    plt.ylabel("Altitude relative (ft)")
    plt.title(f"Profils de décollage normalisés ({nb_traces} vols)")
    plt.grid(True)
    plt.show()