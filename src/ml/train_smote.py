import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate, KFold, StratifiedKFold
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
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

df = pd.read_csv('survey_lung_cancer.csv')

enc = LabelEncoder()
for col in df.columns:
    if df[col].dtype == object:
        df[col] = enc.fit_transform(df[col])

X = df.drop(columns=['LUNG_CANCER'])
y = df['LUNG_CANCER']

print("Before SMOTE:", dict(pd.Series(y).value_counts()))

models = {
    "Log":  LogisticRegression(max_iter=1000),
    "XGB":  XGBClassifier(eval_metric='logloss', verbosity=0),
    "LGBM": LGBMClassifier(verbose=-1),
    "CB":   CatBoostClassifier(verbose=0, iterations=1000, depth=8),
    "RF":   RandomForestClassifier(),
    "DT":   DecisionTreeClassifier(),
    "SVM":  SVC(),
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
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

for name, model in models.items():
    print(f"Training {name}...")
    # Pipeline: SMOTE inside each fold (correct way)
    pipe = Pipeline([('smote', SMOTE(random_state=42)), ('model', model)])

    res = cross_validate(pipe, X, y, cv=cv, scoring=scoring)
    row = {
        'Model': name,
        'MA':  round(np.mean(res['test_accuracy']),  3),
        'MP':  round(np.mean(res['test_precision']), 3),
        'MR':  round(np.mean(res['test_recall']),    3),
        'MF1': round(np.mean(res['test_f1']),        3),
    }
    results.append(row)
    print(f"  MA={row['MA']}  MP={row['MP']}  MR={row['MR']}  MF1={row['MF1']}")

print()
print("=== FINAL TABLE ===")
df_res = pd.DataFrame(results)
print(df_res.to_string(index=False))
df_res.to_csv('smote_results.csv', index=False)
print("\nSaved to smote_results.csv")
