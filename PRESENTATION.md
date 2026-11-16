# Presentation notes

## One-sentence summary
We tested whether adding news sentiment (FinBERT) to technical indicators helps predict the S&P 500's next-day
direction. It does not: every model performs at chance, and that is a valid, honestly measured result.

## Suggested slide flow

1. **Question:** can news sentiment improve next-day Up/Down prediction compared with price indicators alone?
2. **Data:** S&P 500 prices (yfinance, 2008 to 2016, 1994 days) and 49,700 Reddit world-news headlines
   (Kaggle, Combined_News_DJIA).
3. **Features:** 7 technical (1-day and 5-day return, RSI, MACD x3, volume change) and 3 sentiment
   (mean positive, negative and neutral FinBERT probability per day).
4. **Avoiding cheating (look-ahead):**
   - target is tomorrow's direction, used only as the label
   - sentiment lagged one trading day
   - chronological split 70/15/15, no shuffling
   - scaler fit on training data only
   - tuning with walk-forward `TimeSeriesSplit`, test set never used for choices
5. **Models:** Logistic Regression, Random Forest, XGBoost on 3 feature sets = 9 experiments.
6. **Results:** table in `README.md` (accuracy 0.48 to 0.52, ROC-AUC 0.48 to 0.54).
7. **Interpretation:** see the talking points below.
8. **Live demo:** `tomorrow.ipynb` (technical-only forecast for the next trading day).
9. **Conclusion and limits.**

## Talking points

- **Baseline:** always predicting "Up" gives 0.502 accuracy on the test set. No model beats it by more than
  the 5.7-point margin of error (297 test days).
- **High F1 and recall are misleading.** Most models predict "Up" on 80% to 99% of days, so recall is high and
  F1 is about 0.65, but balanced accuracy is about 0.50. This is shown in `models.ipynb`, section 5.12.
- **Sentiment effect:** +0.019 ROC-AUC for the best model, within the noise. Random Forest and XGBoost
  changed by -0.004 and -0.001.
- **Why it is hard:** the market is close to efficient for next-day direction, daily indicators are public and
  already priced in, and news headlines are noisy and world-news focused (not company or market specific).
- **Why we trust the process:** strict chronological evaluation. A model that had cheated with look-ahead would
  have shown a much higher score, and that would have been the suspicious result.

## "Can you predict tomorrow?"

**Short answer:** the pipeline can produce a forecast for tomorrow, but it has no real edge, and we say so.

- `tomorrow.ipynb` downloads the latest S&P 500 prices, rebuilds the same indicators (checked to match the
  training features exactly), and predicts the next trading day with Logistic Regression.
- Latest run: last close 2026-11-13 at 7561.67, P(Up) = 0.561, so "Up". The historical range of this model's
  P(Up) is 0.35 to 0.69, so 0.56 is a weak, near-coin-flip signal.
- **Why not the full multimodal model?** The Kaggle news data ends in 2016 and there is no live headline feed
  in the project, so sentiment cannot be computed for today. Sentiment gave almost no gain anyway.
- **To make it fully live (future work):** add a news API, score headlines with FinBERT daily, lag by one day,
  retrain on recent years.

## Likely questions and answers

- *Why is accuracy only about 50%?* Next-day direction is close to random. A real edge here would be surprising,
  and the study confirms that.
- *Did you try to improve it until it looked good?* No. The grids are small on purpose and the test set was
  never used for choices. Tuning on the test set would give a higher but meaningless number.
- *Could deep learning do better?* Possibly slightly, but with about 2,000 daily samples it would likely overfit.
- *Is sentiment useless?* Not necessarily. This news source (global Reddit headlines) is only loosely related
  to the market. Company-specific financial news, or predicting volatility instead of direction, might work better.
- *Should anyone trade on this?* No.
