#**Finding Lane Lines on the Road** 


**Finding Lane Lines on the Road**

The goals / steps of this project are the following:

* Step 1: Reading the image 
* Step 2: Converting the image from RGB to Gray
  
  In order to prepare input image for edge detection, it needs to be converted to grayscale first.
  method used for this conversion: ```cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)```
  
  [image1]: ./examples/gray.png "Grayscale"

* Step 3: Smoothing the image using GaussianBlur
* Step 4: Finding edges using Canny edge detection with a set of low and high threshold
* Step 5: Marking a region that has high probablity of containing LaneLines with a set of vertices as a polygon
* Step 6: Sending the masked_region to HoughLine Transformation to detect lines
* Step 7: Filtering outliers and drawing lines 
* Step 8: displaying the lines on the input image 


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

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
