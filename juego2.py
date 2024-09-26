import tkinter as tk
import random
import json
from tkinter import messagebox

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
herramientas_jugador_1 = []
herramientas_jugador_2 = []

# Herramientas disponibles
herramientas_disponibles = ["Lupa", "Esposas"]


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
        "7. Las herramientas 'Lupa' y 'Esposas' se pueden usar para obtener ventajas.\n"
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
    global cargador, balas_reales, balas_falsas, herramientas_jugador_1, herramientas_jugador_2
    balas_reales = 2 if ronda == 1 else (3 if ronda == 2 else 4)
    balas_falsas = 6 - balas_reales
    cargador = [True] * balas_reales + [False] * balas_falsas
    random.shuffle(cargador)

    # Asignar herramienta aleatoria a cada jugador
    herramientas_jugador_1.append(random.choice(herramientas_disponibles))
    herramientas_jugador_2.append(random.choice(herramientas_disponibles))


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


def usar_herramienta(herramienta, ventana_juego):
    global jugador_actual, indice_bala

    if herramienta == "Lupa":
        bala_actual = cargador[indice_bala]
        mensaje = "La bala es real." if bala_actual else "La bala es falsa."
        messagebox.showinfo("Lupa", mensaje)

    elif herramienta == "Esposas":
        jugador_actual = 2 if jugador_actual == 1 else 1
        actualizar_turno()
        messagebox.showinfo("Esposas", "Has saltado el turno del otro jugador.")

    # Eliminar la herramienta usada solo si está en la lista
    if jugador_actual == 1 and herramienta in herramientas_jugador_1:
        herramientas_jugador_1.remove(herramienta)
    elif jugador_actual == 2 and herramienta in herramientas_jugador_2:
        herramientas_jugador_2.remove(herramienta)


# Función para mostrar las herramientas disponibles
def mostrar_herramientas(ventana_juego):
    herramientas = herramientas_jugador_1 if jugador_actual == 1 else herramientas_jugador_2
    herramientas_ventana = tk.Toplevel(ventana_juego)
    herramientas_ventana.title("Herramientas")
    herramientas_ventana.configure(bg="black")
    centrar_ventana(herramientas_ventana, 300, 200)

    if herramientas:
        for herramienta in herramientas:
            btn_herramienta = tk.Button(herramientas_ventana, text=f"Usar {herramienta}",
                                        command=lambda h=herramienta: usar_herramienta(h, ventana_juego),
                                        fg="red", bg="black", borderwidth=0)
            btn_herramienta.pack()
    else:
        label_no_herramientas = tk.Label(herramientas_ventana, text="No tienes herramientas disponibles.", fg="red",
                                         bg="black")
        label_no_herramientas.pack()


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
    global ronda_actual, vidas_jugador_1, vidas_jugador_2, jugador_actual, ganadas_jugador_1, ganadas_jugador_2
    if ganador == "Jugador 1":
        ganadas_jugador_1 += 1
    else:
        ganadas_jugador_2 += 1
    guardar_registros()
    ventana_juego.destroy()

    # Mostrar ventana de fin de ronda
    ronda_fin_ventana = tk.Toplevel()
    ronda_fin_ventana.title("Fin de la Ronda")
    centrar_ventana(ronda_fin_ventana, 300, 200)
    label_fin = tk.Label(ronda_fin_ventana, text=f"{ganador} ha ganado la ronda.", fg="red", bg="black")
    label_fin.pack()
    btn_ok = tk.Button(ronda_fin_ventana, text="Aceptar", command=lambda: iniciar_ronda(ronda_fin_ventana), fg="red",
                       bg="black", borderwidth=0)
    btn_ok.pack()


# Función para iniciar una nueva ronda
def iniciar_ronda(ventana_ronda_fin=None):
    global ronda_actual, vidas_jugador_1, vidas_jugador_2, jugador_actual, indice_bala, herramientas_jugador_1, herramientas_jugador_2
    if ventana_ronda_fin:
        ventana_ronda_fin.destroy()
    ronda_actual += 1
    vidas_jugador_1 = 3 if ronda_actual == 1 else (5 if ronda_actual == 2 else 8)
    vidas_jugador_2 = vidas_jugador_1
    jugador_actual = 1
    indice_bala = 0
    herramientas_jugador_1 = []
    herramientas_jugador_2 = []
    generar_cargador(ronda_actual)
    mostrar_balas(ronda_actual)
    iniciar_juego()


# Función para iniciar el juego
def iniciar_juego():
    ventana_juego = tk.Toplevel()
    ventana_juego.title("Ruleta Rusa")
    ventana_juego.configure(bg="black")
    centrar_ventana(ventana_juego)

    global label_vidas_jugador_1, label_vidas_jugador_2, label_turno

    label_vidas_jugador_1 = tk.Label(ventana_juego, text=f"Vidas Jugador 1: {vidas_jugador_1}", fg="red", bg="black")
    label_vidas_jugador_1.pack()

    label_vidas_jugador_2 = tk.Label(ventana_juego, text=f"Vidas Jugador 2: {vidas_jugador_2}", fg="red", bg="black")
    label_vidas_jugador_2.pack()

    label_turno = tk.Label(ventana_juego, text=f"Turno del Jugador {jugador_actual}", fg="red", bg="black")
    label_turno.pack()

    btn_disparar_self = tk.Button(ventana_juego, text="Dispararte", command=lambda: disparar("self", ventana_juego),
                                  fg="red", bg="black", borderwidth=0)
    btn_disparar_self.pack()

    btn_disparar_contrincante = tk.Button(ventana_juego, text="Disparar al contrincante",
                                          command=lambda: disparar("contrincante", ventana_juego), fg="red", bg="black",
                                          borderwidth=0)
    btn_disparar_contrincante.pack()

    btn_herramientas = tk.Button(ventana_juego, text="Ver herramientas",
                                 command=lambda: mostrar_herramientas(ventana_juego), fg="red", bg="black",
                                 borderwidth=0)
    btn_herramientas.pack()


# Función para iniciar el programa principal
def iniciar_programa():
    ventana_principal = tk.Tk()
    ventana_principal.title("Ruleta Rusa")
    ventana_principal.configure(bg="black")
    centrar_ventana(ventana_principal, 400, 400)

    btn_jugar = tk.Button(ventana_principal, text="Jugar", command=iniciar_juego, fg="red", bg="black", borderwidth=0)
    btn_jugar.pack(pady=20)

    btn_instrucciones = tk.Button(ventana_principal, text="Instrucciones", command=mostrar_instrucciones, fg="red",
                                  bg="black", borderwidth=0)
    btn_instrucciones.pack(pady=20)

    btn_salir = tk.Button(ventana_principal, text="Salir", command=ventana_principal.destroy, fg="red", bg="black",
                          borderwidth=0)
    btn_salir.pack(pady=20)

    cargar_registros()
    ventana_principal.mainloop()


iniciar_programa()
