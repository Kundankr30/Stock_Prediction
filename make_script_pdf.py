"""Builds Presentation_Script.pdf (4-speaker script) with reportlab.

Run:  .venv_run/bin/python make_script_pdf.py
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

OUT = Path(__file__).parent / "Presentation_Script.pdf"
INDIGO = colors.HexColor("#5D65BB")
TINT = colors.HexColor("#E2E4F5")
DARK = colors.HexColor("#181818")
GRAY = colors.HexColor("#6B6B6B")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=20, textColor=DARK,
                    alignment=TA_LEFT, spaceAfter=4)
SUB = ParagraphStyle("Sub", parent=ss["Normal"], fontSize=10.5, textColor=GRAY, spaceAfter=8)
SPK = ParagraphStyle("Spk", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, textColor=colors.white,
                     backColor=INDIGO, borderPadding=(5, 6, 5, 6), spaceBefore=6, spaceAfter=10, leading=19)
SL = ParagraphStyle("Sl", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, textColor=INDIGO,
                    spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("Body", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5, leading=15.5,
                      textColor=DARK, spaceAfter=3)
BUL = ParagraphStyle("Bul", parent=BODY, leftIndent=16, bulletIndent=5, spaceAfter=1.5)
CELL = ParagraphStyle("Cell", parent=BODY, fontSize=9.5, leading=12.5, spaceAfter=0)
CELLB = ParagraphStyle("CellB", parent=CELL, fontName="Helvetica-Bold")
CELLH = ParagraphStyle("CellH", parent=CELLB, textColor=colors.white)
NOTE = ParagraphStyle("Note", parent=BODY, fontSize=9.5, textColor=GRAY)


def table(rows, widths, header=True):
    data = [[Paragraph(c, CELLH if (header and i == 0) else (CELLB if j == 0 else CELL))
             for j, c in enumerate(r)] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9CBE0")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TINT])]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), INDIGO))
    t.setStyle(TableStyle(st))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(2 * cm, 1.2 * cm, "Stock Trend Prediction using Machine Learning - Presentation Script")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


story = [
    Paragraph("Presentation Script (4 Speakers)", H1),
    Paragraph("Stock Trend Prediction using Machine Learning | Silicon University | Supervisor: "
              "Dr. Pradipta Kumar Pattanayak | Total time: about 10 to 12 minutes", SUB),
    HRFlowable(width="100%", thickness=1, color=INDIGO, spaceAfter=8),
    Paragraph("Team: Kundan Kumar (SIC-24BCSG85), Soham Mohanty (SIC-24BCSD49), Priyanshu Sekhar Badhei "
              "(SIC-24BCSF35), Naman Verma (SIC-24BCSF15), Tejash Arya (SIC-24BCSG63). Write each member's name "
              "against a speaker below.", BODY),
    Spacer(1, 6),
    table([["Speaker", "Slides", "Part", "Presenter name"],
           ["Speaker 1", "1 to 4", "Introduction, motivation, problem, literature gaps", "__________________"],
           ["Speaker 2", "5 to 8", "Data, pipeline, features, look-ahead controls", "__________________"],
           ["Speaker 3", "9 to 12", "Models, results, ROC curves, confusion matrices", "__________________"],
           ["Speaker 4", "13 to 15", "Sentiment effect, demo forecast, conclusion", "__________________"]],
          [2.3 * cm, 2.0 * cm, 8.2 * cm, 4.5 * cm]),
    Spacer(1, 6),
]


def speaker(title):
    story.append(Paragraph(title, SPK))


def slide(title, text):
    story.append(KeepTogether([Paragraph(title, SL), Paragraph(text, BODY)]))


def slide_bullets(title, intro, items, outro=None):
    block = [Paragraph(title, SL), Paragraph(intro, BODY)]
    block += [Paragraph(it, BUL, bulletText="\u2022") for it in items]
    if outro:
        block.append(Paragraph(outro, BODY))
    story.append(KeepTogether(block))


# ------------------------------------------------------------------ Speaker 1
speaker("Speaker 1 - Slides 1 to 4")
slide("Slide 1: Title",
      "\"Good morning everyone, respected sir and fellow students. We are Kundan Kumar, Soham Mohanty, Priyanshu "
      "Sekhar Badhei, Naman Verma and Tejash Arya from the Department of Computer Science and Engineering, "
      "Silicon University. Our project, under the guidance of Dr. Pradipta Kumar Pattanayak, is <i>Stock Trend "
      "Prediction using Machine Learning</i>. We ask one question: does news sentiment help predict the S&amp;P "
      "500's next-day direction?\"")
slide("Slide 2: Motivation",
      "\"Investors have two kinds of information. The first is numerical data: prices, volume and indicators "
      "like RSI and MACD. These are public and cheap, but they do not say why prices move. The second is text: "
      "news headlines that shape investor mood. FinBERT, a language model trained on financial text, turns a "
      "headline into positive, negative and neutral probabilities, so a normal classifier can use it. Most "
      "studies use only one of these. We combine both and measure what each one adds.\"")
slide_bullets("Slide 3: Problem and objectives",
              "\"Our problem is a binary classification. Given everything known at the close of day t, will the "
              "S&amp;P 500 close higher on day t+1? If yes, the label is 1, otherwise 0. This is hard by design, "
              "because the efficient market hypothesis says prices already reflect public information. Our six "
              "objectives are:\"",
              ["building the numerical features", "scoring headlines with FinBERT",
               "fusing them without leaking the future", "tuning three models",
               "evaluating on a later test period against a baseline",
               "comparing numerical-only, sentiment-only and multimodal features"],
              "\"We study the S&amp;P 500 index at daily frequency. We do not test any trading strategy.\"")
slide_bullets("Slide 4: Gaps in existing work",
              "\"We reviewed three recent studies and found four gaps.\"",
              ["<b>Single modality:</b> most use one modality, so the value of each is never isolated.",
               "<b>No baseline:</b> one study reports 57% accuracy, but without a baseline you cannot tell if "
               "that is good.",
               "<b>Leaky splits:</b> one preprint reports 100% on a static split with no temporal separation, "
               "and even its author suspects leakage.",
               "<b>Narrow metrics:</b> accuracy alone hides class bias."],
              "\"Our design addresses all four. Now my teammate will explain the data and method.\"")

# ------------------------------------------------------------------ Speaker 2
speaker("Speaker 2 - Slides 5 to 8")
slide("Slide 5: Data sources",
      "\"We use two datasets. Market data is the S&amp;P 500 from Yahoo Finance through yfinance, from August "
      "2008 to July 2016. News data is the Kaggle dataset <i>Daily News for Stock Market Prediction</i>, with "
      "the top 25 Reddit world-news headlines each day, about 49,700 in total. We cleaned them by removing the "
      "b'..' wrapper, very short headlines and daily duplicates. After joining the two sources we have 1,978 "
      "trading days. We split them chronologically 70/15/15, giving 1,384 training days, 297 validation days "
      "and 297 test days. The test period runs from April 2015 to June 2016.\"")
slide("Slide 6: Pipeline",
      "\"This is our architecture, with two branches. In the top branch, market data becomes seven technical "
      "features. In the bottom branch, each headline goes through FinBERT, and the scores are averaged into "
      "three daily sentiment features. We join them on date and lag the sentiment by one trading day. That "
      "gives 7 plus 3, or 10 features. We then split the data in time order, tune three models, and evaluate "
      "once on the test period. This is called early fusion, because we combine the features before the "
      "classifier.\"")
slide("Slide 7: Features",
      "\"The technical features are 1-day and 5-day returns; RSI, a 14-day momentum measure from 0 to 100; "
      "MACD, its signal line and histogram, scaled as a percentage of price; and volume change. The sentiment "
      "features are the daily means of FinBERT's positive, negative and neutral probabilities. We keep the soft "
      "probabilities, because a score of 0.52 and one of 0.98 carry different information. This gives three "
      "feature sets: numerical-only with 7 features, sentiment-only with 3, and multimodal with 10. With three "
      "models, that makes nine experiments.\"")
slide_bullets("Slide 8: Look-ahead bias",
              "\"This is our main contribution. Predicting the next day is close to a coin flip, so a very high "
              "score would actually be suspicious. We use six safeguards:\"",
              ["a chronological split with no shuffling",
               "a one-day sentiment lag, applied after the join so Mondays do not misalign",
               "a scaler fitted on training data only",
               "walk-forward tuning with TimeSeriesSplit, where the test set is never used",
               "sanity checks, such as an assertion that no feature correlates with the target at 0.2 or more",
               "an honest baseline, always predicting Up, at 50.2%, with a margin of error of plus or minus "
               "5.7 points"],
              "\"Next, my teammate will present the models and results.\"")

# ------------------------------------------------------------------ Speaker 3
speaker("Speaker 3 - Slides 9 to 12")
slide("Slide 9: Models",
      "\"We train three models. Logistic Regression is linear and hard to overfit, so it is a strong baseline "
      "for noisy data. Random Forest uses many bagged trees and captures interactions. XGBoost uses boosted "
      "trees, is flexible, but can fit noise. We kept the search grids small on purpose, because we have only "
      "about 1,400 training days. Large grids would mostly overfit the validation folds. Each model is tuned "
      "with walk-forward cross-validation, refit on the full training set, and tested once. All seeds are "
      "fixed to 42.\"")
slide("Slide 10: Results",
      "\"Here are all nine experiments on the 297-day test set. Accuracy ranges from 47.8% to 52.2%, and "
      "ROC-AUC from 0.481 to 0.539. The baseline is 50.2%, and the margin of error is about plus or minus 5.7 "
      "points. So every accuracy is within noise of the baseline. The best AUC, 0.539, is multimodal Logistic "
      "Regression, and even that cannot be separated from chance, because AUC uncertainty here is about plus "
      "or minus 0.06. The F1 scores of about 0.65 look good, but they are misleading, as the next slides "
      "show.\"")
slide("Slide 11: ROC curves",
      "\"These are the ROC curves for the three feature sets. The dashed diagonal is a coin flip, and almost "
      "every curve stays on or near it. ROC-AUC is the probability that a random Up day gets a higher score "
      "than a random Down day. 0.5 means no skill. Our values of 0.48 to 0.54 are essentially at chance.\"")
slide("Slide 12: Confusion matrices",
      "\"Why is F1 high if the models have no skill? The confusion matrices explain it. Most models predict Up "
      "on nearly every day. Eight of the nine predict Up on over 75% of days, and numerical-only Logistic "
      "Regression predicts Up on 296 of 297 days. That produces high recall and an F1 of about 0.65. But a "
      "model that always says Up gets recall 1.0 and F1 of 0.67, so this is just bias. Balanced accuracy, "
      "which treats both classes equally, is about 0.50 for every model. That means no skill. Now my teammate "
      "will cover the sentiment effect and the conclusion.\"")

# ------------------------------------------------------------------ Speaker 4
speaker("Speaker 4 - Slides 13 to 15")
slide("Slide 13: Does sentiment help?",
      "\"This is our core question. The best multimodal AUC is 0.539, and the best numerical-only AUC is "
      "0.520, a gain of just 0.019. That is well within the noise. For Random Forest and XGBoost, adding "
      "sentiment changed AUC by minus 0.004 and minus 0.001. The feature importance chart shows no dominant "
      "sentiment feature. Why is it hard? The market is close to efficient for next-day direction, the "
      "indicators are public and already priced in, and Reddit world-news headlines are noisy and not "
      "finance-specific. And we trust this result because a leaky pipeline would have shown a much higher "
      "score.\"")
slide("Slide 14: Demo forecast",
      "\"To show how the pipeline works on live data, our tomorrow.ipynb notebook downloads fresh prices, "
      "rebuilds the same indicators, and predicts the next trading day. The last close was 7,561.67 on 13 "
      "November 2026, and the model gave a probability of Up of 0.561. We use technical features only, because "
      "our news data ends in 2016 and we have no live headline feed. The model's historical range is 0.348 to "
      "0.686, so 0.561 is a near-neutral signal. This is a demonstration of the procedure, not a trading "
      "signal.\"")
slide_bullets("Slide 15: Conclusion",
              "\"To conclude, none of the nine models showed predictive skill. Accuracy was at the 50% baseline, "
              "and sentiment added only 0.019 AUC, which is within noise. This is consistent with the efficient "
              "market hypothesis. The value of our project is the evaluation design, which makes this negative "
              "result trustworthy. The limitations are a single rising test period, Reddit-only headlines, and "
              "no trading costs. For future work we would:\"",
              ["add a live finance-specific news feed", "fine-tune FinBERT", "try LSTM or GRU models",
               "use rolling-window evaluation", "test an actual trading rule"],
              "\"Thank you. We are happy to take your questions.\"")

# ------------------------------------------------------------------ Q&A
story.append(Spacer(1, 10))
story.append(KeepTogether([
    Paragraph("Quick Q&amp;A guide", SPK),
    table([["Question", "Who", "Short answer"],
           ["Why only 50% accuracy?", "3", "Next-day direction is close to random, and our study confirms that."],
           ["Did you tune until it looked good?", "2",
            "No. The grids are small and the test set was never used for choices."],
           ["Could deep learning do better?", "4",
            "Possibly slightly, but about 2,000 samples would likely overfit."],
           ["Is sentiment useless?", "4",
            "Not necessarily. This news source is loosely related to the market. Company-specific news or "
            "predicting volatility might work better."],
           ["Should anyone trade on this?", "4", "No."]],
          [5.2 * cm, 1.3 * cm, 10.5 * cm]),
]))

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                        bottomMargin=2 * cm, title="Presentation Script", author="Project team")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("saved", OUT)
