import math
import tkinter as tk
from tkinter import messagebox


class SimuladorAntenasApp:

  def __init__(self, ventana_principal):
    self.ventana_principal = ventana_principal
    self.ventana_principal.title(
        "Simulador Avanzado de Radioenlaces y Nivel - @JCabello"
    )
    self.ventana_principal.geometry("520x820")
    self.ventana_principal.config(bg="#121212")

    self.rumbo_objetivo = 0.0
    self.elevacion_objetivo = 0.0

    # --- TÍTULO PRINCIPAL ---
    etiqueta_titulo = tk.Label(
        ventana_principal,
        text="RADIOENLACES - AZIMUT Y NIVEL DE ELEVACIÓN",
        font=("Consolas", 10, "bold"),
        bg="#121212",
        fg="#00ffcc",
    )
    etiqueta_titulo.pack(pady=4)

    # --- SECCIÓN ORIGEN ---
    marco_origen = tk.LabelFrame(
        ventana_principal,
        text=" Punto de Origen (Torre / Antena) ",
        font=("Consolas", 8, "bold"),
        bg="#1e1e1e",
        fg="#00ffcc",
        bd=2,
        relief="groove",
    )
    marco_origen.pack(fill="x", padx=15, pady=2)

    self.entrada_latitud_origen = self.crear_campo_pack(
        marco_origen, "Latitud Origen:"
    )
    self.entrada_longitud_origen = self.crear_campo_pack(
        marco_origen, "Longitud Origen:"
    )
    self.entrada_altitud_origen = self.crear_campo_pack(
        marco_origen, "Altitud Terreno Origen (m):"
    )
    # Nuevo campo para la altura de la antena en la torre
    self.entrada_altura_torre_origen = self.crear_campo_pack(
        marco_origen, "Altura Antena en Torre / Suelo (m) [Ej: 12]:"
    )
    self.entrada_altura_torre_origen.insert(0, "12.0")  # Valor por defecto típico

    # --- SECCIÓN DESTINO ---
    marco_destino = tk.LabelFrame(
        ventana_principal,
        text=" Punto de Destino (Receptor) ",
        font=("Consolas", 8, "bold"),
        bg="#1e1e1e",
        fg="#00ffcc",
        bd=2,
        relief="groove",
    )
    marco_destino.pack(fill="x", padx=15, pady=2)

    self.entrada_latitud_destino = self.crear_campo_pack(
        marco_destino, "Latitud Destino:"
    )
    self.entrada_longitud_destino = self.crear_campo_pack(
        marco_destino, "Longitud Destino:"
    )
    self.entrada_altitud_destino = self.crear_campo_pack(
        marco_destino, "Altitud Terreno Destino (m):"
    )
    # Nuevo campo para la altura de la antena receptor
    self.entrada_altura_torre_destino = self.crear_campo_pack(
        marco_destino, "Altura Antena en Torre / Suelo (m) [Ej: 12]:"
    )
    self.entrada_altura_torre_destino.insert(0, "12.0")  # Valor por defecto típico

    # --- BOTÓN CALCULAR ---
    boton_calcular = tk.Button(
        ventana_principal,
        text="CALCULAR ENLACE, RUMBO Y ELEVACIÓN",
        command=self.calcular_enlace,
        bg="#00ffcc",
        fg="#000000",
        font=("Consolas", 9, "bold"),
        relief="flat",
        cursor="hand2",
    )
    boton_calcular.pack(fill="x", padx=15, pady=6)

    # --- ETIQUETA DE RESULTADOS ---
    self.etiqueta_resultado = tk.Label(
        ventana_principal,
        text="Distancia: -- | Rumbo: -- | Elevación: --",
        font=("Consolas", 8, "bold"),
        bg="#1e1e1e",
        fg="#ffffff",
        padx=5,
        pady=4,
        relief="solid",
        bd=1,
    )
    self.etiqueta_resultado.pack(fill="x", padx=15, pady=2)

    # --- SIMULADOR DE GIRO (AZIMUT) ---
    etiqueta_sim_giro = tk.Label(
        ventana_principal,
        text="Simulador Brújula / Azimuth (Horizontal):",
        font=("Consolas", 7),
        bg="#121212",
        fg="#aaaaaa",
    )
    etiqueta_sim_giro.pack(anchor="w", padx=15, pady=(2, 0))

    self.barra_giro = tk.Scale(
        ventana_principal,
        from_=0,
        to=360,
        orient="horizontal",
        command=self.actualizar_simulacion_general,
        bg="#1e1e1e",
        fg="#00ffcc",
        highlightbackground="#121212",
        troughcolor="#2d2d2d",
        font=("Consolas", 7),
        length=480,
    )
    self.barra_giro.pack(padx=15)

    self.etiqueta_brujula_simulada = tk.Label(
        ventana_principal,
        text="Horizontal: 0°",
        font=("Consolas", 8, "bold"),
        bg="#121212",
        fg="#ff3355",
    )
    self.etiqueta_brujula_simulada.pack(pady=1)

    # --- SIMULADOR DE NIVEL (ELEVACIÓN) ---
    etiqueta_sim_nivel = tk.Label(
        ventana_principal,
        text="Simulador Inclinómetro / Nivel (Vertical de -45° a +45°):",
        font=("Consolas", 7),
        bg="#121212",
        fg="#aaaaaa",
    )
    etiqueta_sim_nivel.pack(anchor="w", padx=15, pady=(2, 0))

    self.barra_nivel = tk.Scale(
        ventana_principal,
        from_=-45,
        to=45,
        resolution=0.5,
        orient="horizontal",
        command=self.actualizar_simulacion_general,
        bg="#1e1e1e",
        fg="#00ffcc",
        highlightbackground="#121212",
        troughcolor="#2d2d2d",
        font=("Consolas", 7),
        length=480,
    )
    self.barra_nivel.pack(padx=15)

    self.etiqueta_nivel_simulado = tk.Label(
        ventana_principal,
        text="Vertical: 0.0°",
        font=("Consolas", 8, "bold"),
        bg="#121212",
        fg="#ff3355",
    )
    self.etiqueta_nivel_simulado.pack(pady=1)

  def crear_campo_pack(self, contenedor, texto):
    tk.Label(
        contenedor,
        text=texto,
        font=("Consolas", 7),
        bg="#1e1e1e",
        fg="#cccccc",
    ).pack(anchor="w", padx=8, pady=0)
    entrada = tk.Entry(
        contenedor,
        font=("Consolas", 8),
        bg="#2d2d2d",
        fg="#ffffff",
        insertbackground="white",
        relief="solid",
        bd=1,
    )
    entrada.pack(fill="x", padx=8, pady=1)
    return entrada

  def calcular_enlace(self):
    try:
      lat1 = float(self.entrada_latitud_origen.get().replace(",", "."))
      lon1 = float(self.entrada_longitud_origen.get().replace(",", "."))
      alt_terreno_1 = float(
          self.entrada_altitud_origen.get().replace(",", ".")
      )
      altura_torre_1 = float(
          self.entrada_altura_torre_origen.get().replace(",", ".")
      )
      alt1 = alt_terreno_1 + altura_torre_1  # Altura total real de la antena

      lat2 = float(self.entrada_latitud_destino.get().replace(",", "."))
      lon2 = float(self.entrada_longitud_destino.get().replace(",", "."))
      alt_terreno_2 = float(
          self.entrada_altitud_destino.get().replace(",", ".")
      )
      altura_torre_2 = float(
          self.entrada_altura_torre_destino.get().replace(",", ".")
      )
      alt2 = alt_terreno_2 + altura_torre_2  # Altura total real de la antena

      lat_rad_1 = math.radians(lat1)
      lon_rad_1 = math.radians(lon1)
      lat_rad_2 = math.radians(lat2)
      lon_rad_2 = math.radians(lon2)

      diferencia_lon = lon_rad_2 - lon_rad_1
      diferencia_lat = lat_rad_2 - lat_rad_1

      radio_tierra_km = 6371.0
      a = (
          math.sin(diferencia_lat / 2) ** 2
          + math.cos(lat_rad_1)
          * math.cos(lat_rad_2)
          * math.sin(diferencia_lon / 2) ** 2
      )
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
      distancia_km = radio_tierra_km * c

      x = math.cos(lat_rad_2) * math.sin(diferencia_lon)
      y = (math.cos(lat_rad_1) * math.sin(lat_rad_2)) - (
          math.sin(lat_rad_1)
          * math.cos(lat_rad_2)
          * math.cos(diferencia_lon)
      )
      self.rumbo_objetivo = (math.degrees(math.atan2(x, y)) + 360) % 360

      diferencia_altitud_metros = alt2 - alt1
      distancia_metros = distancia_km * 1000.0
      if distancia_metros > 0:
        self.elevacion_objetivo = math.degrees(
            math.atan(diferencia_altitud_metros / distancia_metros)
        )
      else:
        self.elevacion_objetivo = 0.0

      self.etiqueta_resultado.config(
          text=(
              f"Dist: {distancia_km:.2f} km | Rumbo: {self.rumbo_objetivo:.1f}°"
              f" | Elev: {self.elevacion_objetivo:+.1f}°"
          )
      )
      self.actualizar_simulacion_general(None)

    except ValueError:
      messagebox.showerror(
          "Faltan Datos o Error",
          "Por favor, introduce valores numéricos válidos en todas las"
          " casillas.",
      )

  def actualizar_simulacion_general(self, event):
    orientacion_actual = int(float(self.barra_giro.get()))
    diferencia_rumbo = (self.rumbo_objetivo - orientacion_actual + 360) % 360
    if diferencia_rumbo > 180:
      diferencia_rumbo -= 360

    guia_giro = ""
    if abs(diferencia_rumbo) < 3:
      guia_giro = " [OK]"
    elif diferencia_rumbo > 0:
      guia_giro = " (Gira -> DERECHA)"
    else:
      guia_giro = " (Gira <- IZQUIERDA)"

    self.etiqueta_brujula_simulada.config(
        text=(
            f"Horizontal: {orientacion_actual}° (Obj:"
            f" {self.rumbo_objetivo:.1f}°){guia_giro}"
        )
    )

    inclinacion_actual = float(self.barra_nivel.get())
    diferencia_elevacion = self.elevacion_objetivo - inclinacion_actual

    guia_nivel = ""
    if abs(diferencia_elevacion) < 0.5:
      guia_nivel = " [¡NIVELADO!]"
    elif diferencia_elevacion > 0:
      guia_nivel = " (Eleva antena ⬆)"
    else:
      guia_nivel = " (Baja antena ⬇)"

    self.etiqueta_nivel_simulado.config(
        text=(
            f"Vertical: {inclinacion_actual:+.1f}° (Obj:"
            f" {self.elevacion_objetivo:+.1f}°){guia_nivel}"
        )
    )


if __name__ == "__main__":
  ventana_raiz = tk.Tk()
  app = SimuladorAntenasApp(ventana_raiz)
  ventana_raiz.mainloop()