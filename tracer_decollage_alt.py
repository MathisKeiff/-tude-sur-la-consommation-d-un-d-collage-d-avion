import pandas as pd
import matplotlib.pyplot as plt

def tracer_decollage_alt(
        fichier_parquet,
        alt_max=None,
        t_max=None,
        seuil_detection=5,
        max_vols=None
    ):
    """
    Trace les profils de décollage (ALT) pour tous les vols.

    paramètres
    ----------
    fichier_parquet : str
        chemin du dataset parquet

    alt_max : float ou None
        altitude max pour couper la courbe (ex: 3000 ft)

    t_max : int ou None
        nombre de points après décollage

    seuil_detection : float
        seuil de montée d'altitude pour détecter le décollage

    max_vols : int ou None
        nombre maximum de vols à tracer (None = tous)
    """

    df = pd.read_parquet(fichier_parquet)

    plt.figure(figsize=(10,6))

    # sélection des vols
    vols = list(df["record"].unique())
    if max_vols is not None:
        vols = vols[:max_vols]  # ne garder que les premiers max_vols

    for record in vols:
        df_vol = df[df["record"] == record].copy()

        # détection du décollage
        dalt = df_vol["ALT [ft]"].diff()
        idx_takeoff = dalt[dalt > seuil_detection].index

        if len(idx_takeoff) == 0:
            continue

        idx_takeoff = idx_takeoff[0]

        # temps relatif
        df_vol["t_rel"] = range(len(df_vol))
        df_vol["t_rel"] = df_vol["t_rel"] - df_vol.loc[idx_takeoff, "t_rel"]

        # garder uniquement après décollage
        df_vol = df_vol[df_vol["t_rel"] >= 0]

        # limiter altitude
        if alt_max is not None:
            df_vol = df_vol[df_vol["ALT [ft]"] <= alt_max]

        # limiter durée
        if t_max is not None:
            df_vol = df_vol[df_vol["t_rel"] <= t_max]

        plt.plot(df_vol["t_rel"], df_vol["ALT [ft]"], alpha=0.3)

    plt.xlabel("Temps relatif au décollage")
    plt.ylabel("Altitude (ft)")
    plt.title("Profils de décollage")
    plt.grid()
    plt.show()