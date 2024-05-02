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
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)

                # Read the CSV file
                df = pd.read_csv(file_path, header=None)
                print(f"File {filename}:", len(df), "rows")

                # Divide the DataFrame into chunks of 1000 rows
                chunks = [df[i:i+1000] for i in range(0, len(df), 1000)]
                print("Total fragments:", len(chunks))

                # Iterate over each chunk
                for i, chunk in enumerate(chunks):
                    start_row = i * 1000 + 1
                    end_row = min((i + 1) * 1000, len(df))

                    print(f"Fragment {i+1}: {len(chunk)} rows")
                    print(f"Rows {start_row} to {end_row}")

                    filename_without_extension = os.path.splitext(filename)[0]

                    # Convert the chunk to CSV
                    csv_data = chunk.to_csv(index=False, header=False)

                    # Create the data dictionary
                    datos = {"fileName": filename_without_extension, "fileData": csv_data}

                    # Send the request
                    response = requests.post(url, data=json.dumps(datos), headers={"Content-Type": "application/json"})
                    print("API response:", response.text)

    except requests.exceptions.RequestException as e:
        print("Error making the request:", e)

if __name__ == "__main__":
    main()