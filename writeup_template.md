#**Finding Lane Lines on the Road** 


**Finding Lane Lines on the Road**

The goals / steps of this project are the following:

* Step 1: Reading the image 
* Step 2: Converting the image from RGB to Gray
  
  In order to prepare input image for edge detection, it needs to be converted to grayscale first.
  method used for this conversion: ```cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)```
* Step 3: Smoothing the image using GaussianBlur

  Blurred the image using kernel_size=3 for images and kernel_size = 9 for video images for smoothing the edges to get better results from canny
* Step 4: Finding edges using Canny edge detection with a set of low and high threshold
 
 After running a few experiments found the following values as thresholds:
    * low_threshold = 90
    * high_threshold = 110
* Step 5: Marking a region that has high probablity of containing LaneLines with a set of vertices as a polygon
  
 I figured that adding margins to both (x,y) for each verice can help reduce outliers specifically in the optional-video part of the assignment
    * lower part of polygon: Xs have a margin of 150px from edges, Ys have margin of 100px from the bottom of the image 
    * upper part of polygon: Xs have a mrgin of 150px from the middle of the image(horizontally) and margin of ~60px from the middle of the image (vertically)
* Step 6: Sending the masked_region to HoughLine Transformation to detect lines
  
  Method used for this section with following paramters: ```cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)```
    * rh = 1
    * theta = np.pi/180
    * threshold = 7
    * min_line_length = 5
    * max_line_gap = 10
* Step 7: Filtering outliers and drawing lines 
* Step 8: displaying the lines on the input image 


[//]: # (Image References)

[gray_scale]: ./examples/gray_image.jpg "Grayscale"

---

### Reflection

###1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


###2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


###3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...
