import pandas as pd
import subprocess
import json

# Sign into AZ CLI with az login cmd first before running this script

key_vault_name = 'kv-mlx-preprod001' # Update this path

# Read the CSV file
csv_file = 'c:\\scripts\\keyvault\\akv-preprod001-7-9-24.csv'  # Update this path
data = pd.read_csv(csv_file)

# Iterate over each row in the CSV file and add the secret to Key Vault
for index, row in data.iterrows():
    secret_name = row['secret_name']
    secret_value = row['secret_value']

    # Check if the secret already exists
    check_command = f"az keyvault secret show --vault-name {key_vault_name} --name {secret_name}"
    check_process = subprocess.run(check_command, shell=True, text=True, capture_output=True)

    if check_process.returncode == 0:
        print(f"Secret {secret_name} already exists, skipping...")
    else:
        # Construct the Azure CLI command to add the secret
        # Use json.dumps() to escape special characters in the secret value
    
        escaped_secret_value = json.dumps(secret_value)
        add_command = f"az keyvault secret set --vault-name {key_vault_name} --name {secret_name} --value {escaped_secret_value}"

        try:
            # Execute the command
            add_process = subprocess.run(add_command, shell=True, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to add secret {secret_name}. Error: {str(e)}")
        else:
            if add_process.returncode == 0:
                print(f"Successfully added secret {secret_name}")

print("All secrets processed.")
