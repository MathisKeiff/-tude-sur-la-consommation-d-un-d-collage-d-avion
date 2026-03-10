Chaque dataset contient 1000 vols "record_XX"


Un vol contient 4 éléments : "axis0", "axis1", "block0_items", "block0_values"

axis0 : contient le nom des toutes les cases de l'axe 0 (55)

axis1 : pareil pour l'axe 1 (7429)

block0_items: contient la même chose que axis0 j'ai l'impression

block0_values : matrice de taille (size(axis1),size(axis0)) contenant toutes les valeurs

blockX_values regroupe les colonnes de même type dans des blocs (int, float, etc..) ici il n'y a qu'un seul type (block0_values) donc axis0 = block0_values

les différentes données dont ont a accès:
'ALT [ft]'
'EGT_1 [deg C]'
'EGT_2 [deg C]'
'FMV_1 [mm]'
'FMV_2 [mm]'
'HPTACC_1 [%]'
'HPTACC_2 [%]'
'M [Mach]'
'N1_1 [% rpm]'
'N1_2 [% rpm]'
'N2_1 [% rpm]'
'N2_2 [% rpm]'
'NAIV_1 [bool]'
'NAIV_2 [bool]'
'P0_1 [psia]'
'P0_2 [psia]'
'PRV_1 [bool]'
'PRV_2 [bool]'
'PS3_1 [psia]'
'PS3_2 [psia]'
'PT2_1 [mbar]'
'PT2_2 [mbar]'
'P_OIL_1 [psi]'
'P_OIL_2 [psi]'
'Q_1 [lb/h]'
'Q_2 [lb/h]'
'T1_1 [deg C]'
'T1_2 [deg C]'
'T2_1 [deg C]'
'T2_2 [deg C]'
'T3_1 [deg C]'
'T3_2 [deg C]'
'T5_1 [deg C]'
'T5_2 [deg C]'
'TAT [deg C]'
'TBV_1 [%]'
'TBV_2 [%]'
'TCASE_1 [deg C]'
'TCASE_2 [deg C]'
'TLA_1 [deg]'
'TLA_2 [deg]'
'T_OIL_1 [deg C]'
'T_OIL_2 [deg C]'
'VBV_1 [mm]'
'VBV_2 [mm]'
'VIB_AN1_1 [mils]'
'VIB_AN1_2 [mils]'
'VIB_AN2_1 [ips]'
'VIB_AN2_2 [ips]'
'VIB_BN1_1 [mils]'
'VIB_BN1_2 [mils]'
'VIB_BN2_1 [ips]'
'VIB_BN2_2 [ips]'
'VSV_1 [mm]'
'VSV_2 [mm]'



explication i : engine station from 0 before fan to 5 after nozzle

L’air traverse le moteur dans cet ordre : 

Entrée d’air → Fan → Compresseur → Chambre de combustion → Turbine → Tuyère


Le fan accélère l’air et commence légèrement à le comprimer.

Le compresseur augmente fortement la pression et la température de l’air avant la combustion.

La turbine récupère l’énergie des gaz chauds pour faire tourner le compresseur et le fan.


Station 0 : Avant l’entrée du moteur

Station 1 : entrée du fan

Station 2 : Après le fan / entrée du compresseur

Station 3 : Après le compresseur

Station 4 : Après la chambre de combustion

Station 5 : Après la turbine



CHOIX des variables à garder :


le débit de carburant instantané des deux moteurs:

Q_1 [lb/h] Fuel flow

Q_2 [lb/h]



Variables de puissance moteur:

EGT → température turbine (charge moteur)

EGT_1 [deg C] Exhaust Gaz Temperature

EGT_2 [deg C]


N1 / N2 → régime moteur

N1_1 [% rpm] Speed of secondary shaft (fan)

N1_2 [% rpm]

N2_1 [% rpm] Speed of primary shaft (core)

N2_2 [% rpm]


TLA → position de la manette des gaz

TLA_1 [deg] Level Angle

TLA_2 [deg]



Variables environnementales:

ALT [ft] Altitude

M [Mach] Vitesse

TAT [deg C] Température



Pressions du moteur:

PS3 → pression statique après le compresseur

PS3_1 [psia] Static pressure

PS3_2 [psia]


PT2 → pression totale après le fan

PT2_1 [mbar] Pressure

PT2_2 [mbar]



Températures internes du moteur:

T2 → Température après le fan

T2_1 [deg C]

T2_2 [deg C]


T3 → Température après le compresseur

T3_1 [deg C]

T3_2 [deg C]


T5 → Température après la turbine

T5_1 [deg C]

T5_2 [deg C]



Définition et caractérisation de la phase de montée 

Analyse préliminaire des profils de montée

Afin d’obtenir une première vision des profils de montée, nous avons représenté sur un même graphique les trajectoires d’altitude de cinq vols différents, normalisées de manière à ce que chaque vol débute au point 
(0,0)
(0,0). Cette normalisation permet de comparer plus facilement les formes de montée indépendamment de l’altitude initiale ou du moment exact du décollage.

L’observation de ces profils met en évidence deux comportements principaux de montée.

Le premier correspond à une montée continue, dans laquelle l’altitude augmente de manière relativement régulière jusqu’à atteindre l’altitude de croisière.

Le second type de profil présente l’apparition d’un palier intermédiaire, durant lequel l’avion stabilise temporairement son altitude avant de reprendre sa montée vers l’altitude finale.


Dans la suite de l’étude, il pourra donc être pertinent de séparer les vols en deux catégories :

les vols présentant une montée continue sans palier,

les vols présentant un ou plusieurs paliers intermédiaires.

Cette classification permettra d’analyser plus finement les stratégies de montée et d’adapter les méthodes d’étude aux différents types de profils observés.