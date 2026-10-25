# Sorting Algorithm Performance Analyzer

A simple, interactive web application built with Python and Streamlit to compare the performance of five sorting algorithms.

## Features

- **Five sorting algorithms:** Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick Sort.
- **Multiple input options:** Enter numbers manually, generate random numbers, or upload a CSV/Excel dataset.
- **Performance comparison:** View execution time, comparisons, and swaps/shifts for each algorithm.
- **Visual results:** Compare execution times using a bar chart.
- **Sorted output:** Inspect the sorted result for the selected algorithm.
- **Correctness check:** Verify that the algorithms produce the expected sorted output.
- **CSV export:** Download the performance comparison table.

## Technologies Used

- Python
- Streamlit
- Pandas
- OpenPyXL (for Excel file support)

## Requirements

- Python 3.10 or later recommended
- pip

## Installation and Setup (Windows PowerShell)

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open the terminal in the folder containing `app.py` and `requirements.txt`.
4. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

5. Activate it:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks script execution, run this in the same terminal first:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   ```

6. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Start the application:

   ```powershell
   python -m streamlit run app.py
   ```

8. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## How to Use

1. Choose an input method: type numbers, generate random numbers, or upload a CSV/Excel file.
2. If uploading a file, select the numeric column you want to sort.
3. Click **Analyze Sorting Performance**.
4. Review the comparison table and execution-time bar chart.
5. Select an algorithm to view its sorted output.
6. Download the results as a CSV file if needed.

## Algorithm Complexity

| Algorithm | Average Time Complexity | Worst-case Time Complexity |
|---|---|---|
| Bubble Sort | O(n²) | O(n²) |
| Selection Sort | O(n²) | O(n²) |
| Insertion Sort | O(n²) | O(n²) |
| Merge Sort | O(n log n) | O(n log n) |
| Quick Sort | O(n log n) | O(n²) |

Actual execution times depend on the input dataset, computer, and Python environment. For a quick classroom demonstration, use a small dataset first.

## Project Structure

```text
Sorting_Algorithm_Performance_Analyzer/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Notes

- Keep `.venv/`, `.env`, and private secrets out of GitHub.
- CSV/Excel upload requires a dataset with a numeric column.
- Only upload datasets you are allowed to use and share.

## Author

**DHARIKHA U and Team**  
Department of Artificial Intelligence and Data Science  
Karunya Institute of Technology and Sciences
