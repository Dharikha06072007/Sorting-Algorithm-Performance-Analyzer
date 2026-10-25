# Sorting Algorithm Performance Analyzer — Static Website

A frontend-only version of the project built with HTML, CSS, and JavaScript. It can be hosted as a Render **Static Site** without Python or a backend.

## Features
- Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick Sort
- Manual numeric input
- Random dataset generator
- CSV/TXT upload and numeric-value extraction
- Execution-time comparison chart
- Comparisons and swaps/shifts metrics
- Correctness verification
- Sorted output selector
- Download results as CSV
- Responsive layout for desktop and mobile
- All analysis runs locally in the browser

## Deploy on Render Static Site
1. Upload `index.html`, `style.css`, `script.js`, and `README.md` to the root of your GitHub repository.
2. In Render, choose **New + → Static Site**.
3. Connect the GitHub repository.
4. Set **Build Command** to blank (or leave it empty if Render permits).
5. Set **Publish Directory** to `.` (a single dot).
6. Click **Create Static Site**.

Do not use `streamlit run app.py` for this static website. It no longer requires `app.py` or `requirements.txt` to run online.

## Run locally
Open `index.html` in a browser, or use VS Code Live Server.

## Notes
- CSV and TXT files are read locally in your browser; no data is sent to a server.
- The app supports up to 5,000 values, but Bubble, Selection, and Insertion Sort can be slow for large datasets. Use a small input for a quick classroom demo.
- Timing results vary with the browser, device, and dataset. For very small datasets, measured times may be close to zero.
- The chart is drawn with the HTML canvas API and requires no charting library.
