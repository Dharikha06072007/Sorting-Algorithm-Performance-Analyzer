# Simple Sorting Algorithm Performance Analyzer

## Run in VS Code (Windows)

1. Extract the ZIP and open the folder in VS Code.
2. Open Terminal → New Terminal.
3. Run these commands:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

4. Open the local address shown in the terminal, usually `http://localhost:8501`.

## Easy presentation flow

1. Enter numbers or generate random numbers.
2. Select one of the five sorting algorithms.
3. Click Analyze sorting performance.
4. Show the before/after arrays.
5. Explain the time, comparisons, swaps/shifts and chart comparing all five algorithms.

The app tests all five algorithms using the same input so the comparison is fair.
