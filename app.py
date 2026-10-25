import random
import time
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sorting Algorithm Analyzer", page_icon="📊", layout="wide")

# High-contrast, readable text styling
st.markdown("""
<style>
.stApp {
    background: #F4F7FB;
    color: #172B4D;
}
.block-container {
    max-width: 1200px;
    padding-top: 1.4rem;
    padding-bottom: 2.5rem;
}
h1, h2, h3, h4, p, label, li, span, small, .stMarkdown {
    color: #172B4D;
}
h1 {font-size: 2.15rem !important; font-weight: 750 !important;}
h2, h3 {font-weight: 700 !important;}
.hero {
    background: linear-gradient(120deg, #142B4A, #2865AD);
    padding: 25px 28px;
    border-radius: 16px;
    color: #FFFFFF !important;
    margin-bottom: 22px;
}
.hero h1, .hero p {color: #FFFFFF !important;}
.hero p {font-size: 1rem; margin: 8px 0 0 0;}
.intro {
    background: #EAF2FF;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 18px;
    color: #17365D !important;
}
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #D8E2EF;
    padding: 14px;
    border-radius: 12px;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #172B4D !important;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: 650;
    min-height: 2.8rem;
}
div.stButton > button[kind="primary"] {
    background: #E5484D;
    color: #FFFFFF !important;
    border: 0;
}
div.stButton > button[kind="primary"]:hover {
    background: #C9363B;
    color: #FFFFFF !important;
}
.stTextInput label, .stRadio label, .stSelectbox label,
.stSlider label, .stNumberInput label, .stFileUploader label {
    color: #172B4D !important;
    font-weight: 600;
}
.stRadio div[role="radiogroup"] label p {color: #172B4D !important;}
.stTextInput input, .stNumberInput input {
    color: #FFFFFF !important;
    background: #253247 !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    color: #FFFFFF !important;
    background: #253247 !important;
}
.stSelectbox div[data-baseweb="select"] input {color: #FFFFFF !important;}
.stFileUploader section {background: #FFFFFF; border: 1px dashed #9BB3D1;}
.stFileUploader section * {color: #172B4D !important;}
[data-testid="stDataFrame"] {background: #FFFFFF;}
[data-testid="stExpander"] summary p {color: #172B4D !important; font-weight: 600;}
.stAlert p {color: #172B4D !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>📊 Sorting Algorithm Performance Analyzer</h1>
  <p>A simple, interactive way to compare five sorting algorithms.</p>
</div>
""", unsafe_allow_html=True)

