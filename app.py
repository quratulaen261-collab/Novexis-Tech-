import streamlit as st
import pandas as pd
import csv
from datetime import datetime

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Novexis Tech – Testimonial Bot",
    page_icon="⭐",
    layout="centered"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("⭐ Novexis Tech – Testimonial Bot")
st.write("We value your feedback! Please share your experience below 👇")

# -----------------------------
# INPUT FORM
# -----------------------------
name = st.text_input("👤 Your Name")
email = st.text_input("📩 Email (optional)")
rating = st.slider("⭐ Rating", 1, 5)
feedback = st.text_area("💬 Your Feedback")

image_file = st.file_uploader("📸 Upload an optional image (product/your photo)", type=["jpg", "jpeg", "png"])

submit = st.button("Submit Testimonial")

# -----------------------------
# WHEN USER SUBMITS
# -----------------------------
if submit:
    if name.strip() == "" or feedback.strip() == "":
        st.error("⚠ Please enter at least your name and your feedback.")
    else:
        # Save data to CSV
        file_path = "testimonials.csv"

        # Create CSV if not exists
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.DataFrame(columns=["timestamp", "name", "email", "rating", "feedback", "image_filename"])
            df.to_csv(file_path, index=False)

        # Save image
        image_name = ""
        if image_file:
            image_name = f"image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            with open(f"uploads/{image_name}", "wb") as f:
                f.write(image_file.getbuffer())

        # Append new row
        new_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "email": email,
            "rating": rating,
            "feedback": feedback,
            "image_filename": image_name
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_path, index=False)

        st.success("🎉 Thank you! Your testimonial has been submitted successfully.")
        st.balloons()

# -----------------------------
# SHOW ALL TESTIMONIALS (ADMIN AREA)
# -----------------------------
st.write("---")
st.subheader("📄 Previous Testimonials (Admin Preview)")

try:
    df = pd.read_csv("testimonials.csv")
    st.dataframe(df)
except:
    st.info("No testimonials yet.")
