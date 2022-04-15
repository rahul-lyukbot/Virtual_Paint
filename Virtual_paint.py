# First we have to import two libraries
import cv2
import numpy as np

# Getting access of data it can be through webcam/video
frame_width = 720
frame_height = 480
capture = cv2.VideoCapture(0)
capture.set(3, frame_width)
capture.set(4, frame_height)


# Now defining the HSV value of colour which we want to detect
my_colors = [[5, 107, 0, 19, 255, 255],    # -> Orange
              [133, 56, 0, 159, 156, 255],   # -> Purple
              [57, 76, 0, 100, 255, 255],    # -> Green
              [90, 48, 0, 118, 255, 255]]   # -> Blue

# Now defining the RGB values of my_colours
my_color_values = [[51, 153, 255],[255, 0, 255],[0, 255, 0],[255, 0, 0]]

# Now we difining the points which we want to display and looping through  it's like a line
my_points = []

# Now we are defining a function for colour detection


def find_colour(img, my_colors, my_color_values):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for color in my_colors:
        lower = np.array(color[0:3])
        upper = np.array((color[3:6]))
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = get_contour(mask)
        cv2.circle(img_copy, (x, y), 18, my_color_values[count], cv2.FILLED)
        if x != 0 and y != 0:
            new_points.append([x, y, count])
            count += 1
    return new_points


# Now Getting the contour position of images


def get_contour(img):
    contour, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area > 500:
            perimeter = cv2.arcLength(cnt, True)         # True because we know that it's closed
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)      # epilsion = 0.02*perimeter you can play with this
            x, y, w, z = cv2.boundingRect(approx)

    return x+w//2, y         # For getting the center point of bounding rect


# Now Drawing on canvus
def draw_on_canvas(my_points, my_color_values):
    for point in my_points:
        cv2.circle(img_copy, (point[0], point[1]), 10, my_color_values[point[2]], cv2.FILLED)


# Looping through each frame of video we get
while True:
    success, img = capture.read()
    img_copy = img.copy()
    newpoints = find_colour(img, my_colors, my_color_values)
    if len(newpoints) != 0:
        for new_P in newpoints:
            my_points.append(new_P)
    if len(my_points) != 0:
        draw_on_canvas(my_points, my_color_values)
    cv2.imshow("Result", img_copy)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
