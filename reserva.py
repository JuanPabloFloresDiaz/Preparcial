# Métodos para gestión de reservas de hotel - Versión del Parcial

# Función para validar el tipo de habitación
def validar_tipo_habitacion(tipo):
    tipo = tipo.lower().strip()
    return tipo in ["estándar", "suite"]

# Función para calcular el costo total con recargos y descuentos
def calcular_costo_completo(dias, tipo, huespedes, es_frecuente=False):
    # Precio base por tipo de habitación
    precio_base = 150 if tipo == "suite" else 100
    # Recargo por huéspedes adicionales
    recargo_huespedes = 20 if huespedes > 2 else 0
    # Costo por noche (base + recargo)
    costo_por_noche = precio_base + recargo_huespedes
    # Costo total base
    costo_total = dias * costo_por_noche
    # Aplicar descuentos
    descuento_total = 0.0
    # 10% de descuento si la estancia es mayor a 7 días
    if dias > 7:
        descuento_total += 0.10
    # 15% adicional si es huésped frecuente
    if es_frecuente:
        descuento_total += 0.15
    # Aplicar descuentos
    costo_final = costo_total * (1 - descuento_total)
    return costo_final, costo_total, descuento_total

# Función para calcular el costo de una reserva
def calcular_costo(dias, tipo, huespedes=1, es_frecuente=False):
    costo_final, _, _ = calcular_costo_completo(dias, tipo, huespedes, es_frecuente)
    return costo_final

# Función para agregar una nueva reserva
def agregar_reserva(reservas, Teclado):
    print("\n--- Agregar nueva reserva ---")
    nombre = Teclado.read_text("Nombre del huésped:", min_length=2)
    dias = Teclado.read_integer("Cantidad de días:", min_value=1)
    # Tipo de habitación
    while True:
        tipo = Teclado.read_text("Tipo de habitación (estándar/suite):").lower()
        if validar_tipo_habitacion(tipo):
            break
        print("Tipo de habitación inválido. Debe ser 'estándar' o 'suite'.")
    huespedes = Teclado.read_integer("Número de huéspedes:", min_value=1)
    # Preguntar si es huésped frecuente
    es_frecuente_input = Teclado.read_text("¿Es huésped frecuente? (si/no):").lower()
    es_frecuente = es_frecuente_input in ['si', 's', 'sí', 'yes', 'y']
    # Crear reserva con ID único
    reserva_id = len(reservas) + 1
    reserva = {
        "id": reserva_id,
        "nombre": nombre,
        "dias": dias,
        "tipo": tipo,
        "huespedes": huespedes,
        "es_frecuente": es_frecuente
    }
    reservas.append(reserva)
    # Mostrar resumen de la reserva
    costo_final, costo_base, descuento_total = calcular_costo_completo(dias, tipo, huespedes, es_frecuente)
    print(f"\n--- Resumen de Reserva ---")
    print(f"ID: {reserva_id}")
    print(f"Huésped: {nombre}")
    print(f"Días: {dias}")
    print(f"Tipo: {tipo}")
    print(f"Huéspedes: {huespedes}")
    print(f"Huésped frecuente: {'Sí' if es_frecuente else 'No'}")
    print(f"Costo base: ${costo_base:.2f}")
    if descuento_total > 0:
        descuento_monto = costo_base * descuento_total
        print(f"Descuento ({descuento_total*100:.0f}%): -${descuento_monto:.2f}")
    print(f"Costo total: ${costo_final:.2f}")
    print("Reserva agregada exitosamente.")

