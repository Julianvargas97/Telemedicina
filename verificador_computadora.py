import tkinter as tk
from tkinter import Frame, Button, Label
from PIL import Image, ImageTk
import cv2
import speech_recognition as sr
import threading
import socket
import time

def verificar_sonido():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        estado_label.config(text="Diga 'Hola' dos veces para verificar sonido...")
        audio = r.listen(source, timeout=7)
    try:
        texto = r.recognize_google(audio, language='es-ES')
        conteo = texto.lower().count("hola")
        if conteo >= 2:
            sonido_label.config(text="🎧 Sonido Verificado ✔️", fg="#28a745")
            verificar_estado_final()
        else:
            sonido_label.config(text=f"🎧 Solo detectado 'hola' {conteo} vez/veces ❌", fg="#dc3545")
    except:
        sonido_label.config(text="🎧 Error al reconocer sonido ❌", fg="#dc3545")

def verificar_camara():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        camara_label.config(text="📷 Cámara no detectada ❌", fg="#dc3545")
        return

    estado_label.config(text="Mostrando cámara...")
    tiempo_mostrar = time.time() + 5
    while time.time() < tiempo_mostrar:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow('Verificación de Cámara (presiona Q para cerrar)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    camara_label.config(text="📷 Cámara Verificada ✔️", fg="#28a745")
    verificar_estado_final()

def verificar_internet():
    try:
        socket.create_connection(("8.8.8.8", 53))
        internet_label.config(text="🌐 Internet Verificado ✔️", fg="#28a745")
        verificar_estado_final()
    except:
        internet_label.config(text="🌐 Internet No Disponible ❌", fg="#dc3545")

def verificar_estado_final():
    if ("✔️" in sonido_label.cget("text") and
        "✔️" in camara_label.cget("text") and
        "✔️" in internet_label.cget("text")):
        estado_label.config(text="✅ Conexión Exitosa", fg="#28a745")
        mensaje_verificacion.config(text="Verificación exitosa, ya puedes comenzar...", fg="#28a745", font=("Helvetica", 18, "bold"))
        siguiente_btn.pack()
        siguiente_btn.config(state="normal")

def verificar_conexion():
    estado_label.config(text="Verificando...", fg="#007ACC")
    threading.Thread(target=verificar_sonido).start()
    threading.Thread(target=verificar_camara).start()
    threading.Thread(target=verificar_internet).start()

def abrir_ventana_telemedicina():
    root.destroy()
    import telemedicina
    telemedicina.crear_ventana()

root = tk.Tk()
root.title("Verificador de Conexión - Hospital Universitario San José")
root.geometry("900x600")
root.configure(bg="#f4f4f4")

logo_img = Image.open("logo.png").resize((120, 60), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)

header = Frame(root, bg="#f4f4f4")
header.pack(pady=10)
logo_label = Label(header, image=logo_photo, bg="#f4f4f4")
logo_label.pack()

title_text = ("HOSPITAL UNIVERSITARIO SAN JOSÉ\n"
              "EMPRESA SOCIAL DEL ESTADO - POPAYÁN")
title_label = Label(root, text=title_text, font=("Helvetica", 18, "bold"),
                    fg="#003366", bg="#f4f4f4", justify=tk.CENTER)
title_label.pack(pady=10)

main_frame = Frame(root, bg="#f4f4f4")
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

muñeco_jose = Image.open("Jose.png").resize((200, 220), Image.Resampling.LANCZOS)
muñeco_jose_img = ImageTk.PhotoImage(muñeco_jose)

muñeco_saludo = Image.open("saludo.png").resize((150, 200), Image.Resampling.LANCZOS)
muñeco_saludo_img = ImageTk.PhotoImage(muñeco_saludo)

contenido = Frame(main_frame, bg="#f4f4f4")
contenido.pack(expand=True, fill=tk.BOTH)

muñeco_izq = Label(contenido, image=muñeco_jose_img, bg="#f4f4f4")
muñeco_izq.pack(side="left", padx=20)

centro = Frame(contenido, bg="#f4f4f4")
centro.pack(side="left", expand=True)

estado_label = Label(centro, text="Haz clic en verificar conexión", font=("Arial", 14),
                     bg="#f4f4f4", fg="black")
estado_label.pack(pady=10)

sonido_label = Label(centro, text="🎧 Sonido: Sin verificar", font=("Arial", 12),
                     bg="#f4f4f4", fg="black")
sonido_label.pack(pady=5)

camara_label = Label(centro, text="📷 Cámara: Sin verificar", font=("Arial", 12),
                     bg="#f4f4f4", fg="black")
camara_label.pack(pady=5)

internet_label = Label(centro, text="🌐 Internet: Sin verificar", font=("Arial", 12),
                       bg="#f4f4f4", fg="black")
internet_label.pack(pady=5)

verificar_btn = Button(centro, text="Verificar Conexión", font=("Helvetica", 11, "bold"),
                       bg="#52be80", fg="white", padx=15, pady=10,
                       activebackground="#B76A89", relief="flat", command=verificar_conexion)
verificar_btn.pack(pady=(10, 5))

siguiente_btn = Button(centro, text="Siguiente", font=("Helvetica", 11, "bold"),
                       bg="#7d3c98", fg="white", padx=15, pady=10,
                       activebackground="#7E6FBB", relief="flat", command=abrir_ventana_telemedicina,
                       state="disabled")
siguiente_btn.config(disabledforeground="white")
siguiente_btn.pack(pady=(0, 10))

mensaje_verificacion = Label(centro, text="", font=("Helvetica", 16, "bold"),
                             bg="#f4f4f4", fg="#388E3C")
mensaje_verificacion.pack(pady=10)

muñeco_der = Label(contenido, image=muñeco_saludo_img, bg="#f4f4f4")
muñeco_der.pack(side="right", padx=20)

def animar_balanceo(widget, direccion=1, posicion_inicial=0):
    nueva_pos = posicion_inicial + (2 * direccion)
    widget.place_configure(x=nueva_pos)
    if abs(nueva_pos - posicion_inicial) >= 10:
        direccion *= -1
    root.after(80, animar_balanceo, widget, direccion, posicion_inicial)


footer_label = Label(root, text="Innovación e Investigación 2025  |  David Mesa Martínez & Julian Andrés Vargas",
                     font=("Helvetica", 8), fg="gray", bg="#f4f4f4")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
