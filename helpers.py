#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
LEFT= 'LEFT'
RIGHT= 'RIGHT'

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def find_slope(x1,y1,x2,y2):
    return ((y2-y1)/(x2-x1))

def find_side(slope, avg_x, avg_y, x_mid_line):
    #to ignore outlires in each side, added a comparison to middle line x value
    if slope < 0 and avg_x <= x_mid_line: # and avg_y >=y_mid_line:
        return LEFT
    elif slope >0 and avg_x >= x_mid_line: # and avg_y>=y_mid_line:
        return RIGHT
    else:
        return

def filter(lines, threshold=6):

    lines_copy = lines.copy()
    difference = np.abs(lines - np.median(lines))
    median_difference = np.median(difference)
    if median_difference == 0:
        s = 0
    else:
        s = difference / float(median_difference)
    mask = s > threshold
    lines[mask] = np.median(lines)
    return lines


def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    left_line = np.empty((0,2), dtype=np.int32)
    right_line= np.empty((0,2), dtype=np.int32)

    x_mid_line = img.shape[1]/2
    for line in lines:
        for x1,y1,x2,y2 in line:
            avg_x = int((x1+x2)/2)
            avg_y = int((y1+y2)/2)
            length = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
            slope = find_slope(x1,y1,x2,y2)
            side=find_side(slope , avg_x, avg_y,x_mid_line)
            if  side == LEFT:
                left_line = np.append(left_line,np.array([[avg_x, avg_y]]), axis=0)
            elif side == RIGHT:
                right_line = np.append(right_line,np.array([[avg_x,avg_y]]), axis=0)

    left_line = filter(left_line)
    right_line = filter(right_line)


    # negative slope:
    if len(left_line) >0:
        # y = ax+b
        left_line = left_line[left_line[:,0].argsort()]
        x1_left,y1_left= left_line[0]

        x2_left,y2_left = left_line[len(left_line)-1]

        bottom_fix_y = img.shape[0]
        top_left = [x2_left, y2_left]
        try:
            a, b = np.polyfit((x1_left,x2_left), (y1_left,y2_left), 1)
            bottom_fix_x = int((bottom_fix_y - b )/a)
            gap = 150
            x_mid = int(img.shape[1]/2-gap)
            if bottom_fix_x <0 or bottom_fix_x<gap :
                bottom_fix_x=gap
            cv2.line(img, (top_left[0],top_left[1]), (bottom_fix_x, bottom_fix_y), color, thickness)
        except Exception as err:
            print(err)
            pass

    # negative slope:
    if len(right_line) >0:
        # y = ax+b
        right_line = right_line[right_line[:,0].argsort()]
        x1_right,y1_right= right_line[0]

        x2_right,y2_right = right_line[len(right_line)-1]

        bottom_fix_y = img.shape[0]
        top_right = [x1_right, y1_right]
        try:
            a, b = np.polyfit((x1_right,x2_right), (y1_right,y2_right), 1)
            bottom_fix_x = int((bottom_fix_y - b )/a)
            x_mid = int(img.shape[1]/2-150)
            if bottom_fix_x<x_mid: bottom_fix_x=x_mid
            cv2.line(img, (top_right[0],top_right[1]), (bottom_fix_x, bottom_fix_y), color, thickness)
        except Exception as err:
            print(err)
            pass


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)
