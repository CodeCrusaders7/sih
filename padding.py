import os
import numpy as np
array = np.zeros(132)
print(array.ndim)
Action = "Walking"
parent_folder = f"Trainingdata/{Action}"
flag = 0
# Iterate over subfolders (0 to 80)
for subfolder_name in range(20):
    subfolder_path = os.path.join(parent_folder, str(subfolder_name))
    i = 0
    # Check if the subfolder exists
    if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
        # Iterate over .npy files (0 to 80) within each subfolder
        while i < 80:

            npy_file_path = os.path.join(subfolder_path, f"{i}.npy")

            # Check if the .npy file exists
            if not (os.path.exists(npy_file_path) and os.path.isfile(npy_file_path)):
                flag = 1
                break
            i = i + 1
        if flag == 1:
            while i < 80:
                file_name = f"Trainingdata/{Action}/{subfolder_name}/{i}.npy"
                print(file_name)
                np.save(file_name, array)
                i = i + 1
            flag = 0
        else:
            while True:
                file_name = f"Trainingdata/{Action}/{subfolder_name}/{i}.npy"

                if os.path.isfile(file_name):
                    os.remove(file_name)
                else:
                    break
                i = i + 1
