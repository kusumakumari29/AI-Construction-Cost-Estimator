
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

# Load model and encoders
model = joblib.load("model.pkl")
material_encoder = joblib.load("material.pkl")
location_encoder = joblib.load("location.pkl")
type_encoder = joblib.load("type.pkl")

st.title("🏗️ AI-Based Construction Cost Estimator")
st.write("Predict construction cost using AI")

area = st.number_input("Enter Area (sq.ft)", min_value=500, max_value=10000, value=1000)
floors = st.selectbox("Number of Floors", [1, 2, 3])

material = st.selectbox("Material Quality", ["Basic", "Standard", "Premium"])
location = st.selectbox("Location", ["Urban", "Rural"])
building_type = st.selectbox("Building Type", ["Residential", "Commercial"])
city = st.selectbox(
    "Select City",
    [
        "Visakhapatnam",
        "Vijayawada",
        "Guntur",
        "Nellore",
        "Kurnool",
        "Rajahmundry",
        "Kakinada",
        "Tirupati",
        "Anantapur",
        "Kadapa",
        "Eluru",
        "Ongole",
        "Srikakulam",
        "Vizianagaram",
        "Machilipatnam",
        "Nandyal",
        "Tenali",
        "Chittoor",
        "Hindupur",
        "Palakollu",
        "Bhimavaram",
        "Amalapuram",
        "Tadepalligudem",
        "Proddatur"
    ]
)
interior = st.checkbox("Include Interior Design (+ ₹500/sq.ft)")

if st.button("Estimate Cost"):

    material_val = material_encoder.transform([material])[0]
    location_val = location_encoder.transform([location])[0]
    type_val = type_encoder.transform([building_type])[0]

    input_data = pd.DataFrame({
        "Area": [area],
        "Floors": [floors],
        "Material": [material_val],
        "Location": [location_val],
        "Type": [type_val]
    })

    prediction = model.predict(input_data)[0]
    city_multiplier = {
    "Visakhapatnam": 1.20,
    "Vijayawada": 1.15,
    "Guntur": 1.12,
    "Nellore": 1.10,
    "Kurnool": 1.08,
    "Rajahmundry": 1.10,
    "Kakinada": 1.09,
    "Tirupati": 1.18,
    "Anantapur": 1.05,
    "Kadapa": 1.05,
    "Eluru": 1.08,
    "Ongole": 1.07,
    "Srikakulam": 1.03,
    "Vizianagaram": 1.03,
    "Machilipatnam": 1.08,
    "Nandyal": 1.04,
    "Tenali": 1.08,
    "Chittoor": 1.07,
    "Hindupur": 1.04,
    "Palakollu": 1.06,
    "Bhimavaram": 1.07,
    "Amalapuram": 1.05,
    "Tadepalligudem": 1.06,
    "Proddatur": 1.04
}

    prediction = prediction * city_multiplier[city]
    # Interior Cost
    if interior:
       prediction += area * 500

# GST
    gst = prediction * 0.18
    total_cost = prediction + gst

# Cost per Sq.ft
    cost_per_sqft = total_cost / area

    st.success(f"🏗️ Estimated Construction Cost: ₹ {prediction:,.0f}")
    st.info(f"🧾 GST (18%): ₹ {gst:,.0f}")
    st.success(f"💰 Total Cost (Including GST): ₹ {total_cost:,.0f}")

    st.metric("📏 Cost per Sq.ft", f"₹ {cost_per_sqft:,.0f}")

    foundation = prediction * 0.15
    walls = prediction * 0.20
    roofing = prediction * 0.15
    finishing = prediction * 0.30
    labour = prediction * 0.20

    st.subheader("📊 Cost Breakdown")
    st.write(f"🧱 Foundation : ₹ {foundation:,.0f}")
    st.write(f"🏢 Walls : ₹ {walls:,.0f}")
    st.write(f"🏠 Roofing : ₹ {roofing:,.0f}")
    st.write(f"🎨 Finishing : ₹ {finishing:,.0f}")
    st.write(f"👷 Labour : ₹ {labour:,.0f}")

    # Pie Chart
    labels = ["Foundation", "Walls", "Roofing", "Finishing", "Labour"]
    sizes = [foundation, walls, roofing, finishing, labour]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    st.pyplot(fig)

    # PDF Generation

    pdf_file = "construction_estimate.pdf"
    # Material Quantity Estimation
    cement_bags = area * 0.4
    steel_tons = area * 0.0035
    sand_cft = area * 0.65
    bricks = area * 35
    c = canvas.Canvas(pdf_file)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Construction Cost Estimate")

    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Estimated Cost: Rs. {prediction:,.0f}")
    c.drawString(100, 740, f"Foundation: Rs. {foundation:,.0f}")
    c.drawString(100, 720, f"Walls: Rs. {walls:,.0f}")
    c.drawString(100, 700, f"Roofing: Rs. {roofing:,.0f}")
    c.drawString(100, 680, f"Finishing: Rs. {finishing:,.0f}")
    c.drawString(100, 660, f"Labour: Rs. {labour:,.0f}")
    c.drawString(100, 640, f"GST (18%): Rs. {gst:,.0f}")
    c.drawString(100, 620, f"Total Cost: Rs. {total_cost:,.0f}")
    c.drawString(100, 600, f"Cement Bags: {cement_bags:.0f}")
    c.drawString(100, 580, f"Steel: {steel_tons:.2f} Tons")
    c.drawString(100, 560, f"Sand: {sand_cft:.0f} CFT")
    c.drawString(100, 540, f"Bricks: {bricks:.0f}")

    c.save()

    with open(pdf_file, "rb") as pdf:
        st.download_button(
            label="📄 Download Estimate PDF",
            data=pdf,
            file_name="Construction_Estimate.pdf",
            mime="application/pdf"
        )
# Material Quantity Estimation

cement_bags = area * 0.4
steel_tons = area * 0.0035
sand_cft = area * 0.65
bricks = area * 35

st.subheader("🧱 Material Quantity Estimation")

st.write(f"🪨 Cement Bags : {cement_bags:.0f}")
st.write(f"🔩 Steel : {steel_tons:.2f} Tons")
st.write(f"🏖️ Sand : {sand_cft:.0f} CFT")
st.write(f"🧱 Bricks : {bricks:.0f}")