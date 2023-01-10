import pandas as pd

name, carriage, box = None, None, None
for l in open("./raw_description.txt", "r", encoding="utf-8"):
  line = l.rstrip()
  if "//E" in line:
    name = line.replace("//", "")
  if "C " in line:
    exec("carriage = " + line.replace("C ", "").replace(" ", ", "))
  if "B " in line:
    exec("box = " + line.replace("B ", "").replace(", ", ",").replace(" ", ", "))
  if box != None:
    df = pd.DataFrame(columns=["label", "length", "width", "height", "count"])
    df.loc[len(df)] = ["C", carriage[0], carriage[1], carriage[2], 1]
    for b in box:
      df.loc[len(df)] = ["B", b[0], b[1], b[2], b[3]]
    df.to_csv(name + ".csv", index=False)
    name, carriage, box = None, None, None
  