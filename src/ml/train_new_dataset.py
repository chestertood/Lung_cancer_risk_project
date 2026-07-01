import pandas as pd
import numpy as np
from sklearn.model_selection import cross_validate, KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

df = pd.read_csv('lung_cancer_dataset.csv')
df = df.drop(columns=['patient_id'])

# Fill missing alcohol_consumption with mode
df['alcohol_consumption'] = df['alcohol_consumption'].fillna(df['alcohol_consumption'].mode()[0])

# Encode all categorical
enc = LabelEncoder()
for col in df.columns:
    if df[col].dtype == object:
        df[col] = enc.fit_transform(df[col])

X = df.drop(columns=['lung_cancer'])
y = df['lung_cancer']

print("Features:", list(X.columns))
print("Class distribution:", y.value_counts().to_dict())
print()

models = {
    "Log":  LogisticRegression(max_iter=1000),
    "XGB":  XGBClassifier(eval_metric='logloss', verbosity=0),
    "LGBM": LGBMClassifier(verbose=-1),
    "CB":   CatBoostClassifier(verbose=0, iterations=1000, depth=8),
    "RF":   RandomForestClassifier(),
    "DT":   DecisionTreeClassifier(),
    "SVM":  SVC(probability=True),
    "KNN":  KNeighborsClassifier(),
    "NB":   GaussianNB(),
}

scoring = {
    'accuracy':  make_scorer(accuracy_score),
    'precision': make_scorer(precision_score),
    'recall':    make_scorer(recall_score),
    'f1':        make_scorer(f1_score),
}

results = []
for name, model in models.items():
    print(f"Training {name}...")
    cv = cross_validate(model, X, y, cv=10, scoring=scoring)
    row = {
        'Model': name,
        'MA':  round(np.mean(cv['test_accuracy']),  3),
        'MP':  round(np.mean(cv['test_precision']), 3),
        'MR':  round(np.mean(cv['test_recall']),    3),
        'MF1': round(np.mean(cv['test_f1']),        3),
    }
    results.append(row)
    print(f"  MA={row['MA']}  MP={row['MP']}  MR={row['MR']}  MF1={row['MF1']}")

print()
print("=== FINAL TABLE ===")
df_res = pd.DataFrame(results)
print(df_res.to_string(index=False))
df_res.to_csv('new_dataset_results.csv', index=False)
print("\nSaved to new_dataset_results.csv")
