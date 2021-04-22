import os
"""

"""
interps = [
    "none", "nearest", "bilinear", "bicubic", "spline16", "spline36",
    "hanning", "hamming", "hermite", "kaiser", "quadric", "catrom", "gaussian",
    "bessel", "mitchell", "sinc", "lanczos"
]

fileNames = ["mystery", "lead_bricks", "lead_bricks_gaps"]

for file in fileNames:
    for interp in interps:
        os.system("python3 focus_stacking_algo.py {} {}".format(interp, file))
        print("Done with " + interp + " for " + file)

#os.system(pythonCommand)
