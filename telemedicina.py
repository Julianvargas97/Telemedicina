from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import re
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
import webbrowser
import threading

def generar_enlace_videollamada():
    enlace = f"https://meet.google.com/{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}"
    return enlace

def validar_correo(correo):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, correo)


def enviar_correo(correo_entry, spinner_frame):
    destinatario = correo_entry.get()
    if not destinatario:
        messagebox.showwarning("Campo vacío", "Por favor ingresa un correo destinatario.")
        return
    if not validar_correo(destinatario):
        messagebox.showwarning("Correo inválido", "Por favor ingresa un correo electrónico válido.")
        return

    spinner_frame.grid(row=5, column=0, pady=(10,0))
    remitente = "innovacioneinvestigacion@hospitalsanjose.gov.co"
    password = "" # Añadir la contraseña real aquí

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Telemedicina Hospital San José de Popayán"
    enlace = generar_enlace_videollamada()
    cuerpo = f"Hola,\n\nAquí está el enlace para tu consulta de telemedicina: {enlace}\n\nSaludos,\nHospital San José de Popayán"
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    def envio():
        try:
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, password)
            servidor.sendmail(remitente, destinatario, mensaje.as_string())
            servidor.quit()
            messagebox.showinfo("Correo enviado", "El enlace de la videollamada fue enviado con éxito.")
            correo_entry.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")
        finally:
            spinner_frame.grid_forget()

    threading.Thread(target=envio, daemon=True).start()

def iniciar_teleconsulta():
    webbrowser.open(generar_enlace_videollamada())

def reproducir_gif(label, frames, index):
    label.configure(image=frames[index])
    label.after(100, reproducir_gif, label, frames, (index+1)%len(frames))

def crear_ventana():
    root = Tk()
    root.title("Teleconsulta Hospital Universitario San José de Popayán")
    root.geometry("800x600")

    fondo = Image.open("HUSJ.jpeg").resize((800, 600), Image.Resampling.LANCZOS)
    fondo_img = ImageTk.PhotoImage(fondo)
    Label(root, image=fondo_img).place(relwidth=1, relheight=1)

    frame = Frame(root, bg="white", bd=2, relief="solid", highlightthickness=5, highlightbackground="#4db8ff", width=500, height=350)
    frame.place(relx=0.5, rely=0.4, anchor="center")

    Label(frame, text="Teleconsulta Hospital Universitario San José", font=("Segoe UI", 18, "bold"), bg="white", fg="#006699").grid(row=0, column=0, pady=15)
    Label(frame, text="Correo del paciente:", font=("Segoe UI", 12), bg="white", fg="black").grid(row=1, column=0, pady=(0,10))

    correo_entry = Entry(frame, font=("Segoe UI", 10), width=25, bd=2, relief="solid", highlightthickness=1, highlightcolor="#4db8ff")
    correo_entry.grid(row=2, column=0, pady=(0,15))

    spinner_frame = Frame(frame, bg="white", bd=1, relief="flat", highlightbackground="#0073e6", highlightthickness=1)
    Label(spinner_frame, text="Enviando enlace...", font=("Segoe UI", 11, "italic"), fg="#0073e6", bg="white").pack(side="left", padx=5)

    spinner_img = Image.open("spinner.gif")
    spinner_frames = [ImageTk.PhotoImage(f.copy().resize((20,20), Image.Resampling.LANCZOS)) for f in ImageSequence.Iterator(spinner_img)]
    spinner_lbl = Label(spinner_frame, bg="white")
    spinner_lbl.pack(side="left", padx=5)
    reproducir_gif(spinner_lbl, spinner_frames, 0)
    spinner_frame.grid_forget()

    Button(frame, text="Enviar Enlace de Teleconsulta", font=("Segoe UI",10,"bold"), bg="#0073e6", fg="white", padx=20, pady=10, relief="flat", bd=0,
           command=lambda: enviar_correo(correo_entry, spinner_frame)).grid(row=3, column=0, pady=15)
    Button(frame, text="Iniciar Teleconsulta", font=("Segoe UI",10,"bold"), bg="#28a745", fg="white", padx=20, pady=10, relief="flat", bd=0,
           command=iniciar_teleconsulta).grid(row=4, column=0, pady=10)

    Label(root, text="Innovación e Investigación 2025  |  David Mesa Martínez & Julian Andrés Vargas", font=("Segoe UI",8), fg="gray", bg="#f4f4f4").pack(side="bottom", fill="x", pady=10)

    root.mainloop()

crear_ventana()
