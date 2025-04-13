
import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import cv2
import mediapipe as mp

# Personnalisation CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .css-18e3th9 {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", ["🏠 Accueil", "🧪 Essayage virtuel"])

if page == "🏠 Accueil":
    st.title("👗 Bienvenue dans la cabine d’essayage virtuelle")
    st.image("https://cdn.pixabay.com/photo/2017/08/06/18/03/fashion-2590874_1280.jpg", use_column_width=True)
    st.markdown(
        """
        Cette application vous permet d'essayer virtuellement des vêtements grâce à votre **webcam** ou en **uploadant une photo** 📸

        👉 Utilisez le menu à gauche pour accéder à l'essayage.

        ---
        """
    )
else:
    st.title("👚 Cabine d’essayage virtuelle")

    mode = st.radio("Choisir un mode :", ["Photo", "Caméra en direct"])

    clothing_files = {
        "T-shirt": "images/tshirt.png",
        "Robe": "images/dress.png",
        "Sac à main": "images/handbag.png",
        "Veste": "images/jacket.png",
        "Pull": "images/sweater.png",
        "Pantalon": "images/pants.png",
        "Short": "images/shorts.png",
        "Casquette": "images/cap.png",
        "Chaussure": "images/shoes.png"
    }

    selected_item = st.selectbox("Choisir un vêtement ou accessoire :", list(clothing_files.keys()))
    clothing_img = Image.open(clothing_files[selected_item]).convert("RGBA")

    def overlay_clothing(base_img, clothing_img, shoulder1, shoulder2, y_offset_factor=0.25):
        width = abs(shoulder2[0] - shoulder1[0]) * 2
        height = int(width * clothing_img.height / clothing_img.width)
        x = int((shoulder1[0] + shoulder2[0]) / 2 - width / 2)
        y = int(shoulder1[1] - height * y_offset_factor)
        clothing_resized = clothing_img.resize((width, height))
        base_img.paste(clothing_resized, (x, y), clothing_resized)
        return base_img

    if mode == "Photo":
        uploaded_file = st.file_uploader("Uploader une photo", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            user_image = Image.open(uploaded_file).convert("RGBA")
            user_image = ImageOps.contain(user_image, (500, 700))
            result = user_image.copy()
            width = int(user_image.width * 0.6)
            height = int(width * clothing_img.height / clothing_img.width)
            x = int((user_image.width - width) / 2)
            y = int(user_image.height * 0.35)
            clothing_resized = clothing_img.resize((width, height))
            result.paste(clothing_resized, (x, y), clothing_resized)
            st.image(result, caption="Aperçu de l'essayage", use_column_width=True)

    elif mode == "Caméra en direct":
        run = st.checkbox("Activer la caméra")
        if run:
            mp_pose = mp.solutions.pose
            pose = mp_pose.Pose()
            cap = cv2.VideoCapture(0)
            frame_placeholder = st.empty()

            while run and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)
                frame_pil = Image.fromarray(image_rgb).convert("RGBA")

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    h, w, _ = frame.shape
                    left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w),
                                     int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h))
                    right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w),
                                      int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h))
                    frame_pil = overlay_clothing(frame_pil, clothing_img, left_shoulder, right_shoulder)

                frame_np = np.array(frame_pil)
                frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGBA2BGR)
                frame_placeholder.image(frame_bgr, channels="BGR", use_column_width=True)

            cap.release()
