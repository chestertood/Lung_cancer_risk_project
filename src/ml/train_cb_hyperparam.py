import pandas as pd
import numpy as np
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
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

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
scoring = {
    'accuracy':  make_scorer(accuracy_score),
    'precision': make_scorer(precision_score),
    'recall':    make_scorer(recall_score),
    'f1':        make_scorer(f1_score),
}

def run_sweep(param_name, param_values, fixed_params):
    results = []
    for val in param_values:
        params = dict(fixed_params)
        params[param_name] = val
        model = CatBoostClassifier(verbose=0, **params)
        pipe = Pipeline([('smote', SMOTE(random_state=42)), ('model', model)])
        res = cross_validate(pipe, X, y, cv=cv, scoring=scoring)
        row = {
            param_name: val,
            'MA':  round(np.mean(res['test_accuracy']),  3),
            'MP':  round(np.mean(res['test_precision']), 3),
            'MR':  round(np.mean(res['test_recall']),    3),
            'MF1': round(np.mean(res['test_f1']),        3),
        }
        results.append(row)
        print(f"  {param_name}={val}  MA={row['MA']}  MP={row['MP']}  MR={row['MR']}  MF1={row['MF1']}")
    return pd.DataFrame(results)

# Table 3: Iterations (fixed depth=8, eta=0.05)
print("=== Table 3: Iterations ===")
t3 = run_sweep('iterations', [100, 200, 500, 1000, 2000],
               fixed_params={'depth': 8, 'learning_rate': 0.05})

# Table 4: Eta / Learning Rate (fixed iterations=1000, depth=8)
print("\n=== Table 4: Eta ===")
t4 = run_sweep('learning_rate', [0.01, 0.05, 0.15, 0.20, 0.30],
               fixed_params={'iterations': 1000, 'depth': 8})

# Table 5: Depth (fixed iterations=1000, eta=0.05)
print("\n=== Table 5: Depth ===")
t5 = run_sweep('depth', [2, 4, 6, 8, 10],
               fixed_params={'iterations': 1000, 'learning_rate': 0.05})

print("\n=== RESULTS ===")
print("Table 3 - Iterations:")
print(t3.to_string(index=False))
print("\nTable 4 - Eta:")
print(t4.rename(columns={'learning_rate': 'Eta'}).to_string(index=False))
print("\nTable 5 - Depth:")
print(t5.to_string(index=False))

# Save
with pd.ExcelWriter('cb_hyperparam_results.xlsx') as writer:
    t3.to_excel(writer, sheet_name='Table3_Iterations', index=False)
    t4.rename(columns={'learning_rate': 'Eta'}).to_excel(writer, sheet_name='Table4_Eta', index=False)
    t5.to_excel(writer, sheet_name='Table5_Depth', index=False)

print("\nSaved: cb_hyperparam_results.xlsx")
