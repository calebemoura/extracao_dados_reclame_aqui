from datetime import datetime
from pandas import DataFrame
from io import StringIO
import requests

def upload_to_databricks(
        data: dict, 
        token: str, 
        volume_path: str, 
        file_name: str,
        host: str
    ) -> None:
    
    df = DataFrame(data)

    output = StringIO()
    df.to_csv(output, sep=';', index=False)
    csv_data = output.getvalue()

    token_databriks = token
    volume = volume_path
    name = file_name
    host_databriks = host
    api_url = f"{host_databriks}/api/2.0/fs/files{volume}/{name}"
    
    headers = {
        'Authorization': f'Bearer {token_databriks}',
        'Content-Type': 'text/plain'
    }

    response = requests.put(
            url=api_url,
            headers=headers,
            data=csv_data.encode('utf-8'),
            timeout=60
        )

    if response.status_code == 204:
        print("\nSucesso! Upload concluído no volume do databricks.")
        print(f"Status Code: {response.status_code}")
    else:
        print("\nErro! Upload não foi concluído no volume do databricks.")
        print(f"Status Code: {response.status_code}")