# Función para mostrar reservas con opciones de ordenamiento
def mostrar_reservas(reservas, tipo_filtro=None, ordenar_por=None):
    print("\nReservas activas:")
    if not reservas:
        print("No hay reservas para mostrar.")
        return
    # Filtrar por tipo si se especifica
    reservas_a_mostrar = reservas
    if tipo_filtro:
        reservas_a_mostrar = [r for r in reservas if r["tipo"] == tipo_filtro]
    # Si no hay reservar por mostrar
    if not reservas_a_mostrar:
        print("No hay reservas para mostrar con el filtro especificado.")
        return
    # Ordenar según el criterio especificado
    if ordenar_por == "nombre":
        reservas_a_mostrar = sorted(reservas_a_mostrar, key=lambda x: x["nombre"])
    elif ordenar_por == "costo":
        reservas_a_mostrar = sorted(reservas_a_mostrar, key=lambda x: calcular_costo(x["dias"], x["tipo"], x.get("huespedes", 1), x.get("es_frecuente", False)))
    # Mostrar reservas
    for r in reservas_a_mostrar:
        # Calcular costo de la reserva
        costo = calcular_costo(r["dias"], r["tipo"], r.get("huespedes", 1), r.get("es_frecuente", False))
        print(f"--- Reserva ID: {r.get('id', 'N/A')} ---")
        print(f"Huésped: {r['nombre']}")
        print(f"Días: {r['dias']}")
        print(f"Tipo: {r['tipo']}")
        print(f"Huéspedes: {r.get('huespedes', 1)}")
        print(f"Huésped frecuente: {'Sí' if r.get('es_frecuente', False) else 'No'}")
        print(f"Costo total: ${costo:.2f}")
        print("")

# Función para mostrar reservas con menú de ordenamiento
def mostrar_reservas_con_menu(reservas, Teclado, tipo_filtro=None):
    if not reservas:
        print("No hay reservas para mostrar.")
        return
    # Preguntar cómo desea ordenar las reservas
    print("\n¿Cómo desea ordenar las reservas?")
    print("1. Sin ordenar")
    print("2. Por nombre del huésped (A-Z)")
    print("3. Por costo total (menor a mayor)")
    # Seleccionar la opción
    opcion = Teclado.read_integer("Seleccione una opción (1-3):", min_value=1, max_value=3)
    # Determinar el criterio de ordenamiento
    ordenar_por = None
    if opcion == 2:
        ordenar_por = "nombre"
    elif opcion == 3:
        ordenar_por = "costo"
    
    mostrar_reservas(reservas, tipo_filtro, ordenar_por)

# Función para buscar reservas
def buscar_reserva(reservas, nombre_busqueda):
    nombre_busqueda = nombre_busqueda.lower()
    resultados = [r for r in reservas if nombre_busqueda in r["nombre"].lower()]
    return resultados

# Función para búsqueda flexible
def buscar_reserva_flexible(reservas, Teclado):
    # Por si no hay reservas para buscar
    if not reservas:
        print("No hay reservas para buscar.")
        return
    # Mostrar opciones de búsqueda
    print("\n--- Búsqueda Flexible ---")
    print("1. Buscar por nombre parcial")
    print("2. Buscar por rango de días")
    # Seleccionar la opción
    opcion = Teclado.read_integer("Seleccione tipo de búsqueda (1-2):", min_value=1, max_value=2)
    # Arreglo de resultados
    resultados = []
    # Imprimir los resultados según la opción seleccionada
    if opcion == 1:
        nombre = Teclado.read_text("Nombre o parte del nombre:")
        resultados = buscar_reserva(reservas, nombre)
    
    elif opcion == 2:
        dias_min = Teclado.read_integer("Días mínimos:", min_value=1)
        dias_max = Teclado.read_integer("Días máximos:", min_value=dias_min)
        resultados = [r for r in reservas if dias_min <= r['dias'] <= dias_max]
        print(f"Buscando reservas entre {dias_min} y {dias_max} días...")
    # Mostrar la cantidad de resultados encontrados
    if resultados:
        print(f"\n--- Se encontraron {len(resultados)} resultado(s) ---")
        for r in resultados:
            costo = calcular_costo(r["dias"], r["tipo"], r.get("huespedes", 1), r.get("es_frecuente", False))
            print(f"ID: {r.get('id', 'N/A')} - {r['nombre']}: {r['dias']} días en {r['tipo']} (${costo:.2f})")
    else:
        print("No se encontraron reservas con los criterios especificados.")

