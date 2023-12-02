"""
此檔為訓練模型的主要程式，我們先將data區分為training與validation兩部分
接著使用gridsearch找出最適合參數(由於已經search過只填入目前最佳參數)，然後使用XGB訓練模型，並使用model預測被盜刷的機率
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import numpy as np

def calculate_f1_score(y_true, y_pred):
    """
    在給定正確答案與預測結果後，此函式會幫忙計算f1 score
    """
    a_count = sum((y_true == 0) & (y_pred == 0))
    b_count = sum((y_true == 0) & (y_pred == 1))
    c_count = sum((y_true == 1) & (y_pred == 0))
    d_count = sum((y_true == 1) & (y_pred == 1))

    print(a_count)
    print(b_count)
    print(c_count)
    print(d_count)

    if b_count + d_count == 0:
        precision = 0
    else:
        precision = d_count / (b_count + d_count)

    print("precision:")
    print(precision)
    
    if d_count + c_count == 0:
        recall = 0
    else:
        recall = d_count / (d_count + c_count)

    if precision + recall == 0:
        return 0.0
    f1 = 2 * (precision * recall) / (precision + recall)

    print("recall:")
    print(recall)

    return f1

# Load the training data
print("Load the training data")
train_data = pd.read_csv("train_time_myf_cano_moref_conam_null_group_dup2.csv")

selected_columns = [
    'chid', 'cano', 'contp', 'etymd', 'mchno', 'acqic', 'mcc', 'conam', 'ecfg', 'insfg',
    'iterm', 'bnsfg', 'flam1', 'stocn', 'scity', 'stscd', 'ovrlt', 'flbmk', 'hcefg', 'csmcu', 'csmam', 'flg_3dsmk',
    'hour', 'cano_all_combined', 'cano_5', 'cano_20', 
    'cano_locdt', 'cano_locdt_freq', 'cano_locdt_sigma', 'chid_mchno', 'cano_locdt_conam_max', 'cano_locdt_conam_min'
]

print(selected_columns)

# Separate features (X) and labels (y)
X = train_data[selected_columns]
y = train_data["label"]

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.01, random_state=55)

# Initialize the XGBoost classifier
xgb_model = XGBClassifier(objective='binary:logistic', random_state=66, reg_alpha=1, reg_lambda=1)

# Define a parameter grid for hyperparameter tuning
param_grid = {
    'n_estimators': [300],
    'learning_rate': [0.05], # bigger, more 1s？
    'max_depth': [32], # bigger, more 1s, more overfitting
    'subsample': [1],
    'colsample_bytree': [1]
}

# Use GridSearchCV to find the best hyperparameters
print("Use GridSearchCV to find the best hyperparameters")
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring='f1', cv=3)
grid_search.fit(X_train, y_train)

# Get the best model
best_xgb_model = grid_search.best_estimator_

# Make predictions on the training set with adjusted threshold
y_train_prob = best_xgb_model.predict_proba(X_train)[:, 1]
threshold = 0.25
print(threshold)
y_train_pred_adjusted = (y_train_prob > threshold).astype(int)

# Calculate F1 score on the training set with adjusted threshold
f1_train_adjusted = calculate_f1_score(y_train, y_train_pred_adjusted)
print("train:")
print(f'Number of 0s in training data: {len(y_train) - y_train.sum()}')
print(f'Number of 1s in training data: {y_train.sum()}')
print(f'F1-score on training data (E_in) with adjusted threshold: {f1_train_adjusted}')
print(f"Training F1 Score: {f1_train_adjusted:.4f}")

# Make predictions on the validation set with adjusted threshold
y_val_prob = best_xgb_model.predict_proba(X_val)[:, 1]
y_val_pred_adjusted = (y_val_prob > threshold).astype(int)

# Calculate F1 score on the validation set with adjusted threshold
f1_val_adjusted = calculate_f1_score(y_val, y_val_pred_adjusted)
print("val:")
print(f'Number of 0s in validation data: {len(y_val) - y_val.sum()}')
print(f'Number of 1s in validation data: {y_val.sum()}')
print(f'F1-score on validation data (E_out) with adjusted threshold: {f1_val_adjusted}')
print(f"Validation F1 Score: {f1_val_adjusted:.4f}")

# Load the test data
test_data = pd.read_csv("test_time_myf_cano_moref_conam_null_group.csv")

# Separate features from the test set
X_test = test_data[selected_columns]

# Make predictions on the test set with adjusted threshold
y_test_prob = best_xgb_model.predict_proba(X_test)[:, 1]
y_test_pred_adjusted = (y_test_prob > threshold).astype(int)

print(f'Number of 0s predicted in testing data: {len(y_test_pred_adjusted) - y_test_pred_adjusted.sum()}')
print(f'Number of 1s predicted in testing data: {y_test_pred_adjusted.sum()}')

# Create a DataFrame with 'txkey' and 'pred' columns
output_df = pd.DataFrame({'txkey': test_data['txkey'], 'pred': y_test_pred_adjusted})

# Save the results to a CSV file for submission
output_df.to_csv('xgb.csv', index=False)
# output_df.to_csv('xgb2_debug.csv', index=False)
print("Predictions for the test data have been saved to xgb.csv.")
