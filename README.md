# Étude de la consommation en montée d'un avion

## Description du projet

Ce projet vise à analyser la **consommation de carburant durant la phase de montée d’un avion** à partir de données de vol enregistrées.

Les objectifs principaux sont :

- détecter automatiquement les phases de montée
- distinguer deux types de profils :
  - montée continue
  - montée avec palier intermédiaire
- construire des variables synthétiques décrivant chaque montée
- analyser statistiquement les différences entre ces profils

Les méthodes utilisées incluent :

- statistiques descriptives
- visualisations
- analyse en composantes principales (PCA)
- clustering (K-Means)

---

# Dataset

Les données utilisées dans ce projet **ne sont pas incluses dans le repository GitHub** en raison de leur taille.

Le dataset peut être téléchargé depuis Kaggle :

https://www.kaggle.com/datasets/jrmlac/dfdr1000?resource=download

## Installation des données

1. Télécharger l’archive du dataset depuis Kaggle.

2. Placer l’archive téléchargée dans le dossier suivant du projet :

```
data/raw/
```

3. Décompresser l’archive afin d’obtenir la structure suivante :

```
data/
 ├── raw
 │   └── archive
 │       ├── Aircraft_01.h5
 │       ├── Aircraft_02.h5
 │       └── Aircraft_03.h5
```

Ces fichiers `.h5` contiennent les données brutes des vols et sont utilisés par le pipeline de traitement.

---

Une fois les données installées, le projet peut être exécuté avec :

```
python main.py
```

---

# Structure du projet

```
project/
│
├── data
│   ├── raw
│   │   └── archive
│   │       ├── Aircraft_01.h5
│   │       ├── Aircraft_02.h5
│   │       └── Aircraft_03.h5
│   │
│   └── processed
│       ├── vols_avec_palier.parquet
│       ├── vols_sans_palier.parquet
│       ├── variables_montee_avec_palier.parquet
│       └── variables_montee_sans_palier.parquet
│
├── src
│   ├── aircraft_dataset_builder.py
│   ├── climb_detection.py
│   ├── feature_engineering.py
│   ├── analysis.py
│   └── visualization.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Structure des données

Chaque dataset contient environ **1000 vols**, identifiés sous la forme :

```
record_XX
```

Les données sont stockées au format **HDF5**.

Chaque vol contient quatre éléments :

| Élément | Description |
|------|------|
| axis0 | noms des variables (55 capteurs) |
| axis1 | index temporel (~7429 points) |
| block0_items | équivalent de axis0 |
| block0_values | matrice contenant toutes les valeurs |

La matrice `block0_values` est de taille :

```
(size(axis1), size(axis0))
```

Elle contient toutes les valeurs des capteurs.

Les données sont regroupées par type numérique dans des blocs (`blockX_values`).  
Dans ce dataset, il n'existe qu’un seul bloc (`block0_values`).

---

# Variables disponibles

Les données contiennent différentes catégories de variables.

## Variables moteur

### Débit carburant

```
Q_1 [lb/h]
Q_2 [lb/h]
```

### Température turbine

```
EGT_1 [deg C]
EGT_2 [deg C]
```

### Régime moteur

```
N1_1 [% rpm]
N1_2 [% rpm]

N2_1 [% rpm]
N2_2 [% rpm]
```

### Position des manettes de poussée

```
TLA_1 [deg]
TLA_2 [deg]
```

---

## Variables environnementales

```
ALT [ft]   Altitude
M [Mach]   Vitesse relative au son
TAT [deg C] Température de l’air
```

---

## Pressions moteur

```
PS3_1 [psia]
PS3_2 [psia]

PT2_1 [mbar]
PT2_2 [mbar]
```

---

## Températures internes moteur

```
T2_1 [deg C]
T2_2 [deg C]

T3_1 [deg C]
T3_2 [deg C]

