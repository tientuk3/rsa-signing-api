import requests
import base64
import argparse

def main(input_file, output_file):
    # Read the hash from the input file
    with open(input_file, 'rb') as file:
        hash_binary = file.read()

    # Convert the hash to base64
    hash_base64 = base64.b64encode(hash_binary).decode('utf-8')

    # Prepare the request to the FastAPI service
    url = 'http://127.0.0.1:8000/sign/'
    headers = {'Content-Type': 'application/json'}
    payload = {'hash_base64': hash_base64}
    
    response = requests.post(url, params=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Decode the signature from base64
        signature = base64.b64decode(response.text)

        # Write the signature to a file
        with open(output_file, 'wb') as file:
            file.write(signature)
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Sign a hash using a FastAPI service.')
    parser.add_argument('--input', required=True, help='Input file containing an SHA256 hash in binary')
    parser.add_argument('--output', required=True, help='Output file to save the signature in binary')

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.input, args.output)