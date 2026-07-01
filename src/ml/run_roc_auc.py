# -*- coding: utf-8 -*-
"""
ROC-AUC for all 9 ML models — 10-fold StratifiedKFold + SMOTE within fold.
Matches paper methodology exactly.
"""
import sys, warnings
sys.stdout.reconfigure(encoding='utf-8')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE

# ── Load & preprocess ──────────────────────────────────────────────────────
df = pd.read_csv('survey_lung_cancer.csv')
df.columns = df.columns.str.strip()
df['GENDER']      = LabelEncoder().fit_transform(df['GENDER'])       # M=1, F=0
df['LUNG_CANCER'] = (df['LUNG_CANCER'] == 'YES').astype(int)

X = df.drop('LUNG_CANCER', axis=1).values
y = df['LUNG_CANCER'].values

# ── Models (same hyperparams as paper's best config) ──────────────────────
models = {
    'Logistic Regression (Log)': LogisticRegression(max_iter=1000, random_state=42),
    'XGBoost (XGB)':             XGBClassifier(eval_metric='logloss', random_state=42, verbosity=0),
    'LightGBM (LGBM)':           LGBMClassifier(random_state=42, verbose=-1),
    'CatBoost (CB)':             CatBoostClassifier(iterations=1000, depth=8, learning_rate=0.05,
                                                     random_state=42, verbose=0),
    'Random Forest (RF)':        RandomForestClassifier(random_state=42),
    'Decision Tree (DT)':        DecisionTreeClassifier(random_state=42),
    'SVM':                       SVC(probability=True, random_state=42),
    'KNN':                       KNeighborsClassifier(),
    'Naive Bayes (NB)':          GaussianNB(),
}

# ── 10-fold StratifiedKFold + SMOTE inside fold ───────────────────────────
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

print(f'{"Model":<30} {"Mean AUC":>10} {"Std":>8}')
print('-' * 52)

results = {}
for name, model in models.items():
    fold_aucs = []
    for train_idx, test_idx in skf.split(X, y):
        X_tr, X_te = X[train_idx], X[test_idx]
        y_tr, y_te = y[train_idx], y[test_idx]

        # SMOTE only on training fold
        sm = SMOTE(random_state=42)
        X_tr_res, y_tr_res = sm.fit_resample(X_tr, y_tr)

        model.fit(X_tr_res, y_tr_res)
        proba = model.predict_proba(X_te)[:, 1]
        fold_aucs.append(roc_auc_score(y_te, proba))

    mean_auc = np.mean(fold_aucs)
    std_auc  = np.std(fold_aucs)
    results[name] = (mean_auc, std_auc)
    print(f'{name:<30} {mean_auc:>10.4f} {std_auc:>8.4f}')

print()
best = max(results, key=lambda k: results[k][0])
print(f'Best: {best} — AUC {results[best][0]:.4f}')

# ── Save to CSV ───────────────────────────────────────────────────────────
rows = [{'Model': k, 'Mean AUC': round(v[0],4), 'Std AUC': round(v[1],4)}
        for k,v in results.items()]
pd.DataFrame(rows).to_csv('ml_roc_auc_results.csv', index=False)
print('\nSaved: ml_roc_auc_results.csv')
