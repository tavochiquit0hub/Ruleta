import tkinter as tk
import random
import json
from tkinter import messagebox
from PIL import Image, ImageTk  # Importar PIL para manejar la imagen

# Variables globales
vidas_jugador_1 = 3
vidas_jugador_2 = 3
jugador_actual = 1
ronda_actual = 1
indice_bala = 0
cargador = []
balas_reales = 0
balas_falsas = 0
ganadas_jugador_1 = 0
ganadas_jugador_2 = 0


# Cargar registros de victorias
def cargar_registros():
    global ganadas_jugador_1, ganadas_jugador_2
    try:
        with open('registro.json', 'r') as f:
            registros = json.load(f)
            ganadas_jugador_1 = registros.get("jugador_1", 0)
            ganadas_jugador_2 = registros.get("jugador_2", 0)
    except FileNotFoundError:
        ganadas_jugador_1 = 0
        ganadas_jugador_2 = 0


# Guardar registros de victorias
def guardar_registros():
    with open('registro.json', 'w') as f:
        json.dump({"jugador_1": ganadas_jugador_1, "jugador_2": ganadas_jugador_2}, f)


# Función para mostrar instrucciones
def mostrar_instrucciones():
    instrucciones = (
        "Instrucciones del Juego:\n\n"
        "1. Cada jugador toma turnos para disparar.\n"
        "2. En cada ronda, los jugadores tienen un número determinado de vidas.\n"
        "3. Al iniciar cada ronda, se muestra la cantidad de balas reales y falsas.\n"
        "4. Los jugadores pueden elegir disparar a sí mismos o a su contrincante.\n"
        "5. Si el jugador dispara y la bala es real, el otro jugador o él mismo perderá una vida.\n"
        "6. El juego continúa hasta que un jugador pierde todas sus vidas.\n"
        "7. El jugador que gane más rondas será el ganador del juego.\n"
    )
    messagebox.showinfo("Instrucciones", instrucciones)


