import requests
import json
import time

# Definir las variables del Bot
access_token = 'ODRjMjc4M2QtMWVhMy00N2RhLTg3YzAtYWFjMjJkMTMyYTA4ZDZlYzU4NTktMzc2_PE93_27f882c3-50be-433d-96e5-4dceb2514eab'
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vNTBmNGMxMzAtNWY3My0xMWVmLWJhMTEtZDc5MGJkY2Q1Nzhh'

# Autenticación para la API del SDN
api_url_devices = "http://localhost:58000/api/v1/network-device"
api_url_hosts = "http://localhost:58000/api/v1/host"
api_url_flows = "http://localhost:58000/api/v1/flow"  # URL para crear un Flow

headers_sdn = {
    "content-type": "application/json",
    "X-Auth-Token": "NC-149-a8b4fe2cd6ea44e2845c-nbi"  # Tu ticket aquí
}

# Función para obtener información de un dispositivo de red por hostname
def obtener_dispositivo(hostname):
    response = requests.get(api_url_devices, headers=headers_sdn, verify=False)
    if response.status_code == 200:
        dispositivos = response.json()["response"]
        for d in dispositivos:
            if d['hostname'].lower() == hostname.lower():
                return f"{d['hostname']}\t{d['platformId']}\t{d['managementIpAddress']}"
        return f"No se encontró el dispositivo con el hostname **{hostname}**."
    else:
        return "Error al obtener los dispositivos de red."

# Función para obtener información de un host por nombre
def obtener_host(hostname):
    response = requests.get(api_url_hosts, headers=headers_sdn, verify=False)
    if response.status_code == 200:
        hosts = response.json()["response"]
        for h in hosts:
            if h['hostName'].lower() == hostname.lower():
                return f"{h['hostName']}\t{h['hostIp']}\t{h['hostMac']}\t{h['connectedInterfaceName']}"
        return f"No se encontró el host con el nombre **{hostname}**."
    else:
        return "Error al obtener los hosts."

# Función para crear un Flow y obtener el ID
def crear_flow(source_ip, dest_ip):
    flow_data = {
        "sourceIp": source_ip,
        "destIp": dest_ip
    }
    response = requests.post(api_url_flows, headers=headers_sdn, json=flow_data, verify=False)
    if response.status_code == 200:
        flow_info = response.json()
        flow_id = flow_info.get("flowId", "ID de Flow no disponible")
        return f"Flow creado con ID: {flow_id} 😄"
    else:
        return "Error al crear el Flow."

# Variable para almacenar el último mensaje procesado
last_message_id = None
error_message_sent = False
valid_command_received = False

while True:
    # Introducir un retardo
    time.sleep(1)

    # Obtener mensajes de la sala
    url = "https://webexapis.com/v1/messages"
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    params = {'roomId': room_id, 'max': 1}  # Último mensaje
    res = requests.get(url, params=params, headers=headers)

    if not res.status_code == 200:
        raise Exception("Respuesta incorrecta de Webex API. Código de estado: {}. Texto: {}".format(res.status_code, res.text))
    
    # Obtener los mensajes
    mensajes = res.json()["items"]
    
    # Verificar si hay mensajes
    if len(mensajes) == 0:
        continue  # Si no hay mensajes, continuar con el siguiente ciclo
    
    # Almacenar el primer mensaje
    mensaje = mensajes[0]
    mensaje_texto = mensaje["text"].strip().lower()  # Convertir a minúsculas y eliminar espacios en blanco
    mensaje_id = mensaje["id"]

    # Evitar procesar el mismo mensaje más de una vez
    if mensaje_id == last_message_id:
        continue
    
    # Actualizar el último mensaje procesado
    last_message_id = mensaje_id

    print("Mensaje recibido: " + mensaje_texto)

    # Mostrar el menú de opciones
    if mensaje_texto == "menú":
        menu = """
        **Menú de Opciones:**
        1. Obtener información de un dispositivo de red: #hostname
        2. Obtener información de un Host: @hostname
        3. Crear un Flow o Path Trace: !destIP,sourceIP

        **Examen final**
        Grupo Mamani

        Participantes:
        - Alex Mamani
        - Mila Colquichagua
        - Joel Cubas
        - Patricia Vega
        """
        params = {'roomId': room_id, 'markdown': menu}
        res = requests.post(url, headers=headers, json=params)
        error_message_sent = False  # No se debe enviar mensaje de error después de mostrar menú
        valid_command_received = True  # Se considera que se recibió un comando válido al mostrar el menú
        continue

    # Opción 1: Obtener información de un dispositivo de red
    if mensaje_texto.startswith("#"):
        hostname = mensaje_texto[1:].strip()  # Extraer el hostname después de "#"
        dispositivo_info = obtener_dispositivo(hostname)
        
        response_message = f"Información del dispositivo **{hostname}**:\n{dispositivo_info} 😄"
        params = {'roomId': room_id, 'markdown': response_message}
        res = requests.post(url, headers=headers, json=params)
        valid_command_received = True
        error_message_sent = False
        continue

    # Opción 2: Obtener información de un Host
    if mensaje_texto.startswith("@"):
        hostname = mensaje_texto[1:].strip()  # Extraer el hostname después de "@"
        host_info = obtener_host(hostname)
        
        response_message = f"Información del host **{hostname}**:\n{host_info} 😄"
        params = {'roomId': room_id, 'markdown': response_message}
        res = requests.post(url, headers=headers, json=params)
        valid_command_received = True
        error_message_sent = False
        continue

    # Opción 3: Crear un Flow o Path Trace
    if mensaje_texto.startswith("!"):
        ips = mensaje_texto[1:].split(",")  # Extraer las IPs después de "!"
        if len(ips) == 2:
            source_ip, dest_ip = ips
            # Crear el Flow y obtener el ID
            flow_info = crear_flow(source_ip, dest_ip)
            response_message = f"Path Trace entre **{source_ip}** y **{dest_ip}**:\n{flow_info}"
            params = {'roomId': room_id, 'markdown': response_message}
            res = requests.post(url, headers=headers, json=params)
        else:
            response_message = "Formato de IPs incorrecto. Usa: !destIP,sourceIP."
            params = {'roomId': room_id, 'markdown': response_message}
            res = requests.post(url, headers=headers, json=params)
        valid_command_received = True
        error_message_sent = False
        continue

    # En caso de mensaje no válido
    if not valid_command_received:
        if not error_message_sent:
            response_message = "Opción no válida. Por favor selecciona una de las 3 opciones: 'menú', '#hostname', '@hostname', o '!destIP,sourceIP'."
            params = {'roomId': room_id, 'markdown': response_message}
            res = requests.post(url, headers=headers, json=params)
            error_message_sent = True  # Marcar que el mensaje de error ya se envió
