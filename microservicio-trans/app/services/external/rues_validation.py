#services/external/rues_validation.py
import http.client
import json
from fastapi import HTTPException

def get_rues_status(nit: str) -> bool: 
    #Se llama API de RUES para validar estado de matrícula mercantil
    try:
            conn = http.client.HTTPSConnection("www.datos.gov.co")
            payload = ''
            headers = {}
            conn.request("GET", "/resource/c82u-588k.json?nit=" + nit, payload, headers)
            res = conn.getresponse()
            data = res.read()
            json_data = json.loads(data.decode("utf-8"))
            
            bool_active= False
            for item in json_data:
                if item["estado_matricula"] == "ACTIVA":
                    bool_active = True
                    break
            
            return bool_active

    except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))