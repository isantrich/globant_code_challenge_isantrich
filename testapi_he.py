import requests
import os
import requests
import json
import pandas as pd

def main():
    url = "http://localhost:5000/loadtransactions" 
    folder_path = "data" 

    try:
        for filename in os.listdir(folder_path):
            if filename.endswith("hired_employees.csv"):
                file_path = os.path.join(folder_path, filename)

                # Leer el archivo CSV en un DataFrame de pandas
                df = pd.read_csv(file_path)

                # Dividir el DataFrame en fragmentos de 1000 filas o menos
                chunks = [df[i:i+1000] for i in range(0, df.shape[0], 1000)]

                for i, chunk in enumerate(chunks):
                    # Convertir cada fragmento en una cadena CSV
                    csv_data = chunk.to_csv(index=False)
                    
                    filename_without_extension = os.path.splitext(filename)[0]
                    datos = {"fileName": filename_without_extension, "fileData": csv_data}
                    print("este es el archivo de test")
                    print(filename_without_extension)
                    response = requests.post(url, data=json.dumps(datos), headers = {"Content-Type": "application/json"})
                    #response.raise_for_status() 

                    print(response.text)

    except requests.exceptions.RequestException as e:
        print("Error making the request:", e)

if __name__ == "__main__":
    main()