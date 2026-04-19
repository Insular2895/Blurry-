<div align="center">

# 🌐 Blurry — Système décisionnel de revente internationale

### Système d'aide à la décision pour le stock rebalancing international et l'activation ponctuelle de stocks dormants

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Portfolio_Project-blue?style=for-the-badge)](https://github.com/yourusername/blurry-weekly-drop-intelligence)

[Installation](#-installation) • [Utilisation](#-utilisation) • [Pipeline](#-pipeline-analytique) • [Architecture](#-architecture) • [Dashboards](#-dashboards-recommandés) • [Évolutions](#-évolutions-possibles)

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
- [📊 Dashboards recommandés](#-dashboards-recommandés)
- [⚠️ Scénarios de stress](#️-scénarios-de-stress)
- [🔮 Évolutions possibles](#-évolutions-possibles)
- [💡 Intérêt du projet](#-intérêt-du-projet)
- [📝 Résumé court](#-résumé-court)

---

## 📖 Présentation

Ce projet simule un système d'aide à la décision pour une société travaillant avec plusieurs boutiques partenaires afin d'éviter que certains produits restent durablement invendus dans leur zone de chalandise locale.

> **Note importante** : Le bon angle de lecture n'est pas celui d'une marketplace classique ni celui d'un simple outil de pricing. Le projet doit surtout être compris comme un système de **stock rebalancing international**.

### 🎯 Objectifs clés

L'objectif est de détecter les stocks qui stagnent localement, d'identifier les marchés capables de mieux absorber ces produits, puis de décider **quand**, **où** et **à quelles conditions économiques** il devient pertinent de les repositionner.

### 🔑 Principes de fonctionnement

```
┌─────────────────────────────────────────────────────────────┐
│  Le stock n'est pas déplacé en continu                      │
│  ↓                                                          │
│  Il reste dans sa boutique d'origine tant qu'aucune         │
│  activation n'est décidée                                   │
│  ↓                                                          │
│  Le mouvement n'a lieu que lorsqu'un produit est            │
│  sélectionné dans le cadre d'une opération de vente         │
│  ponctuelle                                                 │
│  ↓                                                          │
│  Ce mécanisme constitue l'unique levier d'activation        │
│  inter-boutiques                                            │
└─────────────────────────────────────────────────────────────┘
```

Le projet couvre donc une logique complète de **rebalancing**, depuis l'identification du stock dormant jusqu'à la recommandation d'activation, en passant par l'analyse du coût complet, de la demande cible et de la rentabilité attendue.

---

## 🏢 Contexte métier

Certaines références vendent mal dans leur marché local alors qu'elles pourraient mieux performer dans un autre pays ou une autre zone.

### ⚡ Défis identifiés

Le problème n'est donc pas seulement commercial. Il est aussi opérationnel, logistique et financier :

- ✅ Un produit peut être plus demandé ailleurs
- ⚠️ Mais le transport peut dégrader la marge
- ⚠️ La douane peut rendre l'opération peu intéressante
- ⚠️ Le change peut compresser la rentabilité
- ⚠️ Le marché cible peut ne pas accepter le prix nécessaire
- ⚠️ Déplacer le stock trop souvent augmente le risque
- ⚠️ Une fois le stock arrivé dans une nouvelle zone, il faut encore gérer le dernier kilomètre jusqu'au point de vente ou au client final

### 🎲 Modèle retenu

Le modèle retenu est volontairement contraint :

| Contrainte | Description |
|------------|-------------|
| 📦 Stock local | Le stock est détenu localement par les boutiques partenaires |
| 🚫 Pas de rotation libre | Le stock ne tourne pas librement entre les points de vente |
| ✅ Activation contrôlée | Les produits ne bougent que lorsqu'une activation est validée |
| 🎯 Mécanisme unique | Les activations constituent l'unique mécanisme de redistribution contrôlée |
| 💰 Objectif économique | Améliorer la monétisation des stocks dormants sans créer de complexité logistique inutile |

---

## 🎯 Objectif

Construire un système analytique léger mais crédible capable de répondre à six questions centrales :

| # | Question métier | Sortie attendue |
|---|-----------------|-----------------|
| 1️⃣ | Quels produits stagnent suffisamment pour devenir des candidats au rebalancing ? | Score de santé du stock |
| 2️⃣ | Quels marchés sont les plus intéressants selon la demande, le prix et la volatilité ? | Score d'opportunité marché |
| 3️⃣ | Le coût complet reste-t-il acceptable une fois intégrés transport, douane, packaging, contrôle qualité et dernier kilomètre ? | Analyse de coût complet |
| 4️⃣ | Le marché cible supporte-t-il le prix requis après coût complet ? | Analyse de faisabilité prix |
| 5️⃣ | Quelles activations doivent être validées en priorité pour la prochaine opération ? | Recommandations d'activation |
| 6️⃣ | Ces décisions restent-elles rentables en cas de stress ? | Analyse de scénarios |

---

## 🏗️ Architecture

```text
blurry-weekly-drop-intelligence/
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
│   │   ├── fact_scenario.csv
│   │   ├── fx_rates.csv
│   │   ├── shipping_rates.csv
│   │   └── customs_rules.csv
│   │
│   ├── 📂 curated/
│   │   ├── stock_health_enriched.csv
│   │   ├── market_opportunity_enriched.csv
│   │   ├── pricing_enriched.csv
│   │   ├── activation_recommendation.csv
│   │   ├── scenario_analysis.csv
│   │   └── *_clean.csv
│   │
│   └── 📂 exports/
│       ├── approved_activations.csv
│       ├── rejected_activations.csv
│       └── scenario_summary.csv
│
└── 🐍 src/
    ├── load_data.py
    ├── data_quality_check.py
    ├── stock_health.py
    ├── market_opportunity.py
    ├── pricing.py
    ├── activation.py
    ├── scenarios.py
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
git clone https://github.com/yourusername/blurry-weekly-drop-intelligence.git
cd blurry-weekly-drop-intelligence
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
  - ✅ Simulation de scénarios de stress
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
| `fact_scenario.csv` | Hypothèses de stress | 📊 Fait |

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
# Fournit une vue d'ensemble du périmètre de travail
```

### 2️⃣ Contrôle qualité

```python
# Module: data_quality_check.py
# Vérifie:
#   ✓ Présence des colonnes attendues
#   ✓ Absence de valeurs nulles problématiques
#   ✓ Absence de doublons sur les clés pertinentes
#   ✓ Cohérence des clés entre tables
```

### 3️⃣ Analyse du stock

```python
# Module: stock_health.py
# Identifie les références présentant des signes de stagnation locale
```

**Signaux pris en compte :**

- 📅 Nombre de jours moyens en stock
- 🔄 Vitesse d'écoulement récente
- 📦 Quantité disponible
- ⚠️ Niveau de risque de stock

> **Point clé :** Cette étape correspond au point de départ du stock rebalancing : détecter les produits qui immobilisent du capital localement et qui méritent d'être étudiés pour une réallocation ponctuelle.

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

**Formule simplifiée :**

```
Coût complet = Prix d'achat 
             + Transport international
             + Douane
             + Packaging
             + Contrôle qualité
             + Buffer change
             + Coût de dernier kilomètre
```

> **Important :** Le dernier kilomètre doit être intégré à la logique économique. Même si le produit arrive dans un entrepôt ou une boutique cible, il reste un coût de mise à disposition finale : acheminement local, traitement terminal, préparation finale ou distribution courte distance.

**Validation du prix :**

Le système détermine si le prix nécessaire pour atteindre la marge cible reste compatible avec le marché observé.

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
| 💵 Coût cohérent | Coût complet final cohérent une fois intégré le dernier kilomètre |

> **Philosophie :** Cette logique ne cherche pas à maximiser tous les flux possibles. Elle cherche à recommander peu d'actions, mais des actions cohérentes et défendables.

### 7️⃣ Scénarios de stress

```python
# Module: scenarios.py
# Teste les activations validées sous différentes hypothèses de dégradation
```

**Scénarios testés :**

- 💱 Stress change
- 🚚 Stress transport
- 📉 Stress demande
- ⚠️ Scénario dégradé combiné

### 8️⃣ Export pour restitution

```python
# Module: dashboard_export.py
# Génère les tables finales exploitables dans:
#   - Excel
#   - Google Sheets
#   - Power BI
#   - Tout autre outil de BI
```

---

## 📈 Résultats attendus

Le projet permet de produire des conclusions du type :

```diff
+ Telle référence est prioritaire à activer car le stock est sous pression 
  et le marché cible absorbe le prix

- Telle activation doit être rejetée car le prix nécessaire dépasse 
  le niveau accepté par le marché

+ Certains marchés absorbent mieux les produits premium

+ Certaines activations restent rentables même dans un scénario dégradé

- D'autres deviennent trop sensibles au change, au transport ou 
  au dernier kilomètre

+ Certaines références ont surtout un intérêt de rebalancing, 
  pas uniquement de vente opportuniste
```

---

## 📏 Indicateurs suivis

### 📦 Indicateurs stock / activation

```yaml
Stock:
  - Nombre de références en situation de stagnation
  - Nombre d'activations éligibles
  - Volume candidat par activation

Décisions:
  - Activations approuvées vs rejetées
```

### 💰 Indicateurs prix / marge

```yaml
Coûts:
  - Coût complet
  - Prix recommandé
  - Écart entre prix recommandé et prix marché

Rentabilité:
  - Marge attendue
  - Faisabilité commerciale du prix
  - Poids du dernier kilomètre dans le coût total
```

### 📊 Indicateurs scénarios

```yaml
Performance:
  - Profit total par scénario
  - Marge unitaire moyenne par scénario
  - Nombre d'activations encore profitables

Robustesse:
  - Activations les plus résilientes
  - Activations les plus fragiles
```

---

## 📊 Dashboard

Les dashboards ne doivent pas être compris comme une simple couche visuelle ajoutée à la fin du projet.  
Ils servent à rendre lisible la logique métier du système décisionnel et à montrer comment les données soutiennent une décision de **stock rebalancing international**.

Dans ce projet, le bon angle n’est pas celui d’une marketplace classique.  
L’objectif n’est pas de piloter des mouvements de stock permanents entre plusieurs pays, mais d’identifier **quand un stock dormant doit être réalloué**, vers **quel marché**, à **quel niveau de coût complet**, et avec **quel niveau de robustesse économique**. Cette logique doit donc se retrouver directement dans les dashboards.

Autrement dit, les dashboards doivent répondre à une question simple :

> Quels produits faut-il sortir de leur marché local, vers quelle destination, à quel prix, et avec quelle marge attendue une fois intégrés le transport international, la douane, le packaging, le contrôle qualité et le dernier kilomètre ?

Le dernier kilomètre est important dans la lecture des résultats.  
Même lorsqu’une activation semble rentable au moment de l’expédition internationale, la profitabilité réelle peut encore être dégradée une fois le stock arrivé dans l’entrepôt ou la zone cible, car il faut ensuite financer l’acheminement final vers le point de vente, le point relais ou le client. Les dashboards doivent donc bien faire apparaître que la décision ne repose pas uniquement sur le prix de marché, mais sur un **coût complet réellement exploitable**.

Les pages recommandées ci-dessous ont été pensées pour raconter cette logique de manière progressive :
1. une vue synthétique des décisions,
2. une lecture opérationnelle du stock à rééquilibrer,
3. une lecture marché des destinations les plus pertinentes,
4. une lecture financière du coût complet et du pricing,
5. une lecture explicable du moteur de décision,
6. une lecture de robustesse via les scénarios de stress.

Le pipeline a été conçu de manière reproductible : les mêmes scripts peuvent être réexécutés avec un autre jeu de données structuré selon le même schéma, ce qui permet d’actualiser automatiquement les exports et, par extension, les dashboards. En revanche, les données utilisées ici restent un jeu de données de démonstration construit pour illustrer la logique métier du projet. Les visualisations produites sont donc cohérentes pour une preuve de concept, mais elles ne reflètent pas encore toute la richesse, la granularité ni la complexité d’un environnement réel à grande échelle.

### 📋 Dashboard 1 — Vue executive

Cette page doit permettre de comprendre en quelques secondes ce que le système recommande pour la prochaine vague d’activation.

Elle doit mettre en avant :
- le nombre total d’activations étudiées,
- le nombre d’activations approuvées,
- le nombre d’activations rejetées,
- le bénéfice total attendu,
- la marge moyenne attendue,
- les meilleures activations validées,
- les principaux motifs de rejet.

Cette page est utile pour un lecteur non technique, car elle résume immédiatement la sortie du moteur de décision.

<img width="2930" height="1694" alt="image" src="https://github.com/user-attachments/assets/988a4e3c-a2af-492d-98a2-90d9923b3ed5" />

---

### 📦 Dashboard 2 — Santé du stock et besoin de rebalancing

Cette page doit expliquer **pourquoi** certains produits deviennent des candidats au rebalancing.

Elle doit montrer :
- les jours moyens en stock,
- le taux d’écoulement à 30 jours,
- le score de risque stock,
- le statut du stock,
- le volume dormant par boutique ou localisation,
- les références les plus sous pression.

Cette page est essentielle car elle montre que la logique de départ vient d’un problème d’immobilisation locale du stock, et non d’une simple opportunité commerciale abstraite.

<img width="2906" height="1690" alt="image" src="https://github.com/user-attachments/assets/52df50a8-2870-498a-8db3-214fe9e3fe90" />


---

### 🌍 Dashboard 3 — Opportunité marché

Cette page doit répondre à la question : **où ce stock dormant a-t-il le plus de chances d’être mieux absorbé ?**

Elle doit mettre en avant :
- le score d’opportunité par produit et par pays,
- le score de demande,
- le score de tendance,
- le niveau de volatilité,
- le prix moyen observé,
- le niveau de priorité marché.

Cette page permet de visualiser les destinations les plus crédibles pour un rebalancing sélectif.

<img width="2904" height="1706" alt="image" src="https://github.com/user-attachments/assets/3e563330-6554-45f5-992c-9d825b9ae058" />


---

### 💰 Dashboard 4 — Pricing et coût complet

Cette page doit montrer qu’une décision de rebalancing n’a de sens que si le marché cible supporte un prix cohérent avec le coût complet réel.

Elle doit inclure :
- le prix d’achat,
- le coût de transport international,
- le coût de douane,
- le coût de packaging,
- le coût de contrôle qualité,
- le buffer FX,
- le coût du dernier kilomètre,
- le coût complet total,
- le prix recommandé,
- le prix moyen observé sur le marché,
- l’écart entre prix recommandé et prix de marché,
- le statut pricing.

C’est l’une des pages les plus importantes du rapport, car elle montre que la décision finale ne repose pas sur un simple arbitrage prix de vente / prix d’achat, mais sur une lecture réaliste de la rentabilité après tous les coûts opérationnels.

<img width="2894" height="1450" alt="image" src="https://github.com/user-attachments/assets/c2fc025b-3eda-4d43-bbf2-17f93c4e7a4f" />


---

### ✅ Dashboard 5 — Activation decision engine

Cette page doit rendre visible la logique finale d’approbation ou de rejet.

Elle doit faire apparaître :
- le score de risque stock,
- le score d’opportunité marché,
- la marge attendue,
- les unités candidates,
- le score final d’activation,
- la décision approuver / rejeter,
- la raison de décision.

Cette page permet de transformer le pipeline en système explicable.  
Elle montre qu’une activation n’est pas validée parce qu’un produit “semble intéressant”, mais parce qu’il passe une série de critères cohérents et auditables.

<img width="2902" height="1682" alt="image" src="https://github.com/user-attachments/assets/4f0e26af-1617-441e-a4e7-a20a6d1544eb" />

<img width="2918" height="1514" alt="image" src="https://github.com/user-attachments/assets/058917fd-f4c2-4944-ba5a-2e02c8177211" />

<img width="2930" height="1478" alt="image" src="https://github.com/user-attachments/assets/9f34dfbe-45f3-4f9a-8734-1c44b375b02f" />

Cette page est utile pour montrer qu’une recommandation n’est pas seulement rentable “sur le papier” dans un cas central, mais qu’elle conserve un intérêt même sous stress de demande, de change ou de logistique.


## 🔮 Évolutions possibles

### 🌐 Données externes

```yaml
APIs:
  - 💰 API prix marché ( Via l'API stock X ) 
  - 💱 API taux de change ( FX rates API ) 
  - 🚚 API transporteurs ( UPS campus par ex ) 
  
Signaux:
  - 📊 Signaux boutiques partenaires ( Produits qui dorment le plus en raison de leur valeur/demande ) 
  - 👥 Données de votes ou d'intérêt clients ( Via questionnaire de raffle ) 
  
Raffinements:
  - 🛃 Hypothèses douanières plus fines
  - 🚗 Coûts plus réalistes de dernier kilomètre par pays ou par zone urbaine
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
  - 📊 Dashboard Power BI
  - 🌍 Vues comparatives par marché
  - 📈 Waterfall de marge
  - 🗺️ Cartes pays
  - 📄 Exports PDF exécutifs
```

### 🧠 Approfondissements analytiques

```yaml
Modélisation:
  - 🎯 Score de confiance par marché
  - 📈 Forecast de demande
  - 📦 Contraintes de capacité par boutique
  - 🔧 Moteur d'optimisation plus avancé
  - ⚖️ Arbitrage automatique volume / marge / risque
  - 🚗 Segmentation plus fine des coûts de dernier kilomètre
```

---

## 💡 Intérêt du projet

Ce projet montre la capacité à :

```diff
+ Structurer un problème métier international
+ Raisonner en stock rebalancing plutôt qu'en simple vente opportuniste
+ Relier données, coûts et rentabilité
+ Intégrer les contraintes réelles de transport et de dernier kilomètre
+ Construire une logique de pricing à partir du coût complet
+ Produire des recommandations auditables
+ Maintenir un pipeline analytique reproductible
+ Restituer un sujet comme un profil data business orienté décision
```

> **Positionnement :** Le projet reste volontairement mesuré. Il ne cherche pas à simuler un système opérationnel complet, mais à démontrer une capacité de modélisation propre, crédible et utile.

---

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
