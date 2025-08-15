# reserva.py
# Métodos para gestión de reservas de hotel

# Función para validar el tipo de habitación
def validar_tipo_habitacion(tipo):
    tipo = tipo.lower().strip()
    return tipo in ["estándar", "suite"]

# Función para agregar una nueva reserva
def agregar_reserva(reservas, Teclado):
    print("\n--- Agregar nueva reserva ---")
    nombre = Teclado.read_text("Nombre del huésped:", min_length=2)
    dias = Teclado.read_integer("Cantidad de días:", min_value=1)
    while True:
        tipo = Teclado.read_text("Tipo de habitación (estándar/suite):").lower()
        if validar_tipo_habitacion(tipo):
            break
        print("Tipo de habitación inválido. Debe ser 'estándar' o 'suite'.")
    reserva = {"nombre": nombre, "dias": dias, "tipo": tipo}
    reservas.append(reserva)
    print(f"Reserva de {nombre} agregada.")

# Función para calcular el costo de una reserva
def calcular_costo(dias, tipo):
    precio = 150 if tipo == "suite" else 100
    return dias * precio

# Función para mostrar reservas
def mostrar_reservas(reservas, tipo_filtro=None):
    print("\nReservas activas:")
    hay = False
    for r in reservas:
        if tipo_filtro and r["tipo"] != tipo_filtro:
            continue
        costo = calcular_costo(r["dias"], r["tipo"])
        print(f"- {r['nombre']}: {r['dias']} días en {r['tipo']} (${costo})")
        hay = True
    if not hay:
        print("No hay reservas para mostrar.")

# Función para buscar reservas
def buscar_reserva(reservas, nombre_busqueda):
    nombre_busqueda = nombre_busqueda.lower()
    resultados = [r for r in reservas if nombre_busqueda in r["nombre"].lower()]
    return resultados

# Función para cancelar reservas
def cancelar_reserva(reservas, nombre):
    nombre = nombre.lower()
    for i, r in enumerate(reservas):
        if nombre in r["nombre"].lower():
            print(f"Reserva de {r['nombre']} cancelada.")
            reservas.pop(i)
            return True
    print("No se encontró una reserva con ese nombre.")
    return False
