# app.py — ระบบทำนายแนวโน้มภาวะซึมเศร้าด้วยแบบจำลอง SVM
# วางไฟล์ svm_depression_model.joblib ไว้ในโฟลเดอร์เดียวกับไฟล์นี้

import streamlit as st
import pandas as pd
import joblib

# ----------------------------------------------------------------------
# การตั้งค่าหน้าเว็บ
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="ระบบทำนายแนวโน้มภาวะซึมเศร้า | SVM",
    page_icon="🎓",
    layout="centered",
)

# ----------------------------------------------------------------------
# รูปแบบตัวอักษรและโทนสี (ฟอนต์ Sarabun — โทนทางการ)
# ----------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stSlider {
    font-family: 'Sarabun', sans-serif !important;
}

.main-header {
    background: linear-gradient(135deg, #1a2f52 0%, #24457a 100%);
    border-radius: 10px;
    padding: 2rem 2.2rem 1.7rem 2.2rem;
    margin-bottom: 1.2rem;
    color: #ffffff;
}
.main-header h1 {
    font-size: 1.55rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 .35rem 0;
    letter-spacing: .2px;
}
.main-header p {
    font-size: .95rem;
    font-weight: 300;
    color: #c9d6ec;
    margin: 0;
}
.header-rule {
    border: none;
    border-top: 3px solid #c9a227;
    width: 72px;
    margin: .8rem 0 .9rem 0;
}

.section-title {
    font-size: 1.02rem;
    font-weight: 600;
    color: #1a2f52;
    border-left: 4px solid #c9a227;
    padding-left: .6rem;
    margin: 1.1rem 0 .3rem 0;
}

.result-card {
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-top: .8rem;
    border: 1px solid;
}
.result-positive { background: #fdf3f2; border-color: #e5b8b4; }
.result-negative { background: #f2f8f4; border-color: #b7d9c4; }
.result-card .result-label {
    font-size: .85rem;
    font-weight: 500;
    color: #6b7280;
    margin-bottom: .2rem;
}
.result-card .result-value { font-size: 1.25rem; font-weight: 700; }
.result-positive .result-value { color: #a13c34; }
.result-negative .result-value { color: #1f6b45; }
.result-card .result-note { font-size: .85rem; color: #6b7280; margin-top: .45rem; }

.disclaimer {
    background: #f6f7f9;
    border: 1px solid #dfe3ea;
    border-radius: 8px;
    padding: .85rem 1.1rem;
    font-size: .86rem;
    color: #4b5563;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# โหลดแบบจำลอง
# ----------------------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("svm_depression_model.joblib")

model = load_model()

# ----------------------------------------------------------------------
# ส่วนหัวของระบบ
# ----------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>ระบบทำนายแนวโน้มภาวะซึมเศร้า</h1>
    <hr class="header-rule">
    <p>แบบจำลอง Support Vector Machine (LinearSVC) พัฒนาจากข้อมูลแบบสำรวจ
    จำนวน 140,700 รายการ | ความแม่นยำบนชุดทดสอบ 91%</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
<strong>ข้อจำกัดของระบบ:</strong> ระบบนี้จัดทำขึ้นเพื่อการศึกษาเท่านั้น
มิใช่เครื่องมือวินิจฉัยทางการแพทย์ ผลการทำนายไม่สามารถใช้แทนคำวินิจฉัยของแพทย์ได้
หากท่านมีความกังวลเกี่ยวกับสุขภาพจิต โปรดปรึกษาแพทย์หรือผู้เชี่ยวชาญโดยตรง
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ตัวเลือกในแบบฟอร์ม (ค่าภาษาไทยสำหรับแสดงผล → ค่าภาษาอังกฤษสำหรับแบบจำลอง)
# ----------------------------------------------------------------------
GENDER_MAP = {"ชาย": "Male", "หญิง": "Female"}
STATUS_MAP = {"นักศึกษา": "Student", "ผู้ทำงาน": "Working Professional"}
YESNO_MAP = {"ไม่เคย": "No", "เคย": "Yes"}
FAMILY_MAP = {"ไม่มี": "No", "มี": "Yes"}
SLEEP_MAP = {
    "น้อยกว่า 5 ชั่วโมง": "Less than 5 hours",
    "5–6 ชั่วโมง": "5-6 hours",
    "7–8 ชั่วโมง": "7-8 hours",
    "มากกว่า 8 ชั่วโมง": "More than 8 hours",
}
DIET_MAP = {
    "รับประทานอาหารที่ดีต่อสุขภาพ": "Healthy",
    "ปานกลาง": "Moderate",
    "ไม่ค่อยดีต่อสุขภาพ": "Unhealthy",
}

CITIES = ['Agra', 'Ahmedabad', 'Bangalore', 'Bhopal', 'Chennai', 'Delhi', 'Faridabad',
          'Ghaziabad', 'Hyderabad', 'Indore', 'Jaipur', 'Kalyan', 'Kanpur', 'Kolkata',
          'Lucknow', 'Ludhiana', 'Meerut', 'Mumbai', 'Nagpur', 'Nashik', 'Patna', 'Pune',
          'Rajkot', 'Srinagar', 'Surat', 'Thane', 'Vadodara', 'Varanasi', 'Vasai-Virar',
          'Visakhapatnam']
PROFESSIONS = ['Student', 'Accountant', 'Architect', 'Business Analyst', 'Chef', 'Chemist',
               'Civil Engineer', 'Consultant', 'Content Writer', 'Customer Support',
               'Data Scientist', 'Digital Marketer', 'Doctor', 'Educational Consultant',
               'Electrician', 'Entrepreneur', 'Financial Analyst', 'Graphic Designer',
               'HR Manager', 'Investment Banker', 'Judge', 'Lawyer', 'Manager',
               'Marketing Manager', 'Mechanical Engineer', 'Pharmacist', 'Pilot', 'Plumber',
               'Research Analyst', 'Researcher', 'Sales Executive', 'Software Engineer',
               'Teacher', 'Travel Consultant', 'UX/UI Designer']
DEGREES = ['Class 12', 'BA', 'BBA', 'BCA', 'BE', 'BHM', 'BSc', 'B.Arch', 'B.Com', 'B.Ed',
           'B.Pharm', 'B.Tech', 'LLB', 'LLM', 'MA', 'MBA', 'MBBS', 'MCA', 'MD', 'ME', 'MHM',
           'MSc', 'M.Com', 'M.Ed', 'M.Pharm', 'M.Tech', 'PhD']

# ----------------------------------------------------------------------
# แบบฟอร์มกรอกข้อมูล
# ----------------------------------------------------------------------
st.markdown('<div class="section-title">ส่วนที่ 1 — ข้อมูลทั่วไป</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    gender_th = st.selectbox("เพศ", list(GENDER_MAP))
    age = st.slider("อายุ (ปี)", 18, 60, 25)
    city = st.selectbox("เมืองที่พักอาศัย", CITIES)
with c2:
    status_th = st.selectbox("สถานภาพ", list(STATUS_MAP))
    profession = st.selectbox("อาชีพ", PROFESSIONS)
    degree = st.selectbox("วุฒิการศึกษา", DEGREES)

is_student = STATUS_MAP[status_th] == "Student"

st.markdown('<div class="section-title">ส่วนที่ 2 — ด้านการศึกษาและการทำงาน</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    academic_pressure = st.slider("ความกดดันด้านการเรียน (0–5)", 0.0, 5.0,
                                  3.0 if is_student else 0.0, 1.0,
                                  disabled=not is_student,
                                  help="สำหรับนักศึกษาเท่านั้น")
    cgpa = st.slider("เกรดเฉลี่ยสะสม CGPA (0–10)", 0.0, 10.0,
                     7.5 if is_student else 0.0, 0.1, disabled=not is_student)
    study_satisfaction = st.slider("ความพึงพอใจในการเรียน (0–5)", 0.0, 5.0,
                                   3.0 if is_student else 0.0, 1.0,
                                   disabled=not is_student)
with c4:
    work_pressure = st.slider("ความกดดันด้านการทำงาน (0–5)", 0.0, 5.0,
                              0.0 if is_student else 3.0, 1.0,
                              disabled=is_student,
                              help="สำหรับผู้ทำงานเท่านั้น")
    job_satisfaction = st.slider("ความพึงพอใจในงาน (0–5)", 0.0, 5.0,
                                 0.0 if is_student else 3.0, 1.0,
                                 disabled=is_student)
    hours = st.slider("ชั่วโมงเรียน/ทำงานต่อวัน", 0.0, 12.0, 6.0, 1.0)

st.markdown('<div class="section-title">ส่วนที่ 3 — สุขภาพและการดำเนินชีวิต</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)
with c5:
    sleep_th = st.selectbox("ระยะเวลานอนหลับต่อวัน", list(SLEEP_MAP))
    diet_th = st.selectbox("พฤติกรรมการรับประทานอาหาร", list(DIET_MAP))
    financial = st.slider("ความเครียดด้านการเงิน (1–5)", 1.0, 5.0, 3.0, 1.0)
with c6:
    suicidal_th = st.selectbox("เคยมีความคิดทำร้ายตนเองหรือไม่", list(YESNO_MAP))
    family_th = st.selectbox("ประวัติปัญหาสุขภาพจิตในครอบครัว", list(FAMILY_MAP))

st.markdown("")

# ----------------------------------------------------------------------
# ประมวลผลการทำนาย
# ----------------------------------------------------------------------
if st.button("ประมวลผลการทำนาย", type="primary", use_container_width=True):
    # ชื่อคอลัมน์และค่าต้องตรงกับข้อมูลตอนเทรนแบบจำลองทุกตัวอักษร
    input_df = pd.DataFrame([{
        'Gender': GENDER_MAP[gender_th],
        'Age': float(age),
        'City': city,
        'Working Professional or Student': STATUS_MAP[status_th],
        'Profession': profession,
        'Academic Pressure': academic_pressure,
        'Work Pressure': work_pressure,
        'CGPA': cgpa,
        'Study Satisfaction': study_satisfaction,
        'Job Satisfaction': job_satisfaction,
        'Sleep Duration': SLEEP_MAP[sleep_th],
        'Dietary Habits': DIET_MAP[diet_th],
        'Degree': degree,
        'Have you ever had suicidal thoughts ?': YESNO_MAP[suicidal_th],
        'Work/Study Hours': hours,
        'Financial Stress': financial,
        'Family History of Mental Illness': FAMILY_MAP[family_th],
    }])

    prediction = int(model.predict(input_df)[0])
    score = float(model.decision_function(input_df)[0])

    if prediction == 1:
        st.markdown(f"""
        <div class="result-card result-positive">
            <div class="result-label">ผลการทำนายจากแบบจำลอง</div>
            <div class="result-value">พบแนวโน้มภาวะซึมเศร้า (คลาส 1)</div>
            <div class="result-note">ค่าคะแนนการตัดสินใจ (decision score): {score:.3f}
            — ค่าเป็นบวก แสดงว่าข้อมูลอยู่ฝั่งคลาส 1 ของระนาบตัดสินใจ</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="disclaimer" style="margin-top:.8rem;">
        ผลนี้เป็นเพียงการประเมินจากแบบจำลองทางสถิติ หากท่านหรือบุคคลใกล้ชิด
        กำลังเผชิญความเครียดหรือความไม่สบายใจ การพูดคุยกับแพทย์ นักจิตวิทยา
        หรือสายด่วนสุขภาพจิต 1323 (ประเทศไทย) เป็นทางเลือกที่แนะนำ
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card result-negative">
            <div class="result-label">ผลการทำนายจากแบบจำลอง</div>
            <div class="result-value">ไม่พบแนวโน้มภาวะซึมเศร้า (คลาส 0)</div>
            <div class="result-note">ค่าคะแนนการตัดสินใจ (decision score): {score:.3f}
            — ค่าเป็นลบ แสดงว่าข้อมูลอยู่ฝั่งคลาส 0 ของระนาบตัดสินใจ</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("ตรวจสอบข้อมูลที่ส่งเข้าแบบจำลอง"):
        st.dataframe(input_df.T.rename(columns={0: "ค่าที่ใช้ทำนาย"}),
                     use_container_width=True)

# ----------------------------------------------------------------------
# ส่วนท้าย
# ----------------------------------------------------------------------
st.markdown("---")
st.caption("จัดทำเพื่อการศึกษา | แบบจำลอง: LinearSVC (scikit-learn 1.8.0) | "
           "ข้อมูลฝึกสอน: 140,700 รายการ")