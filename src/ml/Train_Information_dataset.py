import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,cross_validate,KFold
from sklearn.preprocessing import LabelEncoder,StandardScaler, OneHotEncoder
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, StackingClassifier,RandomTreesEmbedding
from sklearn import tree, svm, neighbors,naive_bayes
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv('survey_lung_cancer.csv')
print(df.head())
print(df.isna().sum())

e = np.e
x = -6.8272+ (0.0391 * df['AGE']) + (0.7917 * df['SMOKING_HISTORY']) + (1.3388 * df['CANCER_HISTORY']) + (0.1274 * df['DIAMETER_OF_NODULES/MASS']) + (1.0407 * df['SPICULATION']) + (0.7838 * df['UPPER_LOBE'])
Probability_cancer = (e**x) / (1 + e**x)



Encoder = LabelEncoder()
for i in df.columns:
    if i != 'AGE' :
        df[f"{i}"] = Encoder.fit_transform(df[f"{i}"])

X = df.drop(columns=['LUNG_CANCER'])
y = df['LUNG_CANCER']

# plt.figure(figsize=(10,6))
# sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
# plt.show()

# X = StandardScaler().fit_transform(X)
# print(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


models = {
    # "Log": LogisticRegression(max_iter=1000),
    # "XGB": XGBClassifier(eval_metric='logloss'),
    # "LGBM": LGBMClassifier(),
    "CatBoost": CatBoostClassifier(verbose=0,depth=10),
    # "RandomForest": RandomForestClassifier(),
    # "DecisionTree": tree.DecisionTreeClassifier(),
    # "SVM": svm.SVC(probability=True),
    # "KNN": neighbors.KNeighborsClassifier(),
    # "NaiveBayes": naive_bayes.GaussianNB()
}

excel_file = {"Name_model": [], "Mean Accuracy": [], "Mean Precision": [], "Mean Recall": [], "Mean F1 Score": []}


for name,item in models.items():
    item.fit(X_train, y_train)
for name,item in models.items():
    print(f"Accuracy_{name}: {item.score(X_test, y_test)}")
results = {}
for name,item in models.items():
    cv_results = cross_validate(item, X, y, cv=10, scoring={
        'accuracy': make_scorer(accuracy_score),
        'precision': make_scorer(precision_score),
        'recall': make_scorer(recall_score),
        'f1': make_scorer(f1_score)
    })
    print(f"\n{name} Cross-Validation Results:")
    print(f"Mean Accuracy: {np.mean(cv_results['test_accuracy']):.9f}")
    print(f"Mean Precision: {np.mean(cv_results['test_precision']):.9f}")
    print(f"Mean Recall: {np.mean(cv_results['test_recall']):.9f}")
    print(f"Mean F1 Score: {np.mean(cv_results['test_f1']):.9f}")    
    results[name] = cv_results['test_accuracy'].mean()

    excel_file["Name_model"].append(name)
    excel_file["Mean Accuracy"].append(np.mean(cv_results['test_accuracy']))
    excel_file["Mean Precision"].append(np.mean(cv_results['test_precision']))
    excel_file["Mean Recall"].append(np.mean(cv_results['test_recall']))
    excel_file["Mean F1 Score"].append(np.mean(cv_results['test_f1']))

# save_excel = pd.DataFrame(excel_file)
# save_excel.to_csv('model_evaluation_results.csv', index=False)
# best_model_name = max(results, key=results.get)
# best_model = models[best_model_name]
# print(f"\n✅ โมเดลที่ดีที่สุดคือ: {best_model_name}")

# for name,item in models.items():
#     item.fit(X_train, y_train)
#     score = item.score(X_test, y_test)
#     print(f"✅ {name} model accuracy: {score}")

# for name,item in models.items():
#     joblib.dump(item, f'{name}_model.pkl')
#     print(f"✅ Saved {name} model successfully!")

# print("✅ Saved all trained models successfully!")

# model = joblib.load('Log_model.pkl')
# Test = model.predict([[1,90,1,1,1,1,1,0,0,0,0,0,0,1,0]])
# confidence = model.predict_proba([[1,90,1,1,1,1,1,0,0,0,0,0,0,1,0]])
# print("Test Prediction:", Test , confidence[0][1])