T5_1 [deg C]
T5_2 [deg C]
```

---

# Stations moteur

Les indices correspondent aux stations du moteur.

L’air traverse le moteur dans l’ordre suivant :

```
Entrée d’air → Fan → Compresseur → Chambre de combustion → Turbine → Tuyère
```

| Station | Description |
|------|------|
| 0 | Avant l'entrée du moteur |
| 1 | Entrée du fan |
| 2 | Après le fan |
| 3 | Après le compresseur |
| 4 | Après la chambre de combustion |
| 5 | Après la turbine |

---

# Détection de la phase de montée

## Analyse préliminaire

Pour visualiser les profils de montée, plusieurs trajectoires d’altitude ont été représentées sur un même graphique.

Chaque vol est **normalisé** pour commencer au point :

```
(0,0)
```

Cela permet de comparer les formes de montée indépendamment de l’altitude initiale.

Deux comportements principaux apparaissent :

### Montée continue

L’altitude augmente régulièrement jusqu’à l’altitude de croisière.

### Montée avec palier

Un palier intermédiaire apparaît avant la reprise de la montée.

---

# Algorithme de détection des paliers

L’algorithme repose sur l’analyse de l’évolution de l’altitude à l’aide de **fenêtres glissantes**.

### Paramètres utilisés

| Paramètre | Valeur | Description |
|------|------|------|
| Taille fenêtre | 10 points | ≈ 10 secondes |
| Seuil stabilité | 80 ft | variation max altitude |
| Seuil reprise | 200 ft | reprise significative de montée |
| Points futurs | 10, 30, 200 | vérification reprise montée |

### Détection du début de montée

```
ALT(t0 + 5) − ALT(t0) > seuil
```

---

# Résultats de classification

## Aircraft 1

| Catégorie | Nombre |
|------|------|
Total vols | 1001  
Pas de décollage | 4  
Classés | 994  
Avec palier | 447  
Sans palier | 550  

---

## Aircraft 2

| Catégorie | Nombre |
|------|------|
Total vols | 1002  
Pas de décollage | 1  
Classés | 1001  
Avec palier | 628  
Sans palier | 373  

---

## Aircraft 3

| Catégorie | Nombre |
|------|------|
Total vols | 1002  
Pas de décollage | 2  
Classés | 998  
Avec palier | 611  
Sans palier | 389  

---

# Construction des variables d’analyse

Pour chaque vol, plusieurs variables synthétiques sont calculées.

### Consommation carburant

```
carburant_cumule
```

Somme des débits carburant des deux moteurs sur la montée.

### Durée de montée

```
duree
```

Nombre de points mesurés (≈ secondes).

### Altitude

```
ALT_init
ALT_fin
```

Altitude au début et à la fin de la montée.

### Taux de montée

```
taux_montee = (ALT_fin − ALT_init) / durée
```

### Vitesse

```
Mach_moyen
```

### Paramètres moteur

```
N1_moyen
N2_moyen
TLA_moyen
EGT_moyen
```

---

# Analyse statistique

Les analyses incluent :

- histogrammes
- boxplots
- matrices de corrélation
- analyse en composantes principales (PCA)
- clustering (KMeans)

---

# Résultats principaux

## Vols sans palier

La première composante principale explique **71 à 78 % de la variance**.

Deux clusters apparaissent :

- montée classique (~950 s)
- segments très courts (cas rares)

Les montées sans palier sont **très homogènes**.

---

## Vols avec palier

La variance est plus répartie :

- PC1 ≈ 44–49 %
- PC2 ≈ 33–38 %

Trois stratégies de montée apparaissent :

1. montée longue → consommation élevée  
2. montée courte → consommation plus faible  
3. stratégie intermédiaire  

---

# Conclusion

Les montées **sans palier** sont relativement homogènes et suivent une stratégie directe.

Les montées **avec palier** présentent une variabilité beaucoup plus importante.

Les résultats montrent que les paramètres les plus déterminants pour la consommation sont :

- durée de montée
- taux de montée
- stratégie de gestion du moteur

Une montée plus courte avec un taux de montée élevé tend à être **plus efficace énergétiquement**.

---

# Lancer le projet

## Installation

```bash
git clone <repo>
cd project
pip install -r requirements.txt
```

## Exécution

```
python main.py
```