import cv2
import numpy as np
from tensorflow.keras.models import load_model
import smtplib
from email.mime.text import MIMEText
import platform

# =========================
# 🔊 Alarm function
# =========================
def play_alarm():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 700)
    else:
        print("\a")

# =========================
# 🔥 Load model
# =========================
model = load_model("fire_detection.h5")

_, h, w, c = model.input_shape
print("Model expects:", h, w, c)

# =========================
# 📧 Email function
# =========================
def send_email():
    sender = "ramyaramamoorthi19@gmail.com"
    receiver ="ramyaramamoorthi19@gmail.com"
    password = "knoj bwig vktx jaij"

    msg = MIMEText("🔥 Fire Detected! Check immediately!")
    msg['Subject'] = "Fire Alert"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("📧 Email Sent")
    except Exception as e:
        print("Email Error:", e)

# =========================
# 🎥 Camera
# =========================
cap = cv2.VideoCapture(0)

email_sent = False

# =========================
# 🔁 Loop
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess
    img = cv2.resize(frame, (w, h))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Prediction
    prediction = model.predict(img)[0]

    # Probability extract
    if len(prediction) == 1:
        fire_prob = prediction[0]
    else:
        fire_prob = prediction[0]

    print("Fire Probability:", fire_prob)

    # 🔥 Simple threshold logic
    if fire_prob > 0.95:
        label = "FIRE 🔥"
        color = (0, 0, 255)

        print("🔥 FIRE DETECTED")

        # 🔊 Alarm
        play_alarm()

        # 📧 Email only once
        if not email_sent:
            send_email()
            email_sent = True

    else:
        label = "NON FIRE ✅"
        color = (0, 255, 0)
        email_sent = False

    # Display
    cv2.putText(frame, f"{label} ({fire_prob:.2f})",
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Fire Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()