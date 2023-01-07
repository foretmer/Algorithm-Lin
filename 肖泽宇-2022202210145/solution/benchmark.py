import os
import json
import numpy as np

def main():
    base_folder=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../resources/testdata"
    )
    if not os.path.exists(base_folder):
        print(f"base_folder not exists!please exec tool/test_dataset.py as first!")
        exit()
    for file_name in os.listdir(base_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(base_folder, file_name)
            with open(file_path, "r") as file:
                data = json.load(file)
                length = data["length"]
                width = data["width"]
                height = data["height"]
            os.system(f"python solution/3d-map.py --length={length} --width={width} --height={height} --input_path={file_path}")

if __name__=="__main__":
    main()