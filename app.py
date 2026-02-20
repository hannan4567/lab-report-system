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

    header_height = 300  # px

    report_html = f"""
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Lab Report</title>
    <style>
    :root {{
        --header-height: {header_height}px;
    }}

    body {{
        font-family: Arial, Helvetica, sans-serif;
        margin: 0;
        padding: 0;
    }}

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
    }}

    .header .title {{
        font-size: 28px;
        font-weight: 700;
    }}

    .content {{
        margin-top: var(--header-height);
        padding: 20px;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        table-layout: fixed;
    }}

    th, td {{
        border: 1px solid #333;
        padding: 8px;
    }}

    th {{
        background-color: #f0f0f0;
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
    </style>
    </head>
    <body>
    <div class="header">
        <div class="title">Reliable path lab logo</div>
    </div>

    <div class="content">
    """

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

    for test, values in report_data.items():

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

    report_html += """
    <div class="report-footer">*** END OF REPORT ***</div>
    </div>
    </body>
    </html>
    """

    st.success("Report Generated Successfully")

    # 🔥 Safe rendering that works on mobile
    try:
        components.html(report_html, height=1200, scrolling=True)
    except:
        st.markdown(report_html, unsafe_allow_html=True)

    st.download_button(
        "Download Report",
        report_html,
        file_name="lab_report.html",
        mime="text/html"
    )
