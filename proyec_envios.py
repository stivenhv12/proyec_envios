import json
import os
import random


CLIENTES_FILE = 'clientes.json'
ENVIOS_FILE = 'envios.json'


def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


clientes = cargar_datos(CLIENTES_FILE)
envios = cargar_datos(ENVIOS_FILE)


def generar_numero_guia():
    while True:
        guia = str(random.randint(1000000000, 9999999999))
        if guia not in envios:
            return guia

# Registrar cliente
def registrar_cliente():
    print("\n--- Registro de Cliente ---")
    identificacion = input("Número de identificación: ")
    if identificacion in clientes:
        print("⚠️ Cliente ya registrado.")
        return
    tipo_id = input("Tipo de identificación (CC, TI, CE): ")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono fijo: ")
    celular = input("Número celular: ")
    barrio = input("Barrio de residencia: ")

    clientes[identificacion] = {
        "tipo_id": tipo_id,
        "nombres": nombres,
        "apellidos": apellidos,
        "direccion": direccion,
        "telefono": telefono,
        "celular": celular,
        "barrio": barrio
    }

    guardar_datos(CLIENTES_FILE, clientes)
    print("✅ Cliente registrado con éxito.")

# Registrar envío
def registrar_envio():
    print("\n--- Registro de Envío ---")
    remitente_id = input("Número de identificación del remitente: ")
    if remitente_id not in clientes:
        print("❌ El remitente no está registrado.")
        return

    fecha = input("Fecha del envío (YYYY-MM-DD): ")
    hora = input("Hora del envío (HH:MM): ")
    print("\n--- Información del Destinatario ---")
    nombre_dest = input("Nombre: ")
    direccion_dest = input("Dirección: ")
    telefono_dest = input("Teléfono: ")
    ciudad_dest = input("Ciudad: ")
    barrio_dest = input("Barrio: ")

    guia = generar_numero_guia()
    estado = "Recibido"

    envios[guia] = {
        "fecha": fecha,
        "hora": hora,
        "remitente_id": remitente_id,
        "destinatario": {
            "nombre": nombre_dest,
            "direccion": direccion_dest,
            "telefono": telefono_dest,
            "ciudad": ciudad_dest,
            "barrio": barrio_dest
        },
        "estado": estado
    }

    guardar_datos(ENVIOS_FILE, envios)
    print(f"✅ Envío registrado con éxito. Número de guía: {guia}")

# Seguimiento de paquete 
def seguimiento_paquete():
    print("\n--- Seguimiento de Paquete ---")
    guia = input("Ingrese el número de guía: ")
    if guia not in envios:
        print("❌ Número de guía no encontrado.")
        return

    envio = envios[guia]

    while True:
        print("\n--- Submenú de Seguimiento ---")
        print("1. Ver estado actual del envío")
        print("2. Ver detalles completos del envío")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print(f"\n📦 Estado actual: {envio['estado']}")
        elif opcion == "2":
            print("\n📄 Detalles del Envío:")
            print(f"Fecha: {envio['fecha']} | Hora: {envio['hora']}")
            print(f"Remitente ID: {envio['remitente_id']}")
            print("Destinatario:")
            print(f"  Nombre: {envio['destinatario']['nombre']}")
            print(f"  Dirección: {envio['destinatario']['direccion']}")
            print(f"  Teléfono: {envio['destinatario']['telefono']}")
            print(f"  Ciudad: {envio['destinatario']['ciudad']}")
            print(f"  Barrio: {envio['destinatario']['barrio']}")
            print(f"Estado actual: {envio['estado']}")
        elif opcion == "3":
            print("↩️ Volviendo al menú principal...")
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")

# Estados válidos
ESTADOS_VALIDOS = [
    "Recibido",
    "En Transito",
    "En Ciudad Destino",
    "En Bodega De La Transportadora",
    "En Reparto",
    "Entregado"
]

# Actualizar estado del paquete
def actualizar_estado_paquete():
    print("\n--- Actualización del Estado del Paquete ---")
    guia = input("Ingrese el número de guía del paquete: ")

    if guia not in envios:
        print("❌ Número de guía no encontrado.")
        return

    print("\nEstados posibles:")
    for i, estado in enumerate(ESTADOS_VALIDOS, 1):
        print(f"{i}. {estado}")

    opcion = input("Seleccione el nuevo estado (número): ")

    try:
        opcion = int(opcion)
        if 1 <= opcion <= len(ESTADOS_VALIDOS):
            nuevo_estado = ESTADOS_VALIDOS[opcion - 1]
            envios[guia]["estado"] = nuevo_estado
            guardar_datos(ENVIOS_FILE, envios)
            print(f"✅ Estado actualizado a: {nuevo_estado}")
        else:
            print("❌ Opción inválida.")
    except ValueError:
        print("❌ Entrada no válida. Debe ingresar un número.")

# Menú principal
def menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar Cliente")
        print("2. Registrar Envío")
        print("3. Seguimiento de Paquete")
        print("4. Actualizar estado del paquete")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            registrar_envio()
        elif opcion == "3":
            seguimiento_paquete()
        elif opcion == "4":
            actualizar_estado_paquete()
        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")

# Ejecutar
menu()