# Función para centrar la ventana
def centrar_ventana(ventana, ancho=400, alto=400):
    pantalla_x = ventana.winfo_screenwidth()
    pantalla_y = ventana.winfo_screenheight()
    x = (pantalla_x // 2) - (ancho // 2)
    y = (pantalla_y // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')


# Función para generar el cargador con balas reales y falsas
def generar_cargador(ronda):
    global cargador, balas_reales, balas_falsas
    balas_reales = 2 if ronda == 1 else (3 if ronda == 2 else 4)
    balas_falsas = 6 - balas_reales
    cargador = [True] * balas_reales + [False] * balas_falsas
    random.shuffle(cargador)


# Función para actualizar las vidas en pantalla
def actualizar_vidas():
    label_vidas_jugador_1.config(text=f"Vidas Jugador 1: {vidas_jugador_1}")
    label_vidas_jugador_2.config(text=f"Vidas Jugador 2: {vidas_jugador_2}")


# Función para actualizar el turno en pantalla
def actualizar_turno():
    label_turno.config(text=f"Turno del Jugador {jugador_actual}")


# Función para disparar
def disparar(objetivo, ventana_juego):
    global vidas_jugador_1, vidas_jugador_2, jugador_actual, indice_bala

    if indice_bala >= len(cargador):
        messagebox.showinfo("Fin del cargador", "Se ha terminado el cargador. Generando uno nuevo...")
        generar_cargador(ronda_actual)
        indice_bala = 0
        mostrar_balas(ronda_actual)

    bala_actual = cargador[indice_bala]
    indice_bala += 1

    resultado = "falsa"
    perdedor = ""

    if bala_actual:  # Si es una bala real
        resultado = "real"
        if objetivo == "contrincante":
            if jugador_actual == 1:
                vidas_jugador_2 -= 1
                perdedor = "Jugador 2"
            else:
                vidas_jugador_1 -= 1
                perdedor = "Jugador 1"
        elif objetivo == "self":
            if jugador_actual == 1:
                vidas_jugador_1 -= 1
                perdedor = "Jugador 1"
            else:
                vidas_jugador_2 -= 1
                perdedor = "Jugador 2"
    else:  # Si es una bala falsa
        if objetivo != "self":
            jugador_actual = 2 if jugador_actual == 1 else 1

    mensaje = f"La bala fue {resultado}."
    if resultado == "real":
        mensaje += f"\n{perdedor} ha perdido una vida."

    # Crear ventana de resultado personalizada
    resultado_ventana = tk.Toplevel()
    resultado_ventana.title("Resultado del Disparo")
    resultado_ventana.configure(bg="black")
    centrar_ventana(resultado_ventana, 300, 200)
    label_resultado = tk.Label(resultado_ventana, text=mensaje, fg="red", bg="black")
    label_resultado.pack()
    btn_ok = tk.Button(resultado_ventana, text="Aceptar", command=resultado_ventana.destroy, fg="red", bg="black",
                       borderwidth=0)
    btn_ok.pack()

    actualizar_vidas()
    if vidas_jugador_1 == 0 or vidas_jugador_2 == 0:
        ganador = "Jugador 1" if vidas_jugador_2 == 0 else "Jugador 2"
        messagebox.showinfo("Fin de la Ronda", f"{ganador} ha ganado la ronda.")
        ronda_ganada(ganador, ventana_juego)
    else:
        actualizar_turno()


# Función para mostrar las balas al inicio de cada ronda
def mostrar_balas(ronda):
    cargador_ventana = tk.Toplevel()
    cargador_ventana.title("Cargador")
    cargador_ventana.configure(bg="black")
    centrar_ventana(cargador_ventana, 300, 200)
    mensaje = f"Balas Reales: {balas_reales}, Balas Falsas: {balas_falsas}"
    label_cargador = tk.Label(cargador_ventana, text=mensaje, fg="red", bg="black")
    label_cargador.pack()
    btn_ok = tk.Button(cargador_ventana, text="Aceptar", command=cargador_ventana.destroy, fg="red", bg="black",
                       borderwidth=0)
    btn_ok.pack()


# Función para manejar el final de la ronda y cambiar de ronda
def ronda_ganada(ganador, ventana_juego):
    global ronda_actual, vidas_jugador_1, vidas_jugador_2, indice_bala
    if ronda_actual >= 3:
        messagebox.showinfo("Fin del Juego", f"{ganador} ha ganado el juego.")
        if ganador == "Jugador 1":
            global ganadas_jugador_1
            ganadas_jugador_1 += 1
        else:
            global ganadas_jugador_2
            ganadas_jugador_2 += 1
        guardar_registros()
        ventana_juego.destroy()
        return

    ronda_actual += 1
    vidas_jugador_1 = 3 if ronda_actual == 1 else (5 if ronda_actual == 2 else 8)
    vidas_jugador_2 = 3 if ronda_actual == 1 else (5 if ronda_actual == 2 else 8)
    indice_bala = 0
    generar_cargador(ronda_actual)
    actualizar_vidas()
    mostrar_balas(ronda_actual)


# Función para iniciar el juego
def iniciar_juego():
    global vidas_jugador_1, vidas_jugador_2, ronda_actual, indice_bala

    vidas_jugador_1 = 3
    vidas_jugador_2 = 3
    ronda_actual = 1
    indice_bala = 0
    generar_cargador(ronda_actual)

    ventana_juego = tk.Toplevel(ventana)
    ventana_juego.title("Juego de Ruleta Rusa")
    ventana_juego.configure(bg="black")
    centrar_ventana(ventana_juego, 400, 400)

    # Cargar la imagen de fondo
    imagen_fondo = Image.open("/mnt/data/pistola-balas-traumaticas-negro-arma-autodefensa_185193-14507.webp")
    imagen_fondo = imagen_fondo.resize((400, 400), Image.ANTIALIAS)
    fondo = ImageTk.PhotoImage(imagen_fondo)

    canvas = tk.Canvas(ventana_juego, width=400, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=fondo, anchor="nw")

    # Actualizar las vidas y el turno al iniciar el juego
    global label_vidas_jugador_1, label_vidas_jugador_2, label_turno
    label_vidas_jugador_1 = tk.Label(canvas, text=f"Vidas Jugador 1: {vidas_jugador_1}", fg="white", bg="black")
    label_vidas_jugador_2 = tk.Label(canvas, text=f"Vidas Jugador 2: {vidas_jugador_2}", fg="white", bg="black")
    label_turno = tk.Label(canvas, text=f"Turno del Jugador {jugador_actual}", fg="white", bg="black")

    label_vidas_jugador_1.pack()
    label_vidas_jugador_2.pack()
    label_turno.pack()

    mostrar_balas(ronda_actual)

    boton_disparar_contrincante = tk.Button(ventana_juego, text="Disparar al Contrincante",
                                            command=lambda: disparar("contrincante", ventana_juego))
    boton_disparar_contrincante.pack(side="left", padx=20, pady=20)

    boton_disparar_a_mi = tk.Button(ventana_juego, text="Disparar a mí mismo",
                                    command=lambda: disparar("self", ventana_juego))
    boton_disparar_a_mi.pack(side="right", padx=20, pady=20)


# Función principal
ventana = tk.Tk()
ventana.title("Ruleta Rusa")
ventana.configure(bg="black")
centrar_ventana(ventana)

# Crear botones principales
boton_jugar = tk.Button(ventana, text="Jugar", command=iniciar_juego, fg="red", bg="black", borderwidth=0)
boton_jugar.pack(pady=20)

boton_instrucciones = tk.Button(ventana, text="Instrucciones", command=mostrar_instrucciones, fg="red", bg="black",
                                borderwidth=0)
boton_instrucciones.pack(pady=20)

boton_salir = tk.Button(ventana, text="Salir", command=ventana.quit, fg="red", bg="black", borderwidth=0)
boton_salir.pack(pady=20)

# Cargar registros al iniciar
cargar_registros()

ventana.mainloop()
