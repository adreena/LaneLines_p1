#**Finding Lane Lines on the Road** 


**Finding Lane Lines on the Road**

The goals / steps of this project are the following:

* Step 1: Reading the image 
* Step 2: Converting the image from RGB to Gray
* Step 3: Smoothing the image using GaussianBlur
* Step 4: Finding edges using Canny edge detection with a set of low and high threshold
* Step 5: Marking a region that has high probablity of containing LaneLines with a set of vertices as a polygon
* Step 6: Sending the masked_region to HoughLine Transformation to detect lines
* Step 7: Filtering outliers and drawing lines 
* Step 8: displaying the lines on the input image 

Gaols:
* Developing a robust pipeline to detect laneline on different roads
* Detecting outliers and how they affect the lines




[//]: # (Image References)

[gray_scale]: ./examples/gray_image.jpg "Grayscale"

---

### Reflection

In order to prepare input image for edge detection, first it needs to be converted to grayscale first. Smoothing the edges to get better results from canny and for blurring the images I used kernel_size=3 and kernel_size = 9 for video frames. 
Next step is to pass the blurred_image to Canny edge detection, after running a few experiments I found the following values as thresholds
 * low_threshold = 90
 * high_threshold = 110

For finding region of interest, I defined apolygon with added margins to both (x,y) from image_corners which can help reduce outliers specifically in the optional-video part of the assignment:
    * lower part of polygon: Xs have a margin of 150px from edges, Ys have margin of 100px from the bottom of the image 
    * upper part of polygon: Xs have a mrgin of 150px from the middle of the image(horizontally) and margin of ~60px from the middle of the image (vertically)

Then I passed the masked_area to HoughLine transformation with followign paramters:
    * rh = 1
    * theta = np.pi/180
    * threshold = 7
    * min_line_length = 5
    * max_line_gap = 10

The most difiicult step was to detect outliers and draw a perfect line between points, In this section I did the following modifications to remove outliers from data_points and connect lines on each side to form a solid line
   * I separated the lines based on their slope negative/postive into 2 sets of left_lines and right_lines accordingally
     As a further step to remove some of the outliers, I added another check to see if the points have correct position by comparing their x value (as avarage of x1 & x2 of the line) to x_middle of the image : 
     * 1- if slope is negative and x_avg <= x_middle it's accpeted and appended to left_lines
     * 2- if slope is postive and x_avg >= x_middle , it's accepted and appended to right_lines
   * After creating 2 lists of left/right lines , I passed each list through another filtering process by comparing their differences from the median of lines (in each list). Those having a difference bigger than threshold=6 are kept and the rest are masked-out.
   * For the last step :
     * I sorted filtered_lists based on their x values to find points with minimum/maximum x-values. 
     * Then I calculated coefficients of a fitting line between these 2 points to find `a` and `b` of `y=ax+b` using polyfit.
     * Next I plotted a point(x,y) on the fitted line that has y=image.hight, this helps to have Lane_Lines starting from the bottom of the image as (x1,y1)
     * Final step is to connect a line from the bottom point(x1,y1) that I found form the previous step to a point with highest x-value from the list as(x2,y2)

And as the last step , I added lines to input_image to display how it's fitting the lanelines.



###2. Shortcommings:
Pipleline is very sensitive to outliers even after removing a bunch of them from datapoints there are still jumps in some frames, I think it might be related to image resolution (each frame might have a different resolution) and curves in the lanelines needs a better fitting approach other than `y= ax+b`.
Another big flaw in the whole approach is when we don't have lines on the streets! I happened to observe streets with no lines (very faded lines) or when streets are covered with snow, there would be no lines and this pipeline won't help much.

###3. Suggest possible improvements to your pipeline

 * 1- Detecting curves can improve line fitting where road is bending.
 * 2- Training a model on images to find a relative region based on different features (such as image_size, camera resolution, angle , ...) can help reducing point_dependency in laneline detection, specially on roads with no lines.

