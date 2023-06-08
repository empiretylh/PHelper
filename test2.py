import tempfile
import os

# Create a temporary file with a specific name
temp_file_path = os.path.join(tempfile.gettempdir(), 'pascaltemp.txt')

# Write data to the temporary file
with open(temp_file_path, 'w') as temp_file:
    temp_file.write("Hello, World!")

# Print the path of the temporary file
print(temp_file_path)
