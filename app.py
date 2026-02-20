import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Live Lab Report", layout="centered")

st.title("Path Lab Report System")

# =============================
# PATIENT DETAILS
# =============================
st.subheader("Patient Details")

name = st.text_input("Patient Name")
age = st.text_input("Age / Sex")
doctor = st.text_input("Referred By")
sample = st.text_input("Sample")

received = st.date_input("Received On", date.today())
reported = st.date_input("Reported On", date.today())

st.divider()

# =============================
# TEST DATABASE
# =============================
tests = {

    "CBC": {
        "Hemoglobin": "13-17",
        "RBC Count": "4.5-5.5",
        "WBC Count": "4000-11000",
        "Platelet Count": "150000-450000"
    },

    "Diabetes Profile": {
        "Fasting Blood Sugar": "70-110",
        "Postprandial Sugar": "70-140",
        "HbA1c": "4-5.6"
    },

    "Lipid Profile": {
        "Total Cholesterol": "<200",
        "Triglycerides": "<150",
        "HDL": ">40",
        "LDL": "<100"
    },

    "Liver Function Test": {
        "SGPT (ALT)": "7-56",
        "SGOT (AST)": "10-40",
        "Bilirubin Total": "0.1-1.2"
    },

    "Kidney Function Test": {
        "Urea": "7-20",
        "Creatinine": "0.6-1.3",
        "Uric Acid": "3.5-7.2"
    },

    "Thyroid Profile": {
        "TSH": "0.4-4.0",
        "T3": "80-200",
        "T4": "5-12"
    }
}

selected_tests = st.multiselect("Select Tests", list(tests.keys()))

report_data = {}

st.subheader("Enter Test Values")

for test in selected_tests:
    st.markdown(f"### {test}")
    report_data[test] = {}

    for field, normal in tests[test].items():
        # include unique key to avoid input collisions
        value = st.text_input(f"{field} (Normal: {normal})", key=f"{test}__{field}")
        report_data[test][field] = {
            "value": value,
            "normal": normal
        }

st.divider()

# =============================
# ABNORMAL CHECK FUNCTION
# =============================
def check_abnormal(value, normal):
    try:
        value = float(value)

        if "-" in normal:
            low, high = normal.split("-")
            if value < float(low) or value > float(high):
                return True

        elif normal.startswith("<"):
            if value >= float(normal[1:]):
                return True

        elif normal.startswith(">"):
            if value <= float(normal[1:]):
                return True

        return False
    except:
        return False


# =============================
# GENERATE REPORT
# =============================
if st.button("Generate Report"):

    # NOTE: Header height controlled by --header-height variable (300px by default)
    # You can tune header_height variable below if needed.
    header_height = 300  # px (tweak if you want slightly higher/lower)

    report_html = f"""
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Lab Report</title>
    <style>
    :root {{
        --header-height: {header_height}px;
        --page-padding-left: 20px;
        --page-padding-right: 20px;
    }}

    /* Basic styles for screen */
    body {{
        font-family: Arial, Helvetica, sans-serif;
        margin: 0;
        padding: 0;
        -webkit-font-smoothing:antialiased;
        -moz-osx-font-smoothing:grayscale;
    }}

    /* Fixed top header (green) - visible on screen and preserved for print in most browsers */
    .header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: var(--header-height);
        background: linear-gradient(90deg, #1e7a1e, #2fa02f);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }}
    .header .title {{
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 1px;
    }}

    /* Main content pushed below fixed header */
    .content {{
        margin-top: var(--header-height); /* ensures content starts below header */
        padding: 20px;
        box-sizing: border-box;
    }}

    /* Tables: fixed layout for consistent alignment */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        table-layout: fixed;
        page-break-inside: avoid;
    }}

    th, td {{
        border: 1px solid #333;
        padding: 8px;
        vertical-align: middle;
        word-wrap: break-word;
    }}

    th {{
        background-color: #f0f0f0;
        font-weight: 600;
    }}

    .col-test {{ width: 50%; text-align: left; }}
    .col-result {{ width: 25%; text-align: right; }}
    .col-normal {{ width: 25%; text-align: center; }}

    .patient-table td {{ width: 25%; }}

    .report-footer {{
        margin-top: 40px;
        text-align: center;
        font-weight: 700;
    }}

    /* Print-specific rules to ensure A4 and consistent top margin on every page */
    @page {{
        size: A4;
        /* Provide a top margin that matches header height (approx conversion),
           many browsers expect margin in mm — we set both px and mm fallbacks. */
        margin: 0mm; /* set zero here and control spacing via header and content */
    }}

    @media print {{
        html, body {{
            width: 210mm;
            height: 297mm;
        }}

        /* Keep header printed and fixed at top of each page when possible */
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
        }}

        /* Force content to start below the header on every printed page */
        .content {{
            margin-top: var(--header-height);
            padding-left: 15mm;
            padding-right: 15mm;
        }}

        /* Add page breaks when necessary but keep header spacing consistent */
        table {{
            page-break-inside: avoid;
        }}

        /* Add a small gap at bottom of each printed page to avoid cutoff */
        .page-break {{
            page-break-after: always;
        }}
    }}
    </style>
    </head>
    <body>
    <div class="header">
        <div class="title">Reliable path lab logo</div>
    </div>

    <div class="content">
    """

    # Patient info table
    report_html += f"""
    <table class="patient-table">
    <tr>
        <td><b>Patient Name</b></td><td>{name}</td>
        <td><b>Received</b></td><td>{received}</td>
    </tr>
    <tr>
        <td><b>Age / Sex</b></td><td>{age}</td>
        <td><b>Reported</b></td><td>{reported}</td>
    </tr>
    <tr>
        <td><b>Referred By</b></td><td>{doctor}</td>
        <td><b>Sample</b></td><td>{sample}</td>
    </tr>
    </table>
    """

    # Test sections
    section_count = 0
    for test, values in report_data.items():
        section_count += 1

        report_html += f"""
        <table>
        <tr><th colspan='3'>{test}</th></tr>
        <tr>
            <th class="col-test">Test</th>
            <th class="col-result">Result</th>
            <th class="col-normal">Normal Range</th>
        </tr>
        """

        for k, v in values.items():
            abnormal = check_abnormal(v["value"], v["normal"])
            color = "red" if abnormal else "black"
            display_value = v["value"] if v["value"] != "" else "&nbsp;"

            report_html += f"""
            <tr>
                <td class="col-test">{k}</td>
                <td class="col-result" style="color:{color}; font-weight:bold;">{display_value}</td>
                <td class="col-normal">{v["normal"]}</td>
            </tr>
            """

        report_html += "</table>"

        # Insert a page-break hint for long reports every N sections if desired
        # (uncomment the next line if you want a hard page break after each section)
        # report_html += '<div class="page-break"></div>'

    # Footer / end of report
    report_html += """
    <div class="report-footer">*** END OF REPORT ***</div>
    </div> <!-- end content -->
    </body>
    </html>
    """

    st.success("Report Generated Successfully")

    # Display rendered HTML in Streamlit - set height large enough for content
    components.html(report_html, height=1200, scrolling=True)

    # Download HTML file
    st.download_button(
        "Download Report",
        report_html,
        file_name="lab_report.html",
        mime="text/html"
    )
