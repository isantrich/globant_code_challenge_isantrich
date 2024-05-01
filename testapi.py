import requests
import os
import requests
import json

def main():
    url = "http://localhost:5000/loadtransactions" 
    folder_path = "data" 

    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)

                with open(file_path, "r") as file:
                    csv_data = file.read()
                    
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