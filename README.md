# Stock Prediction: does news sentiment help predict S&P 500 direction?

Predicts whether the S&P 500 closes **Up or Down the next trading day**, and tests whether adding
FinBERT news sentiment improves on technical indicators alone.

## Pipeline

Run the notebooks in this order. Each reads the previous step's files from `data/`.

| Step | Notebook | Output |
|---|---|---|
| 1. Prices (yfinance, 2008-08-01 to 2016-07-01) | `yfinance.ipynb` | `data/sp500_raw.csv` |
| 2. Technical features and target (returns, RSI, MACD, volume change) | `features.ipynb` | `data/features.csv` |
| 3. FinBERT sentiment on the Kaggle DJIA headlines (49,700 headlines) | `sentiment.ipynb` | `data/headline_scores.csv`, `data/sentiment_daily.csv` |
| 4. Join, lag sentiment by one day, chronological 70/15/15 split | `fusion_split.ipynb` | `data/fused.csv`, `train.csv`, `val.csv`, `test.csv` |
| 5. Logistic Regression, Random Forest and XGBoost on three feature sets | `models.ipynb` | `data/results.csv` |
| 6. Live next-day forecast (technical indicators only, downloads fresh prices) | `tomorrow.ipynb` | printed forecast |

Input data: `data/Combined_News_DJIA.csv` (Kaggle "Daily News for Stock Market Prediction").

## Method

- **Feature sets:** numerical-only (7 columns), sentiment-only (3), multimodal (10).
- **No look-ahead:** the target is the only forward-looking column, sentiment is lagged one trading day,
  the split is chronological with no shuffling, and the scaler is fit on training rows only.
- **Tuning:** small grids with walk-forward `TimeSeriesSplit` (3 folds) scored by ROC-AUC.
  The test set is not used for any choice.

## Results (test set, 297 days, 2015-04-29 to 2016-06-30)

| Feature set | Model | Accuracy | ROC-AUC |
|---|---|---|---|
| numerical-only | Logistic Regression | 0.498 | 0.520 |
| numerical-only | Random Forest | 0.512 | 0.487 |
| numerical-only | XGBoost | 0.498 | 0.482 |
| sentiment-only | Logistic Regression | 0.505 | 0.524 |
| sentiment-only | Random Forest | 0.502 | 0.520 |
| sentiment-only | XGBoost | 0.478 | 0.500 |
| multimodal | Logistic Regression | 0.498 | 0.539 |
| multimodal | Random Forest | 0.512 | 0.483 |
| multimodal | XGBoost | 0.522 | 0.481 |

Majority-class baseline accuracy is 0.502, and the 95% margin of error on accuracy is about +/- 5.7 points.

## Conclusion

- Every model performs at chance level. Accuracy is about 0.48 to 0.52 against the 0.502 baseline,
  and balanced accuracy is about 0.50 (see `models.ipynb`, section 5.12).
- Most models predict "Up" on 80% to 99% of days. Their high recall and F1 (about 0.65) only reflect that bias.
- Adding sentiment changes ROC-AUC by less than 0.02 (+0.019 for the best model), well within the noise.
- Next-day S&P 500 direction is very hard to predict from daily technical indicators and headline sentiment alone.
  This is an honest negative result, not a pipeline bug.

## Demo forecast

`models.ipynb`, section 5.13, picks the multimodal model with the best validation ROC-AUC, refits it on
train plus validation, and predicts the direction after the last available day (2016-06-30). It gave
P(Up) = 0.517 (Up), and the actual outcome was Up. Given the results above, this is a demonstration of
the pipeline and not a trading signal. The data ends in 2016, so no live "tomorrow" forecast is possible
without refreshing the price and news data.

## Live forecast for tomorrow

`tomorrow.ipynb` downloads recent S&P 500 prices with yfinance, rebuilds the technical features (checked to
match `data/features.csv` exactly), and predicts the next trading day with the numerical-only Logistic
Regression. Sentiment is not used because the news data ends in 2016 and there is no live headline source.
Latest run: last close 2026-11-13, P(Up) = 0.561 (Up). This is still a near coin-flip, not a trading signal.

Presentation notes and likely questions are in `PRESENTATION.md`.

## Setup

Python 3.13+ with `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`, `yfinance`, `torch` and
`transformers` (the first `sentiment.ipynb` run downloads `ProsusAI/finbert`; scoring all headlines takes
about 5 minutes on a GPU and 20 to 60 minutes on a CPU).
