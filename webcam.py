import tkinter as tk
from tkinter import messagebox, filedialog  # Ajout de l'importation
import cv2
from PIL import Image, ImageTk
import numpy as np

# Charger le modèle de détection de visage
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')

# Fonction pour capturer et afficher les images de la webcam
def show_frame():
    _, frame = cap.read()
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

# Fonction pour prendre une photo
def take_photo():
    _, frame = cap.read()
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            # Ajouter une marge autour du cadre
            margin = 50  # Vous pouvez ajuster cette valeur
            startX = max(0, startX - margin)
            startY = max(0, startY - margin)
            endX = min(w, endX + margin)
            endY = min(h, endY + margin)
            
            face = frame[startY:endY, startX:endX]
            
            # Demander à l'utilisateur où enregistrer le fichier
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, face)
                messagebox.showinfo("Information", f"Photo prise et sauvegardée sous '{file_path}'")
            return

    messagebox.showwarning("Avertissement", "Aucun visage détecté")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Mon Interface")

# Créer un label
label = tk.Label(root, text="Bonjour, bienvenue photo identité crée par EnderMythex!")
label.pack(pady=10)

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)

# Créer un label pour afficher la vidéo
lmain = tk.Label(root)
lmain.pack()

# Créer un bouton pour prendre une photo
photo_button = tk.Button(root, text="Prendre une photo", command=take_photo)
photo_button.pack(pady=10)

# Lancer la capture vidéo
show_frame()

# Lancer la boucle principale
root.mainloop()