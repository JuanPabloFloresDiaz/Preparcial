# Sistema de Reservas de Hotel
# Utiliza Teclado y Validaciones para entrada segura

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from Teclado import Teclado
import reserva


# Función para mostrar el menú
def menu():
	print("\n--- Menú Sistema de Reservas ---")
	print("1. Agregar nueva reserva")
	print("2. Mostrar todas las reservas")
	print("3. Mostrar solo reservas de un tipo")
	print("4. Buscar reservas por nombre")
	print("5. Cancelar reserva")
	print("6. Salir")
# Función principal
def main():
	# Arreglo para almacenar reservas
	reservas = []
	while True:
		# Llamar la función de menú
		menu()
		# Seleccionar la opción
		opcion = Teclado.read_integer("Seleccione una opción (1-6):", min_value=1, max_value=6)
		if opcion == 1:
			# Función para agregar reserva.
			reserva.agregar_reserva(reservas, Teclado)
		elif opcion == 2:
			# Función para mostrar la reserva.
			reserva.mostrar_reservas(reservas)
		elif opcion == 3:
			# Seleccionar el tipo de habitación
			tipo = Teclado.read_text("Tipo de habitación a mostrar (estándar/suite):").lower()
			# Función para mostrar reservas de un tipo específico.
			if not reserva.validar_tipo_habitacion(tipo):
				print("Tipo de habitación inválido.")
			else:
				# Función para mostrar reservas de un tipo específico.
				reserva.mostrar_reservas(reservas, tipo_filtro=tipo)
		elif opcion == 4:
			# Escribir el nombre o parte del nombre a buscar
			nombre = Teclado.read_text("Nombre o parte del nombre a buscar:")
			# Función para buscar reservas
			resultados = reserva.buscar_reserva(reservas, nombre)
			if resultados:
				print("\nResultados de búsqueda:")
				for r in resultados:
					# Función para calcular el costo de la reserva
					costo = reserva.calcular_costo(r["dias"], r["tipo"])
					print(f"- {r['nombre']}: {r['dias']} días en {r['tipo']} (${costo})")
			else:
				print("No se encontraron reservas con ese nombre.")
		elif opcion == 5:
			# Escribir el nombre o parte del nombre a cancelar
			nombre = Teclado.read_text("Nombre o parte del nombre a cancelar:")
			# Función para cancelar reservas
			reserva.cancelar_reserva(reservas, nombre)
		elif opcion == 6:
			print("¡Hasta luego!")
			break

if __name__ == "__main__":
	main()
