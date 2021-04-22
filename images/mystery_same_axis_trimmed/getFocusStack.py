import os
import glob

# path2file = ""
pwd = "/Users/sshanto/hep/hep_daq/CAMAC/focus-stacking/images/mystery_same_axis_trimmed"
folders = [x[0] for x in os.walk(pwd)][1:]
files = [folder.split("/")[-1] for folder in folders]
# print(folders)

for i, j in enumerate(folders):
    path2file = folders[i] + "/*.png"
    # print(path2file)
    os.system(
        "/Applications/focus-stack.app/Contents/MacOS/focus-stack --verbose  --output={}.jpg {}"
        .format(files[i], path2file))
    print(
        "/Applications/focus-stack.app/Contents/MacOS/focus-stack --output={}.jpg {}"
        .format(files[i], path2file))