def bubble_sort(values):
    a = values.copy()
    comparisons = swaps = 0
    for i in range(len(a)):
        changed = False
        for j in range(len(a) - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                changed = True
        if not changed:
            break
    return a, comparisons, swaps

def selection_sort(values):
    a = values.copy()
    comparisons = swaps = 0
    for i in range(len(a)):
        smallest = i
        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1
    return a, comparisons, swaps

def insertion_sort(values):
    a = values.copy()
    comparisons = shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons, shifts

def merge_sort(values):
    count = [0]
    def sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left, right = sort(a[:mid]), sort(a[mid:])
        merged, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            count[0] += 1
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
    return sort(values.copy()), count[0], 0

def quick_sort(values):
    a = values.copy()
    comparisons = swaps = 0
    def sort(low, high):
        nonlocal comparisons, swaps
        if low >= high:
            return
        pivot = a[high]
        i = low
        for j in range(low, high):
            comparisons += 1
            if a[j] <= pivot:
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    swaps += 1
                i += 1
        if i != high:
            a[i], a[high] = a[high], a[i]
            swaps += 1
        sort(low, i - 1)
        sort(i + 1, high)
    sort(0, len(a) - 1)
    return a, comparisons, swaps

ALGORITHMS = {
    "Bubble Sort": (bubble_sort, "O(n²)", "O(1)"),
    "Selection Sort": (selection_sort, "O(n²)", "O(1)"),
    "Insertion Sort": (insertion_sort, "O(n²)", "O(1)"),
    "Merge Sort": (merge_sort, "O(n log n)", "O(n)"),
    "Quick Sort": (quick_sort, "O(n log n) average", "O(log n) average*"),
}

def parse_numbers(raw):
    parts = [p.strip() for p in raw.replace("\n", ",").split(",") if p.strip()]
    if not parts:
        raise ValueError("Please enter at least one number.")
    try:
        return [int(p) for p in parts]
    except ValueError as exc:
        raise ValueError("Please enter whole numbers separated by commas.") from exc

st.markdown("### 1. Choose your dataset")
method = st.radio("Input method", ["Type numbers", "Random numbers", "Upload CSV / Excel"], horizontal=True)
numbers = []

if method == "Type numbers":
    raw = st.text_input("Enter numbers separated by commas", "45, 12, 78, 3, 29, 10")
    try:
        numbers = parse_numbers(raw)
    except ValueError as err:
        st.error(str(err))
elif method == "Random numbers":
    col1, col2 = st.columns(2)
    with col1:
        amount = st.slider("Number of values", 5, 300, 30)
    with col2:
        seed = st.number_input("Random seed", min_value=0, max_value=999999, value=42)
    rng = random.Random(int(seed))
    numbers = [rng.randint(1, 1000) for _ in range(amount)]
else:
    uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded is not None:
        try:
            data = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
            st.dataframe(data.head(8), use_container_width=True)
            numeric_columns = list(data.select_dtypes(include="number").columns)
            if numeric_columns:
                column = st.selectbox("Choose the numeric column to sort", numeric_columns)
                numbers = pd.to_numeric(data[column], errors="coerce").dropna().astype(int).tolist()[:2000]
            else:
                st.warning("This file has no numeric columns.")
        except Exception as exc:
            st.error(f"Could not read the file: {exc}")

numbers = numbers[:2000]
if numbers:
    st.info(f"Input dataset: {len(numbers)} number(s)")
    with st.expander("Preview input numbers"):
        st.code(", ".join(map(str, numbers[:100])) + (" ..." if len(numbers) > 100 else ""))
else:
    st.warning("Enter numbers or upload a dataset to begin.")

st.markdown("### 2. Select an algorithm to inspect")
selected = st.selectbox("Show sorted output for", list(ALGORITHMS.keys()))
st.caption("The comparison runs all five algorithms on the same input.")

if st.button("🚀 Analyze Sorting Performance", type="primary", use_container_width=True):
    if not numbers:
        st.error("Please provide valid numbers first.")
    else:
        rows, outputs = [], {}
        expected = sorted(numbers)
        for name, (function, time_complexity, space_complexity) in ALGORITHMS.items():
            start = time.perf_counter()
            sorted_values, comparisons, swaps = function(numbers)
            elapsed = (time.perf_counter() - start) * 1000
            outputs[name] = sorted_values
            rows.append({
                "Algorithm": name,
                "Execution Time (ms)": elapsed,
                "Comparisons": comparisons,
                "Swaps / Shifts": swaps,
                "Time Complexity": time_complexity,
                "Space Complexity": space_complexity,
                "Correct": sorted_values == expected,
            })
        st.session_state["analysis"] = {"input": numbers.copy(), "rows": rows, "outputs": outputs}

analysis = st.session_state.get("analysis")
if analysis and analysis["input"] == numbers:
    st.markdown("---")
    st.markdown("### 3. Results overview")
    df = pd.DataFrame(analysis["rows"])
    fastest = df.loc[df["Execution Time (ms)"].idxmin()]
    a, b, c = st.columns(3)
    a.metric("Fastest in this run", fastest["Algorithm"])
    b.metric("Dataset size", f"{len(numbers)} values")
    c.metric("All results correct", "Yes" if df["Correct"].all() else "No")

    table = df[["Algorithm", "Execution Time (ms)", "Comparisons", "Swaps / Shifts",
                "Time Complexity", "Space Complexity", "Correct"]].copy()
    table["Execution Time (ms)"] = table["Execution Time (ms)"].map(lambda x: round(x, 5))
    st.markdown("#### Performance comparison")
    st.dataframe(table, hide_index=True, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown("#### Execution time")
        st.bar_chart(df.set_index("Algorithm")[["Execution Time (ms)"]])
    with right:
        st.markdown(f"#### Sorted output — {selected}")
        output = analysis["outputs"][selected]
        st.code(", ".join(map(str, output[:100])) + (" ..." if len(output) > 100 else ""))
        st.caption("The sorted output is in ascending order.")

    st.download_button(
        "⬇ Download results as CSV",
        data=table.to_csv(index=False).encode("utf-8"),
        file_name="sorting_performance_results.csv",
        mime="text/csv",
    )

with st.expander("Learn about the five algorithms"):
    st.markdown("""
- **Bubble Sort:** Swaps neighbouring values that are in the wrong order.
- **Selection Sort:** Finds the smallest remaining value and puts it in its place.
- **Insertion Sort:** Inserts each value into the already-sorted part.
- **Merge Sort:** Splits the list, sorts each part, and merges them.
- **Quick Sort:** Uses a pivot to separate smaller and larger values.

**Presentation tip:** Start with 6–30 numbers. Timing can vary between computers and runs.
""")
st.caption("Sorting Algorithm Performance Analyzer • Python + Streamlit")
