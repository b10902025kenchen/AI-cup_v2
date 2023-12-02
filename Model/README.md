- 模型訓練：此資料夾只包含一個程式XGB.py，先將資料分成training set與validation set，接著使用XGB訓練模型，最後預測結果

- 參數設定：
    - reg_alpha, reg_lambda = 1
    - n_estimators = 300
    - learning_rate = 0.05
    - max_depth = 32
    - subsample, colsample_bytree = 1
    - threshold = 0.25 (我們會預測盜刷的機率，如果高於0.25即認定為盜刷)
