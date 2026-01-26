import cv2
import face_recognition
import os
import customtkinter as ctk
from tkinter import messagebox

VAULT_PATH = "vault"
AUTHORIZED_IMAGE = "authorized_face.jpg"

def hide_vault():
    os.system(f'attrib +h "{VAULT_PATH}"')

def show_vault():
    os.system(f'attrib -h "{VAULT_PATH}"')

def recognize_face():
    try:
        known_image = face_recognition.load_image_file(AUTHORIZED_IMAGE)
        known_encoding = face_recognition.face_encodings(known_image)[0]

        cap = cv2.VideoCapture(0)
        success = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                match = face_recognition.compare_faces([known_encoding], face_encoding)
                if match[0]:
                    success = True
                    break

            cv2.imshow("Face Authentication - Press 'q' to exit", frame)
            if success or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return success

    except Exception as e:
        messagebox.showerror("Error", f"Face recognition failed!\n{e}")
        return False

# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Secure Folder Vault 🔐")
app.geometry("400x300")

def unlock():
    message_label.configure(text="Scanning face...", text_color="yellow")
    app.update()
    if recognize_face():
        show_vault()
        message_label.configure(text="Vault Unlocked!", text_color="green")
    else:
        message_label.configure(text="Access Denied", text_color="red")

def lock():
    hide_vault()
    message_label.configure(text="Vault Locked", text_color="green")

ctk.CTkLabel(app, text="🔐 Secure Folder Vault", font=("Arial", 22)).pack(pady=20)

unlock_btn = ctk.CTkButton(app, text="Unlock Vault", command=unlock)
unlock_btn.pack(pady=10)

lock_btn = ctk.CTkButton(app, text="Lock Vault", command=lock)
lock_btn.pack(pady=10)

message_label = ctk.CTkLabel(app, text="")
message_label.pack(pady=20)

app.mainloop()
