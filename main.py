import helpers as HelperFunctions
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


#1 load image
# image_original = mpimg.imread('test_images/solidWhiteCurve.jpg')
# image_original = mpimg.imread('test_images/solidWhiteRight.jpg')
# image_original = mpimg.imread('test_images/solidYellowCurve.jpg')
# image_original = mpimg.imread('test_images/solidYellowCurve2.jpg')
# image_original = mpimg.imread('test_images/solidYellowLeft.jpg')
image_original = mpimg.imread('test_images/whiteCarLaneSwitch.jpg')

image_copy = np.copy(image_original)

#2 grayscaling and blurring
gray = HelperFunctions.grayscale(image_original)
kernel_size=3
blur = HelperFunctions.gaussian_blur(gray,kernel_size)

#3 finding edges
low_threshold = 90
high_threshold = 110
edges = HelperFunctions.canny(blur, low_threshold, high_threshold)

#4 region on interest
imshape = image_original.shape
vertices = np.array([[(100,imshape[0]),(400, 350), (500, 320), (imshape[1],imshape[0])]], dtype=np.int32)
masked_edges = HelperFunctions.region_of_interest(edges, vertices)

#5 generating lines using hough transformation
rh = 1
theta = np.pi/180
threshold = 7
min_line_length = 5
max_line_gap = 6
lines = HelperFunctions.hough_lines(masked_edges, rh, theta, threshold, min_line_length, max_line_gap)

#6 weighted image
final_image = HelperFunctions.weighted_img(lines,image_copy)

plt.imshow(final_image)
# interp = 'bilinear'
# fig, axs = plt.subplots(nrows=4, sharex=True)
# axs[0].set_title('Original')
# axs[0].imshow(image_original, origin='upper', interpolation=interp)
#
# axs[1].set_title('Canny')
# axs[1].imshow(masked_edges, cmap='Greys_r', origin='upper', interpolation=interp)
#
# axs[2].set_title('Hough Line')
# axs[2].imshow(lines, origin='upper', interpolation=interp)
#
# axs[3].set_title('Final')
# axs[3].imshow(final_image, origin='upper', interpolation=interp)
plt.show()
