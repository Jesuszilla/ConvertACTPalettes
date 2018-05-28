# Program that uses a dictionary to convert palettes
# in the .ACT format into another structure (also in
# .ACT format), usually to convert old palettes to
# color-separated palettes.
# by Jesuszilla
import os
import sys
from struct import unpack

# The process here will have to be manual on your end,
# depending on your needs. You'll need to know the
# palette indices to map from the original to the
# separated palette. You can find these indices using
# Paint Shop Pro's "Edit Palette" tool.
MAPPINGS_FROM_TO = {
    0: [0],
    1: [1],
    2: [2],
    3: [3],
    4: [4],
    5: [5],
    6: [6],
    7: [7],
    8: [8],
    9: [9],
    10: [10],
    11: [11],
    239: [239],
    240: [240],
    206: [206],
    207: [207],
    216: [216],
    217: [217],
    218: [218],
    219: [219],
    220: [220],
    221: [221],
    222: [222],
    223: [223],
    235: [235],
    236: [236],
    237: [237],
    238: [238],
    239: [239],
    240: [240],
    241: [47, 63, 79, 95, 111, 127, 143, 159, 241],
    242: [46, 62, 78, 94, 110, 126, 142, 150, 158, 242],
    243: [243],
    244: [244],
    245: [15, 30, 137, 153, 245],
    246: [45, 61, 77, 93, 109, 125, 141, 149, 157, 246],
    247: [247],
    248: [14, 29, 136, 152, 248],
    249: [249],
    250: [27, 31, 250],
    251: [44, 60, 76, 92, 108, 124, 134, 140, 156, 251],
    252: [252],
    253: [253],
    254: [13, 28, 135, 151, 254],
    255: [43, 59, 75, 91, 107, 123, 133, 139, 155, 255]
}

def main():
    pal = []
    inputFiles = []

    for arg in sys.argv[1:]:
        if "*" in arg:
            inputFiles = [filename for filename in os.listdir(".") if os.path.isfile(filename) and filename.endswith(".act")]
            break
        else:
            inputFiles.append(arg)

    # Now we open the files
    for inputFile in inputFiles:

        # Initialize with black bytes
        pal = []
        for i in range(256):
            pal.append(bytes([0,0,0]))

        colors_from = {}

        with open(inputFile, "rb") as file:
            # Check the file length
            if os.path.getsize(inputFile) != 768:
                raise ValueError("Palette file length must be 768 bytes!")

            color_from = bytes(file.read(3))
            color_to = 0
            i = 0

            # Read in the palette
            while i < 256:

                # Add the original value to the colors dictionary            
                colors_from[255-i] = color_from

                # Get next color
                color_from = bytes(file.read(3))
                i += 1

        # Now replace the colors
        for f,t in MAPPINGS_FROM_TO.items():

            # Map each "from" to "to"
            for t1 in t:
                pal[t1] = colors_from[f]

    
        if not os.path.exists("out"):
            os.mkdir("out")

        with open(os.path.join("out", inputFile), "wb+") as f:
            pal.reverse()
            for a in pal:
                f.write(a)

if __name__ == "__main__":
    main()