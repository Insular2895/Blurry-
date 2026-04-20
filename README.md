<div align="center">
# 🌐 Blurry — Système décisionnel de revente internationale
 
### Système d'aide à la décision pour le stock rebalancing international et l'activation ponctuelle de stocks dormants
 
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Portfolio_Project-blue?style=for-the-badge)](https://github.com/Insular2895/Blurry-)
 
[Installation](#️-installation) • [Utilisation](#-utilisation) • [Pipeline](#-pipeline-analytique) • [Architecture](#️-architecture) • [Dashboards](#-dashboards) • [Évolutions](#-évolutions-possibles)
 
</div>
---
 
## 📑 Sommaire
 
- [📖 Présentation](#-présentation)
- [🏢 Contexte métier](#-contexte-métier)
- [🎯 Objectif](#-objectif)
- [🏗️ Architecture](#️-architecture)
- [⚙️ Installation](#️-installation)
- [🚀 Utilisation](#-utilisation)
- [📊 Jeux de données](#-jeux-de-données)
- [🔄 Pipeline analytique](#-pipeline-analytique)
- [📈 Résultats attendus](#-résultats-attendus)
- [📏 Indicateurs suivis](#-indicateurs-suivis)
- [📊 Dashboards](#-dashboards)
- [🔮 Évolutions possibles](#-évolutions-possibles)
- [💡 Intérêt du projet](#-intérêt-du-projet)
- [📝 Résumé court](#-résumé-court)
---
 
## 📖 Présentation
 
Ce projet simule un système d'aide à la décision pour une société travaillant avec plusieurs boutiques partenaires afin d'éviter que certains produits restent durablement invendus dans leur zone locale.
 
> **Note importante** :

Le projet s'inspire d'une expérience concrète menée au sein de Blurry, 
où j'ai travaillé sur la conception et la structuration d'un système 
similaire pour optimiser la distribution de stocks entre plusieurs 
marchés internationaux.

Le projet présenté ici est une **modélisation analytique** de cette 
problématique métier, transposée dans un cadre portfolio avec des 
données synthétiques. Il reflète la logique décisionnelle, les 
contraintes opérationnelles et l'approche data que j'ai développées 
dans ce contexte réel.

**Objectif du portfolio** : Démontrer ma capacité à transformer un 
problème business complexe en système d'aide à la décision exploitable, 
reproductible et documenté..
 
### 🎯 Objectifs clés
 
Détecter les stocks qui stagnent localement, identifier les marchés capables de mieux les absorber, puis décider **quand**, **où** et **à quelles conditions économiques** il devient pertinent de les repositionner.
 
### 🔑 Principes de fonctionnement
 
```
┌─────────────────────────────────────────────────────────────┐
│  Le stock reste dans sa boutique d'origine                  │
│  ↓                                                          │
│  Il ne bouge que lorsqu'une activation est décidée          │
│  ↓                                                          │
│  Ce mécanisme constitue l'unique levier de redistribution   │
│  contrôlée inter-boutiques                                  │
└─────────────────────────────────────────────────────────────┘
```
 
Le projet couvre une logique complète de **rebalancing**, depuis l'identification du stock dormant jusqu'à la recommandation d'activation, en passant par l'analyse du coût complet, de la demande cible et de la rentabilité attendue.
 
---
 
## 🏢 Contexte métier
 
Certaines références vendent mal dans leur marché local alors qu'elles pourraient mieux performer ailleurs.
 
### ⚡ Défis identifiés
 
- ✅ Un produit peut être plus demandé ailleurs
- ⚠️ Mais le transport peut dégrader la marge
- ⚠️ La douane peut rendre l'opération peu intéressante
- ⚠️ Le change peut compresser la rentabilité
- ⚠️ Le marché cible peut ne pas accepter le prix nécessaire
- ⚠️ Une fois arrivé, il faut gérer le dernier kilomètre jusqu'au point de vente
### 🎲 Modèle retenu
 
| Contrainte | Description |
|------------|-------------|
| 📦 Stock local | Le stock est détenu localement par les boutiques partenaires |
| 🚫 Pas de rotation libre | Le stock ne tourne pas librement entre les points de vente |
| ✅ Activation contrôlée | Les produits ne bougent que lorsqu'une activation est validée |
| 💰 Objectif économique | Améliorer la monétisation des stocks dormants sans complexité logistique |
 
---
 
## 🎯 Objectif
 
Répondre à six questions centrales :
 
| # | Question métier | Sortie attendue |
|---|-----------------|-----------------|
| 1️⃣ | Quels produits stagnent suffisamment pour devenir candidats au rebalancing ? | Score de santé du stock |
| 2️⃣ | Quels marchés sont les plus intéressants selon la demande, le prix et la volatilité ? | Score d'opportunité marché |
| 3️⃣ | Le coût complet reste-t-il acceptable une fois intégrés transport, douane, packaging et dernier kilomètre ? | Analyse de coût complet |
| 4️⃣ | Le marché cible supporte-t-il le prix requis ? | Analyse de faisabilité prix |
| 5️⃣ | Quelles activations doivent être validées en priorité ? | Recommandations d'activation |

 
---
 
## 🏗️ Architecture
 
```text
Blurry/
│
├── 📄 README.md
├── 📄 requirements.txt
│
├── 💾 data/
│   │
│   ├── 📂 raw/
│   │   ├── dim_sku.csv
│   │   ├── dim_location.csv
│   │   ├── dim_market.csv
│   │   ├── fact_stock_health.csv
│   │   ├── fact_market_opportunity.csv
│   │   ├── fact_weekly_activation.csv
│   │   ├── fx_rates.csv
│   │   ├── shipping_rates.csv
│   │   └── customs_rules.csv
│   │
│   ├── 📂 curated/
│   │   ├── stock_health_enriched.csv
│   │   ├── market_opportunity_enriched.csv
│   │   ├── pricing_enriched.csv
│   │   ├── activation_recommendation.csv
│   │   └── *_clean.csv
│   │
│   └── 📂 exports/
│       ├── approved_activations.csv
│       └── rejected_activations.csv
│
└── 🐍 src/
    ├── load_data.py
    ├── data_quality_check.py
    ├── stock_health.py
    ├── market_opportunity.py
    ├── pricing.py
    ├── activation.py
    ├── dashboard_export.py
    └── run_pipeline.py
```
 
---
 
## ⚙️ Installation
 
### 📋 Prérequis
 
```bash
Python 3.9 ou supérieur
pip
```
 
### 1️⃣ Clonage du dépôt
 
```bash
git clone https://github.com/Insular2895/Blurry-.git
cd Blurry-
```
 
### 2️⃣ Création de l'environnement virtuel
 
<details>
<summary><b>macOS / Linux</b></summary>
```bash
python3 -m venv .venv
source .venv/bin/activate
```
</details>
<details>
<summary><b>Windows</b></summary>
```bash
python -m venv .venv
.venv\Scripts\activate
```
</details>
### 3️⃣ Installation des dépendances
 
```bash
pip install -r requirements.txt
```
 
---
 
## 🚀 Utilisation
 
### Exécution complète
 
```bash
python src/run_pipeline.py
```
 
ou
 
```bash
python3 src/run_pipeline.py
```
 
### 📤 Ce que produit l'exécution
 
```yaml
Pipeline:
  - ✅ Chargement des fichiers sources
  - ✅ Contrôle qualité des tables
  - ✅ Enrichissement du risque stock
  - ✅ Scoring d'opportunité marché
  - ✅ Calcul du coût complet et du prix recommandé
  - ✅ Validation ou rejet des activations
  - ✅ Export des tables de restitution
```
 
---
 
## 📊 Jeux de données
 
### 📐 Tables de dimension
 
| Fichier | Rôle | Type |
|---------|------|------|
| `dim_sku.csv` | Référentiel produits | 🏷️ Dimension |
| `dim_location.csv` | Référentiel boutiques / points de stock | 📍 Dimension |
| `dim_market.csv` | Référentiel marchés cibles | 🌍 Dimension |
 
### 📈 Tables de faits
 
| Fichier | Rôle | Type |
|---------|------|------|
| `fact_stock_health.csv` | Niveau de pression sur le stock local | 📊 Fait |
| `fact_market_opportunity.csv` | Attractivité d'un couple produit / marché | 📊 Fait |
| `fact_weekly_activation.csv` | Candidats d'activation | 📊 Fait |
 
### 🔧 Tables d'enrichissement
 
| Fichier | Rôle | Type |
|---------|------|------|
| `fx_rates.csv` | Change et buffer de risque | 💱 Enrichissement |
| `shipping_rates.csv` | Coûts et hypothèses d'expédition | 🚚 Enrichissement |
| `customs_rules.csv` | Hypothèses douanières simplifiées | 🛃 Enrichissement |
 
---
 
## 🔄 Pipeline analytique
 
### 1️⃣ Chargement des données
 
```python
# Module: load_data.py
# Charge tous les fichiers du dossier data/raw/
```
 
### 2️⃣ Contrôle qualité
 
```python
# Module: data_quality_check.py
# Vérifie la présence des colonnes, l'absence de nulls critiques,
# les doublons et la cohérence des clés entre tables
```
 
### 3️⃣ Analyse du stock
 
```python
# Module: stock_health.py
# Identifie les références présentant des signes de stagnation locale
```
 
**Signaux pris en compte :**
- 📅 Jours moyens en stock
- 🔄 Vitesse d'écoulement récente
- 📦 Quantité disponible
- ⚠️ Niveau de risque
> **Point clé :** Détecter les produits qui immobilisent du capital et méritent une réallocation ponctuelle.
 
### 4️⃣ Analyse des marchés
 
```python
# Module: market_opportunity.py
# Mesure l'intérêt commercial d'un marché cible pour chaque produit
```
 
**Signaux utilisés :**
- 💰 Prix moyen de marché
- 📊 Score de demande
- 📈 Tendance
- 📉 Volatilité
> **Objectif :** Identifier les zones capables d'absorber le stock déplacé avec un meilleur niveau de rotation ou de marge.
 
### 5️⃣ Calcul du coût complet et du prix recommandé
 
```python
# Module: pricing.py
# Calcule un coût complet par couple source / destination
```
 
**Formule :**
 
```
Coût complet = Prix d'achat 
             + Transport international
             + Douane
             + Packaging
             + Contrôle qualité
             + Buffer change
             + Dernier kilomètre
```
 
> **Important :** Le dernier kilomètre doit être intégré. Même si le produit arrive dans un entrepôt cible, il reste un coût de mise à disposition finale.
 
**Validation du prix :** Le système détermine si le prix nécessaire pour atteindre la marge cible reste compatible avec le marché observé.
 
### 6️⃣ Recommandation d'activation
 
```python
# Module: activation.py
# Approuve ou rejette les activations candidates
```
 
**Règles de validation :**
 
| Critère | Vérification |
|---------|--------------|
| ✅ Stock éligible | Stock réellement éligible |
| 📊 Potentiel marché | Potentiel marché suffisant |
| 💰 Prix supporté | Prix supporté par le marché |
| 📈 Marge acceptable | Marge attendue encore acceptable |
| 💵 Coût cohérent | Coût complet final cohérent |
 
> **Philosophie :** Recommander peu d'actions, mais des actions cohérentes et défendables.
 
### 7️⃣ Export pour restitution
 
```python
# Module: dashboard_export.py
# Génère les tables finales exploitables dans Excel, Google Sheets, Power BI
```
 
---
 
## 📈 Résultats attendus
 
Le projet permet de produire des conclusions du type :
 
```diff
+ Telle référence est prioritaire : stock sous pression et marché cible absorbe le prix
 
- Telle activation est rejetée : prix nécessaire dépasse le niveau accepté par le marché
 
+ Certains marchés absorbent mieux les produits premium
 
+ Certaines références ont surtout un intérêt de rebalancing, pas de vente opportuniste
```
 
---
 
## 📏 Indicateurs suivis
 
### 📦 Stock / activation
 
```yaml
Stock:
  - Nombre de références en stagnation
  - Nombre d'activations éligibles
  - Volume candidat par activation
 
Décisions:
  - Activations approuvées vs rejetées
```
 
### 💰 Prix / marge
 
```yaml
Coûts:
  - Coût complet
  - Prix recommandé
  - Écart prix recommandé / prix marché
 
Rentabilité:
  - Marge attendue
  - Faisabilité commerciale du prix
  - Poids du dernier kilomètre
```
 
---
 
## 📊 Dashboards
 
Les dashboards rendent lisible la logique métier du système décisionnel. Ils répondent à la question :
 
> Quels produits sortir de leur marché local, vers quelle destination, à quel prix, et avec quelle marge une fois intégrés transport, douane, packaging et dernier kilomètre ?
 
Le pipeline est reproductible : les mêmes scripts peuvent être réexécutés avec un autre jeu de données. Les visualisations sont cohérentes pour une preuve de concept.
 
### 📋 Dashboard 1 — Vue executive
 
Vue synthétique des décisions recommandées pour la prochaine vague d'activation.
 
**Contenu :**
- Nombre total d'activations étudiées
- Activations approuvées / rejetées
- Bénéfice total attendu
- Marge moyenne
- Meilleures activations validées
- Principaux motifs de rejet
<img width="1200" alt="Dashboard Executive" src="https://github.com/user-attachments/assets/988a4e3c-a2af-492d-98a2-90d9923b3ed5" />
---
 
### 📦 Dashboard 2 — Santé du stock
 
Explique **pourquoi** certains produits deviennent candidats au rebalancing.
 
**Contenu :**
- Jours moyens en stock
- Taux d'écoulement à 30 jours
- Score de risque stock
- Volume dormant par localisation
- Références les plus sous pression
<img width="1200" alt="Dashboard Stock" src="https://github.com/user-attachments/assets/52df50a8-2870-498a-8db3-214fe9e3fe90" />
---
 
### 🌍 Dashboard 3 — Opportunité marché
 
**Où** ce stock dormant a-t-il le plus de chances d'être mieux absorbé ?
 
**Contenu :**
- Score d'opportunité par produit/pays
- Score de demande
- Tendance
- Volatilité
- Prix moyen observé
- Niveau de priorité marché
<img width="1200" alt="Dashboard Marché" src="https://github.com/user-attachments/assets/3e563330-6554-45f5-992c-9d825b9ae058" />
---
 
### 💰 Dashboard 4 — Pricing et coût complet
 
Montre que la décision n'a de sens que si le marché cible supporte un prix cohérent avec le coût complet réel.
 
**Contenu :**
- Décomposition du coût complet
- Prix recommandé
- Prix moyen marché
- Écart prix recommandé / marché
- Statut pricing
<img width="1200" alt="Dashboard Pricing" src="https://github.com/user-attachments/assets/c2fc025b-3eda-4d43-bbf2-17f93c4e7a4f" />
---
 
### ✅ Dashboard 5 — Moteur de décision
 
Rend visible la logique finale d'approbation ou de rejet.
 
**Contenu :**
- Score de risque stock
- Score d'opportunité marché
- Marge attendue
- Unités candidates
- Score final d'activation
- Décision et raison
<img width="1200" alt="Dashboard Decision 1" src="https://github.com/user-attachments/assets/4f0e26af-1617-441e-a4e7-a20a6d1544eb" />
<img width="1200" alt="Dashboard Decision 2" src="https://github.com/user-attachments/assets/058917fd-f4c2-4944-ba5a-2e02c8177211" />
<img width="1200" alt="Dashboard Decision 3" src="https://github.com/user-attachments/assets/9f34dfbe-45f3-4f9a-8734-1c44b375b02f" />
---

 Exemples de décisions produites par le modèle :

- Le SKU_003 doit être activé depuis LOC_003 vers le Canada : 11 unités vendables, 106.80 € de marge unitaire, 1 174.80 € de profit attendu.
- Le SKU_004 doit être activé depuis LOC_002 vers BX : 16 unités vendables, 35.19 € de marge unitaire, 563.04 € de profit attendu.
- Le SKU_004 doit être activé depuis LOC_002 vers le Canada : 12 unités vendables, 44.16 € de marge unitaire, 529.92 € de profit attendu.

À l’inverse, certaines activations sont rejetées, comme le SKU_002 vers le Canada, car le prix requis dépasse le niveau supporté par le marché cible. 

## 🔮 Évolutions possibles
 
### 🌐 Données externes
 
```yaml
APIs:
  - 💰 API prix marché (StockX)
  - 💱 API taux de change (FX rates)
  - 🚚 API transporteurs (UPS Campus)
  
Signaux:
  - 📊 Signaux boutiques partenaires
  - 👥 Données de votes clients (questionnaire raffle)
  
Raffinements:
  - 🛃 Hypothèses douanières plus fines
  - 🚗 Coûts dernier kilomètre par pays/zone urbaine
```
 
### 💾 Plateforme data
 
```yaml
Infrastructure:
  - 🐘 PostgreSQL ou BigQuery
  - 🔄 Transformations SQL ou dbt
  - 📚 Historisation
  - ⏰ Exécution planifiée
  - ☁️ Déploiement cloud
```
 
### 📊 Restitution
 
```yaml
Visualisation:
  - 📊 Dashboard Power BI complet
  - 🌍 Vues comparatives par marché
  - 📈 Waterfall de marge
  - 🗺️ Cartes pays ( folium ) 
  - 📄 Exports PDF exécutifs
```
 
### 🧠 Approfondissements analytiques
 
```yaml
Modélisation:
  - 🎯 Score de confiance par marché
  - 📈 Forecast de demande
  - 📦 Contraintes de capacité par boutique
  - 🔧 Moteur d'optimisation avancé
  - ⚖️ Arbitrage automatique volume/marge/risque
  - 🚗 Segmentation fine des coûts dernier kilomètre
```
 
### ⚠️ Tests de robustesse (stress tests)
 
```yaml
Scénarios de stress:
  - 💱 Stress change (+20% variation FX)
  - 🚚 Stress transport (+30% coûts logistiques)
  - 📉 Stress demande (-40% volume attendu)
  - ⚠️ Scénario dégradé combiné
  
Analyses:
  - Profit total par scénario
  - Marge unitaire moyenne par scénario
  - Nombre d'activations encore profitables
  - Activations les plus résilientes vs fragiles
  
Module:
  - scenarios.py
  - scenario_analysis.csv
  - scenario_summary.csv
  - Dashboard 6 — Scénarios de stress
```
 
---
 
## 💡 Intérêt du projet
 
Ce projet démontre la capacité à :
 
```diff
+ Structurer un problème métier international complexe
+ Raisonner en stock rebalancing, pas en simple vente opportuniste
+ Relier données, coûts et rentabilité
+ Intégrer les contraintes réelles de transport et dernier kilomètre
+ Construire une logique de pricing à partir du coût complet
+ Produire des recommandations auditables
+ Maintenir un pipeline analytique reproductible
+ Restituer un sujet data business orienté décision
```
 
> **Positionnement :** Le projet reste volontairement mesuré. Il ne simule pas un système opérationnel complet, mais démontre une capacité de modélisation propre, crédible et utile.
 
---
 
## 📝 Résumé court
## 📝 Résumé court

<div align="center">

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  Ce projet simule un système d'aide à la décision pour une société   │
│  travaillant avec plusieurs boutiques partenaires afin de:           │
│                                                                      │
│  ✅ Identifier les stocks dormants                                   │
│  ✅ Décider des actions de stock rebalancing les plus pertinentes    │
│  ✅ Sélectionner les marchés cibles les plus intéressants            │
│  ✅ Calculer un coût complet réaliste incluant le dernier kilomètre  │
│  ✅ Tester la robustesse de ces décisions sous différents scénarios  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

</div>

---

<div align="center">

**[⬆ Retour en haut](#-blurry--système-décisionnel-de-revente-internationale)**

</div>