# Función para cancelar reservas con lista numerada si hay múltiples coincidencias
def cancelar_reserva(reservas, Teclado):
    if not reservas:
        print("No hay reservas para cancelar.")
        return False
    # Solicitar el nombre del huésped a cancelar
    nombre = Teclado.read_text("Nombre del huésped a cancelar:")
    
    # Buscar todas las reservas que coincidan
    coincidencias = []
    for i, r in enumerate(reservas):
        if nombre.lower() in r["nombre"].lower():
            coincidencias.append((i, r))
    # Si no hay coincidencias
    if not coincidencias:
        print("No se encontró una reserva con ese nombre.")
        return False
    
    # Si hay una sola coincidencia, cancelar directamente
    if len(coincidencias) == 1:
        indice, reserva = coincidencias[0]
        print(f"Reserva de {reserva['nombre']} cancelada.")
        reservas.pop(indice)
        return True
    
    # Si hay múltiples coincidencias, mostrar lista numerada
    print(f"\nSe encontraron {len(coincidencias)} reservas con ese nombre:")
    for i, (_, reserva) in enumerate(coincidencias, 1):
        costo = calcular_costo(reserva["dias"], reserva["tipo"], reserva.get("huespedes", 1), reserva.get("es_frecuente", False))
        print(f"{i}. {reserva['nombre']} - {reserva['dias']} días en {reserva['tipo']} (${costo:.2f})")
    
    # Permitir al usuario elegir cuál cancelar
    opcion = Teclado.read_integer("Seleccione el número de la reserva a cancelar:", min_value=1, max_value=len(coincidencias))
    
    # Cancelar la reserva seleccionada
    indice_real, reserva_seleccionada = coincidencias[opcion - 1]
    print(f"Reserva de {reserva_seleccionada['nombre']} cancelada.")
    reservas.pop(indice_real)
    return True

# Función para generar reporte de ocupación
def reporte_ocupacion(reservas):
    if not reservas:
        print("No hay reservas para generar reporte.")
        return
    
    print("\n--- Reporte de Ocupación ---")
    
    # Total de reservas activas
    total_reservas = len(reservas)
    
    # Contar por tipo de habitación
    reservas_estandar = sum(1 for r in reservas if r['tipo'] == 'estándar')
    reservas_suite = sum(1 for r in reservas if r['tipo'] == 'suite')
    
    # Calcular porcentajes
    porcentaje_estandar = (reservas_estandar / total_reservas) * 100 if total_reservas > 0 else 0
    porcentaje_suite = (reservas_suite / total_reservas) * 100 if total_reservas > 0 else 0
    
    # Calcular ingresos totales actuales
    ingresos_total = 0
    for r in reservas:
        costo = calcular_costo(r['dias'], r['tipo'], r.get('huespedes', 1), r.get('es_frecuente', False))
        ingresos_total += costo
    # Imprimir el reporte
    print(f"Total de reservas activas: {total_reservas}")
    print(f"\nDistribución por tipo de habitación:")
    print(f"Habitaciones estándar: {reservas_estandar} ({porcentaje_estandar:.1f}%)")
    print(f"Habitaciones suite: {reservas_suite} ({porcentaje_suite:.1f}%)")
    print(f"\nIngresos totales actuales: ${ingresos_total:.2f}")
    
    # Información adicional útil
    if total_reservas > 0:
        dias_promedio = sum(r['dias'] for r in reservas) / total_reservas
        huespedes_promedio = sum(r.get('huespedes', 1) for r in reservas) / total_reservas
        huespedes_frecuentes = sum(1 for r in reservas if r.get('es_frecuente', False))
        
        print(f"\nInformación adicional:")
        print(f"Estadía promedio: {dias_promedio:.1f} días")
        print(f"Huéspedes promedio por reserva: {huespedes_promedio:.1f}")
        print(f"Huéspedes frecuentes: {huespedes_frecuentes} ({(huespedes_frecuentes/total_reservas)*100:.1f}%)")
