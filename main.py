# Sistema de Reservas de Hotel
# Utiliza Teclado y Validaciones para entrada segura

from Teclado import Teclado
import reserva


# Función para mostrar el menú
def menu():
	print("\n--- Menú Sistema de Reservas ---")
	print("1. Agregar nueva reserva")
	print("2. Mostrar todas las reservas")
	print("3. Mostrar solo reservas de un tipo")
	print("4. Buscar reservas por nombre")
	print("5. Búsqueda flexible")
	print("6. Cancelar reserva")
	print("7. Reporte de ocupación")
	print("8. Salir")
# Función principal
def main():
	# Arreglo para almacenar reservas
	reservas = []
	
	while True:
		# Llamar la función de menú
		menu()
		# Seleccionar la opción
		opcion = Teclado.read_integer("Seleccione una opción (1-8):", min_value=1, max_value=8)
		
		if opcion == 1:
			# Función para agregar reserva.
			reserva.agregar_reserva(reservas, Teclado)
		
		elif opcion == 2:
			# Función para mostrar todas las reservas con opción de ordenamiento
			reserva.mostrar_reservas_con_menu(reservas, Teclado)
		
		elif opcion == 3:
			# Seleccionar el tipo de habitación
			tipo = Teclado.read_text("Tipo de habitación a mostrar (estándar/suite):").lower()
			if not reserva.validar_tipo_habitacion(tipo):
				print("Tipo de habitación inválido.")
			else:
				# Mostrar reservas de un tipo específico con opciones de ordenamiento
				reserva.mostrar_reservas_con_menu(reservas, Teclado, tipo_filtro=tipo)
		
		elif opcion == 4:
			# Búsqueda por nombre parcial
			nombre = Teclado.read_text("Nombre o parte del nombre a buscar:")
			resultados = reserva.buscar_reserva(reservas, nombre)
			if resultados:
				print("\nResultados de búsqueda:")
				for r in resultados:
					costo = reserva.calcular_costo(r["dias"], r["tipo"], r.get("huespedes", 1), r.get("es_frecuente", False))
					print(f"- {r['nombre']}: {r['dias']} días en {r['tipo']} (${costo:.2f})")
			else:
				print("No se encontraron reservas con ese nombre.")
		
		elif opcion == 5:
			# Búsqueda flexible (por nombre parcial o rango de días)
			reserva.buscar_reserva_flexible(reservas, Teclado)
		
		elif opcion == 6:
			# Cancelar reserva con manejo de múltiples coincidencias
			reserva.cancelar_reserva(reservas, Teclado)
		
		elif opcion == 7:
			# Reporte de ocupación
			reserva.reporte_ocupacion(reservas)
		
		elif opcion == 8:
			print("¡Hasta luego!")
			break

if __name__ == "__main__":
	main()
