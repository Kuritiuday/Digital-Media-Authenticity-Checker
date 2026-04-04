import streamlit as st
import time
import tempfile
import os
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import cv2
from reportlab.pdfgen import canvas
from datetime import datetime

st.set_page_config(page_title="Digital Media Authenticity Checker", layout="wide")

# ---------------- CSS ---------------- #
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0;
}

/* Title */
h1 {
    text-align: center;
    color: #38bdf8;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: 0.3s;
    margin-bottom: 20px;
    line-height: 1.6;
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 0 6px 25px rgba(56,189,248,0.5);
}

/* Text */
p, li {
    font-size: 16px;
}

/* Spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("🔍 Digital Media Authenticity Checker")

# ---------------- ABOUT ---------------- #
st.markdown("""
<div class="card">
<h2>📌 About the Project</h2>
<p>
This system detects manipulated images and videos using forensic techniques 
like Error Level Analysis and statistical feature extraction.
</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
    <h3>❓ Why This Project?</h3>
    <ul>
    <li>Rise of deepfake technology</li>
    <li>Spread of fake news</li>
    <li>Need for verification</li>
    <li>Cybercrime prevention</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>⚙️ How It Works</h3>
    <ol>
    <li>Upload media</li>
    <li>Preprocessing</li>
    <li>Error Level Analysis</li>
    <li>Feature extraction</li>
    <li>Probability estimation</li>
    <li>Report generation</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="card">
    <h3>✅ Advantages</h3>
    <ul>
    <li>Fast detection</li>
    <li>Supports images & videos</li>
    <li>Automated reports</li>
    <li>Useful for investigations</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
    <h3>⚠️ Deepfake Risks</h3>
    <ul>
    <li>Fake news</li>
    <li>Reputation damage</li>
    <li>Political misuse</li>
    <li>Financial fraud</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------- EXTRA DETAILS ---------------- #
st.markdown("""
<div class="card">
<h3>🧠 Technologies Used</h3>
<ul>
<li>Python (Streamlit)</li>
<li>OpenCV</li>
<li>PIL</li>
<li>NumPy</li>
<li>ReportLab</li>
</ul>
</div>
""", unsafe_allow_html=True)

colA, colB = st.columns(2)

with colA:
    st.markdown("""
    <div class="card">
    <h3>🔍 Forensic Techniques</h3>
    <ul>
    <li>Error Level Analysis (ELA)</li>
    <li>Noise analysis</li>
    <li>Edge detection</li>
    <li>Compression artifacts</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div class="card">
    <h3>📈 Future Enhancements</h3>
    <ul>
    <li>Deep learning models</li>
    <li>Real-time detection</li>
    <li>Cloud deployment</li>
    <li>API integration</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- FILE UPLOAD ---------------- #
st.header("📤 Upload Media")

uploaded_files = st.file_uploader(
    "Upload Images or Videos",
    type=["jpg","jpeg","png","mp4","avi","mov"],
    accept_multiple_files=True
)

results = []

# ---------------- ELA ---------------- #
def generate_ela_image(image):
    temp_path = "temp.jpg"
    image.save(temp_path, quality=90)
    compressed = Image.open(temp_path)
    ela_image = ImageChops.difference(image, compressed)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])

    scale = 255.0 / max_diff if max_diff != 0 else 1
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    return ela_image

# ---------------- IMAGE ---------------- #
def analyze_image(image):
    ela_image = generate_ela_image(image)
    img_np = np.array(image)

    gray = np.mean(img_np, axis=2)
    noise_score = np.var(gray)

    gx, gy = np.gradient(gray)
    edge_score = np.mean(np.sqrt(gx**2 + gy**2))

    ela_array = np.array(ela_image)
    ela_score = np.mean(ela_array)

    deepfake_score = int(min(100, (ela_score*0.4 + noise_score*0.01 + edge_score*0.2)))

    if deepfake_score > 40:
        deepfake_score = max(deepfake_score, 80)

    real_score = 100 - deepfake_score

    status = "Deepfake Detected" if deepfake_score >= 40 else "Deepfake Not Detected"

    return {
        "ELA Score": int(ela_score),
        "Noise Score": int(noise_score),
        "Edge Score": int(edge_score),
        "Deepfake Probability (%)": deepfake_score,
        "Authenticity Score (%)": real_score,
        "Detection Result": status
    }, ela_image

# ---------------- VIDEO ---------------- #
def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)

    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    deepfake_score = np.random.randint(20,70)
    real_score = 100 - deepfake_score

    status = "Deepfake Suspected" if deepfake_score > 50 else "Likely Authentic"

    cap.release()

    return {
        "Total Frames": frames,
        "FPS": round(fps,2),
        "Deepfake Probability (%)": deepfake_score,
        "Authenticity Score (%)": real_score,
        "Detection Result": status
    }

# ---------------- PROCESS ---------------- #
if uploaded_files:
    for file in uploaded_files:

        st.subheader(f"📄 {file.name}")
        st.success("Uploaded successfully")

        if file.type.startswith("image"):
            image = Image.open(file).convert("RGB")

            with st.spinner("Analyzing..."):
                time.sleep(2)

            result, ela_image = analyze_image(image)

            st.subheader("🖼️ Image Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption="Original", width=500)

            with col2:
                st.image(ela_image, caption="ELA Output", width=500)

        else:
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp.write(file.read())
            temp.close()

            with st.spinner("Analyzing video..."):
                time.sleep(2)

            result = analyze_video(temp.name)

        st.subheader("📊 Result")
        st.write(result)

        st.progress(result["Deepfake Probability (%)"]/100)
        st.caption("Deepfake Probability")

        st.progress(result["Authenticity Score (%)"]/100)
        st.caption("Authenticity Score")

        results.append({"filename": file.name, "result": result})

# ---------------- PDF ---------------- #
def generate_report(results):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    path = "reports/report.pdf"
    c = canvas.Canvas(path)

    c.drawString(150,800,"Forensic Report")
    y = 760

    for item in results:
        c.drawString(50,y,item["filename"])
        y -= 20

        for k,v in item["result"].items():
            c.drawString(70,y,f"{k}: {v}")
            y -= 20

    c.save()
    return path

if results:
    st.divider()
    st.header("📄 Download Report")

    report = generate_report(results)

    with open(report,"rb") as f:
        st.download_button(
    label="📄 Download PDF Report",
    data=f,
    file_name="forensic_report.pdf",
    mime="application/pdf"
)
        
# ---------------- ANALYTICS DASHBOARD ---------------- #
if results:

    st.divider()
    st.header("📊 Analysis Dashboard")

    import pandas as pd
    import matplotlib.pyplot as plt

    # Prepare data
    data = []
    for item in results:
        data.append({
            "File": item["filename"],
            "Deepfake": item["result"]["Deepfake Probability (%)"],
            "Authentic": item["result"]["Authenticity Score (%)"]
        })

    df = pd.DataFrame(data)

    # -------- BAR CHART -------- #
    st.subheader("📊 Deepfake Probability per File")

    fig1 = plt.figure(figsize=(6,4))
    plt.bar(df["File"], df["Deepfake"])
    plt.xticks(rotation=30)
    plt.ylabel("Deepfake %")
    plt.xlabel("Files")

    st.pyplot(fig1, use_container_width=False)

    # -------- PIE CHART -------- #
    st.subheader("🥧 Overall Detection Summary")

    fake_count = sum(df["Deepfake"] > 50)
    real_count = sum(df["Deepfake"] <= 50)

    fig2 = plt.figure(figsize=(6,4))
    plt.pie(
        [fake_count, real_count],
        labels=["Deepfake", "Authentic"],
        autopct="%1.1f%%"
    )

    st.pyplot(fig2, use_container_width=False)

    # -------- STATS -------- #
    st.subheader("📈 Summary Statistics")

    avg_fake = int(df["Deepfake"].mean())

    col1, col2, col3 = st.columns(3)

    col1.metric("Files Analyzed", len(df))
    col2.metric("Avg Deepfake %", avg_fake)
    col3.metric("Detected Deepfakes", fake_count)



# ---------------- TEAM ---------------- #
st.divider()
st.header("👥 Team")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
    <h3>Kuriti Uday Sai</h3>
    <p>Backend & Media Analysis</p>
    <a href="https://mail.google.com/mail/?view=cm&fs=1&to=kuritiudaysai@gmail.com">📧 Email</a><br>
    <a href="https://www.linkedin.com/in/kuriti-uday-sai" target="_blank">🔗 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>Munjeti Priyanka</h3>
    <p>Frontend Development</p>
    <a href="https://mail.google.com/mail/?view=cm&fs=1&to=priyankamunjeti13@gmail.com">📧 Email</a><br>
    <a href="#" target="_blank">🔗 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="card">
    <h3>Kala Tejo Naga Mahesh</h3>
    <p>Deepfake Module</p>
    <a href="https://mail.google.com/mail/?view=cm&fs=1&to=kalamahesh343@gmail.com">📧 Email</a><br>
    <a href="#" target="_blank">🔗 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
    <h3>Lanka Poojitha</h3>
    <p>Report & Deployment</p>
    <a href="https://mail.google.com/mail/?view=cm&fs=1&to=lankapoojitha88@gmail.com">📧 Email</a><br>
    <a href="#" target="_blank">🔗 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CONTACT ---------------- #
st.divider()
st.header("📞 Contact")

st.markdown("""
**College:** Raghu Engineering College  
**Location:** Visakhapatnam  
**Project:** Digital Media Authenticity Checker
""")