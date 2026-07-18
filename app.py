# app.py — เว็บไซต์ทำนายภาวะซึมเศร้าด้วยโมเดล SVM (Streamlit)
# วางไฟล์ svm_depression_model.joblib ไว้โฟลเดอร์เดียวกับไฟล์นี้

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Depression Prediction (SVM)", page_icon="🧠", layout="centered")


@st.cache_resource
def load_model():
    return joblib.load("svm_depression_model.joblib")


model = load_model()

st.title("🧠 Depression Prediction with SVM")
st.caption("โมเดล LinearSVC เทรนจากข้อมูลแบบสำรวจ 140,700 รายการ")
st.info(
    "⚠️ แอปนี้เป็นโปรเจกต์เพื่อการศึกษาเท่านั้น ไม่ใช่เครื่องมือวินิจฉัยทางการแพทย์ "
    "หากมีความกังวลเกี่ยวกับสุขภาพจิต ควรปรึกษาแพทย์หรือผู้เชี่ยวชาญโดยตรง"
)

# ---------- ตัวเลือกในฟอร์ม (ค่าที่พบบ่อยในชุดข้อมูล) ----------
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
SLEEP = ['Less than 5 hours', '5-6 hours', '7-8 hours', 'More than 8 hours']
DIET = ['Healthy', 'Moderate', 'Unhealthy']

# ---------- ฟอร์มกรอกข้อมูล ----------
st.subheader("กรอกข้อมูลเพื่อทำนาย")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ['Male', 'Female'])
    age = st.slider("Age", 18, 60, 25)
    city = st.selectbox("City", CITIES)
    status = st.selectbox("Working Professional or Student",
                          ['Student', 'Working Professional'])
    profession = st.selectbox("Profession", PROFESSIONS)
    degree = st.selectbox("Degree", DEGREES)
    sleep = st.selectbox("Sleep Duration", SLEEP)
    diet = st.selectbox("Dietary Habits", DIET)

with col2:
    is_student = status == 'Student'
    academic_pressure = st.slider("Academic Pressure (1-5)", 0.0, 5.0,
                                  3.0 if is_student else 0.0, 1.0,
                                  disabled=not is_student)
    cgpa = st.slider("CGPA (0-10)", 0.0, 10.0,
                     7.5 if is_student else 0.0, 0.1,
                     disabled=not is_student)
    study_satisfaction = st.slider("Study Satisfaction (1-5)", 0.0, 5.0,
                                   3.0 if is_student else 0.0, 1.0,
                                   disabled=not is_student)
    work_pressure = st.slider("Work Pressure (1-5)", 0.0, 5.0,
                              0.0 if is_student else 3.0, 1.0,
                              disabled=is_student)
    job_satisfaction = st.slider("Job Satisfaction (1-5)", 0.0, 5.0,
                                 0.0 if is_student else 3.0, 1.0,
                                 disabled=is_student)
    hours = st.slider("Work/Study Hours per day", 0.0, 12.0, 6.0, 1.0)
    financial = st.slider("Financial Stress (1-5)", 1.0, 5.0, 3.0, 1.0)

suicidal = st.selectbox("Have you ever had suicidal thoughts ?", ['No', 'Yes'])
family = st.selectbox("Family History of Mental Illness", ['No', 'Yes'])

# ---------- ทำนาย ----------
if st.button("🔮 ทำนายผล", type="primary", use_container_width=True):
    # ชื่อคอลัมน์ต้องตรงกับตอนเทรนทุกตัวอักษร
    input_df = pd.DataFrame([{
        'Gender': gender,
        'Age': float(age),
        'City': city,
        'Working Professional or Student': status,
        'Profession': profession,
        'Academic Pressure': academic_pressure,
        'Work Pressure': work_pressure,
        'CGPA': cgpa,
        'Study Satisfaction': study_satisfaction,
        'Job Satisfaction': job_satisfaction,
        'Sleep Duration': sleep,
        'Dietary Habits': diet,
        'Degree': degree,
        'Have you ever had suicidal thoughts ?': suicidal,
        'Work/Study Hours': hours,
        'Financial Stress': financial,
        'Family History of Mental Illness': family,
    }])

    prediction = model.predict(input_df)[0]
    score = model.decision_function(input_df)[0]  # ระยะจาก decision boundary

    st.divider()
    if prediction == 1:
        st.error("ผลการทำนาย: **มีแนวโน้มภาวะซึมเศร้า (Depression = 1)**")
    else:
        st.success("ผลการทำนาย: **ไม่มีแนวโน้มภาวะซึมเศร้า (Depression = 0)**")
    st.caption(f"Decision score: {score:.3f} (ค่าบวก = โน้มไปทางคลาส 1, ค่าลบ = คลาส 0)")

    with st.expander("ดูข้อมูลที่ส่งเข้าโมเดล"):
        st.dataframe(input_df.T, use_container_width=True)
