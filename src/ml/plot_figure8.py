import matplotlib.pyplot as plt
import numpy as np

models = ['Log', 'XGB', 'LGBM', 'CB', 'RF', 'DT', 'SVM', 'KNN', 'NB']

accuracy  = [0.929, 0.900, 0.900, 0.906, 0.903, 0.887, 0.479, 0.871, 0.900]
precision = [0.960, 0.938, 0.938, 0.948, 0.941, 0.945, 0.925, 0.947, 0.920]
recall    = [0.959, 0.948, 0.948, 0.944, 0.948, 0.926, 0.441, 0.904, 0.970]
f1        = [0.959, 0.942, 0.942, 0.945, 0.944, 0.934, 0.588, 0.924, 0.944]

x = np.arange(len(models))
width = 0.2

fig, ax = plt.subplots(figsize=(12, 6))

bars1 = ax.bar(x - 1.5*width, accuracy,  width, label='Accuracy',  color='#4472C4')
bars2 = ax.bar(x - 0.5*width, precision, width, label='Precision', color='#ED7D31')
bars3 = ax.bar(x + 0.5*width, recall,    width, label='Recall',    color='#70AD47')
bars4 = ax.bar(x + 1.5*width, f1,        width, label='F1 Score',  color='#FFC000')

ax.set_ylim(0.3, 1.05)
ax.set_title('Performance Comparison of ML Models on\nClinical Lung Cancer Dataset', fontsize=13, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=10)
ax.yaxis.set_tick_params(labelsize=9)
ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('Figure8_new.png', dpi=200, bbox_inches='tight')
print("Saved: Figure8_new.png")
plt.show()
