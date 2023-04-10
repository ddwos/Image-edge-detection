'''When running the program as arguments one can provide
the name of graphic file and maximal percentage of edges
in the whole output file'''

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys


def black(pixel, number):
    '''Function checking if pixel is black
    number variable is sensitivity'''

    if pixel < number:
        return True
    return False


# Checking provided arguments
if len(sys.argv) == 3:
    file_name = sys.argv[1]
    edges_percentage = int(sys.argv[2])
elif len(sys.argv) == 2:
    file_name = sys.argv[1]
    # Default edges percentage in output is 20%
    edges_percentage = 20
else:
    # Asking the user when arguments not provided
    file_name = input("File name: ")
    edges_percentage = 20

# Openning graphic file
image = np.array(Image.open(file_name)).astype(np.uint8)

# Creating grayscale copy
gray_img = np.round(0.299 * image[:, :, 0] +
                    0.587 * image[:, :, 1] +
                    0.114 * image[:, :, 2]).astype(np.uint8)

# Sobel - Feldman operator
h, v = gray_img.shape
# Filters in x and y directions
y_direction_filter = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
x_direction_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

newImage = np.zeros((h, v))

print("Edge detection...")

# Acting with the operator
for i in range(1, h - 1):
    for j in range(1, v - 1):
        x_Grad = 0
        y_Grad = 0

        for x in range(3):
            for y in range(3):
                x_Grad += ((x_direction_filter[x, y] *
                            gray_img[i - 1 + x, j - 1 + y]))

        for x in range(3):
            for y in range(3):
                y_Grad += ((y_direction_filter[x, y] *
                            gray_img[i - 1 + x, j - 1 + y]))

        # Definition of the magnitude of detected edge
        magnitude = np.sqrt(x_Grad**2 + y_Grad**2)

        newImage[i - 1, j - 1] = magnitude

print("Edge detection complete")

sensitivity = 20  # 0 - max, 255 - min

print("Applying edges to the original file...")
while True:
    greens = 0  # Counting green pixels
    img2 = Image.open(file_name)  # Openning original file
    pixels2 = img2.load()  # Creating rgb pixel matrix
    for i in range(img2.size[0]):
        for j in range(img2.size[1]):
            if (i+1 < img2.size[0]) and (j + 1 < img2.size[1]):
                # Check if pixel is on the edge
                if not (black(newImage[j, i], sensitivity)):
                    # If pixel is on the edge color is changed to green
                    pixels2[i, j] = (0, 255, 0)
                    greens += 1

    # Maximal percentage check
    if (greens/(img2.size[0] * img2.size[1]) < edges_percentage/100):
        break
    sensitivity += 3  # Automatic sensitivity adjustment

print("Apllying edges completed")

fig, ax = plt.subplots()
ax.imshow(img2, interpolation='nearest')
ax.set_axis_off()
ax.patch.set_alpha(0)
ax.set_frame_on(False)
fig.tight_layout()
plt.savefig('output.jpg', transparent = True, bbox_inches='tight', 
            pad_inches=0)

# List containing angles in interval 0-180 deg
angles = []
how_many = []

for angle in range(0, 181, 4):
    angles.append(angle)
    how_many.append(0)

for i in range(len(angles)):
    angles[i] = angles[i] * np.pi / 180  # deg to rad


r = 35.0 / 7.0  # Length of detected edges
print("Checking orientation of detected edges...")

for i in range(0, img2.size[0]):
    for j in range(0, img2.size[1]):
        if (i + 1 < img2.size[0]) and (j + 1 < img2.size[1]):
            # Pixel limit protection
            if (i + r * 6 < img2.size[0]-1) and (j + r * 6 < img2.size[1] - 1):
                # Start only on green pixel
                if pixels2[i, j] == (0, 255, 0):
                    for k in range(len(angles)):  # Checkin all angles

                        # Checking is number of green pixels in high enough
                        if ((pixels2[np.floor(i+1*r*np.cos(angles[k])),
                             np.floor(j+1*r*np.sin(angles[k]))] ==
                            (0, 255, 0)) and
                            (pixels2[np.floor(i+2*r*np.cos(angles[k])),
                             np.floor(j+2*r*np.sin(angles[k]))] ==
                            (0, 255, 0)) and
                            (pixels2[np.floor(i+3*r*np.cos(angles[k])),
                             np.floor(j+3*r*np.sin(angles[k]))] ==
                            (0, 255, 0)) and
                            (pixels2[np.floor(i+4*r*np.cos(angles[k])),
                             np.floor(j+4*r*np.sin(angles[k]))] ==
                            (0, 255, 0)) and
                            (pixels2[np.floor(i+5*r*np.cos(angles[k])),
                             np.floor(j+5*r*np.sin(angles[k]))] ==
                            (0, 255, 0)) and
                            (pixels2[np.floor(i+6*r*np.cos(angles[k])),
                             np.floor(j + 6 * r * np.sin(angles[k]))] ==
                             (0, 255, 0))):

                            how_many[k] += 1

print("Orientation check completed")


fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
ax.bar(angles, how_many, 0.05)
ax.set_theta_zero_location('N')  # Set zero angle to north
ax.set_theta_direction(-1)  # Set positive angle direction to clockwise
ax.set_thetamin(0)  # Set minimum angle to 0 degrees
ax.set_thetamax(180)  # Set maximum angle to 180 degrees
# ax.set_ylabel('Occurance')
ax.set_xlabel('Angle [rad] Occurance')
plt.savefig('angles.jpg')
