import numpy as np
import json
import os


def main():
    data_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "./test_dataset.txt"
    )
    dst_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),"../resources/testdata")
    with open(data_path, "r") as file:
        lines = file.readlines()
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    for idx, line in enumerate(lines):
        if line.startswith("C"):
            name_line = lines[idx-1].replace("//","").strip()
            lwh_line = line.replace("(","").replace(")","")
            _,length,width,height=lwh_line.split()
            cube_line = lines[idx+1][2:].replace("[","").replace("]","")
            cubes = cube_line.split(",")
            cubes = list(map(lambda x: x.replace("(","").replace(")",""), cubes))
            rst = []
            for cube in cubes:
                try:
                    cube_l, cube_w,cube_h,cube_n=cube.split()
                except:
                    breakpoint()
                for _ in range(int(cube_n)):
                    rst.append([int(cube_l), int(cube_w), int(cube_h)])
            dst_file_path = os.path.join(dst_dir, f"{name_line}.json")
            with open(dst_file_path, "w") as file:
                dic={"length":int(length), "width":int(width), "height":int(height),"input":rst}
                json.dump(dic, file,indent=4)

if __name__=="__main__":
    main()

