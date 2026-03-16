import pandas as pd

from src.aircraft_dataset_builder import run_aircraft_dataset_builder
from src.climb_detection import run_climb_detection
from src.feature_engineering import run_feature_engineering
from src.analysis import analyse_montee
from src.visualization import plot_all_flights, plot_takeoff_altitude_profiles


def main():
    print("\n" + "=" * 50)
    print("1. Construction des datasets aircraft")
    print("=" * 50)
    run_aircraft_dataset_builder()

    print("\n" + "=" * 50)
    print("2. Détection des phases de montée")
    print("=" * 50)
    run_climb_detection()

    print("\n" + "=" * 50)
    print("3. Construction des variables d'analyse")
    print("=" * 50)
    run_feature_engineering()

    print("\n" + "=" * 50)
    print("4. Analyse des vols avec palier")
    print("=" * 50)
    df_avec = pd.read_parquet("data/processed/variables_montee_avec_palier.parquet")
    analyse_montee(df_avec)

    print("\n" + "=" * 50)
    print("5. Analyse des vols sans palier")
    print("=" * 50)
    df_sans = pd.read_parquet("data/processed/variables_montee_sans_palier.parquet")
    analyse_montee(df_sans)

if __name__ == "__main__":
    main()