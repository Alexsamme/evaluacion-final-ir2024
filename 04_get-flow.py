import requests
import json

api_url_flows = "http://192.168.101.254:58000/flow-analysis"
headers = {
    "X-Auth-Token": "NC-149-a8b4fe2cd6ea44e2845c-nbi",
    "Content-Type": "application/json"
}

try:
    # Realiza la solicitud GET a la API
    response = requests.get(api_url_flows, headers=headers, verify=False, timeout=60)
    
    # Verifica el código de estado de la respuesta
    print("Request status: ", response.status_code)
    
    if response.status_code == 200:
        # Si la solicitud fue exitosa, procesa el contenido JSON
        flow_data = response.json()  # Convierte la respuesta a formato JSON
        
        # Verifica si existe la clave 'response' y luego 'flowAnalysisList'
        if "response" in flow_data and "flowAnalysisList" in flow_data["response"]:
            flow_list = flow_data["response"]["flowAnalysisList"]
            
            # Itera sobre la lista de análisis de flujo y muestra detalles
            for flow in flow_list:
                print(f"Source IP: {flow.get('sourceIP')}")
                print(f"Destination IP: {flow.get('destIP')}")
                print(f"Status: {flow.get('status')}")
                print(f"Creation Time: {flow.get('createTime')}")
                print(f"Last Update Time: {flow.get('lastUpdateTime')}")
                print(f"Failure Reason (if any): {flow.get('failureReason', 'N/A')}")
                print("----")
        else:
            print("No se encontraron datos de análisis de flujo en la respuesta.")
    
    else:
        print("Error en la solicitud. Código de estado:", response.status_code)

except requests.exceptions.Timeout:
    print("Error: La solicitud ha tardado demasiado tiempo en completarse.")
except requests.exceptions.RequestException as e:
    print("Error en la solicitud:", e)
