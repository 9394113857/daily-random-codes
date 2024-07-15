import os
import fnmatch

# Specify the network path
network_path = r'\\DESKTOP-92QEMPM\Stores\Inv - Quality Healthcare\May 2024'

# Check if the network path exists
if not os.path.exists(network_path):
    print(f"The network path {network_path} does not exist.")
else:
    # List all files in the specified network path
    for root, dirs, files in os.walk(network_path):
        for file in files:
            if fnmatch.fnmatch(file, 'QH-????_2024-25.pdf'):
                print(file)
