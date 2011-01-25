pyMandelbrot
============

pyMandelbrot renders the Mandelbrot Set in full glorious color. To render images, it uses the pyPng library which is included for ease of use (png.py).

The program has several different options to control how the set is rendered, it takes as input:
+   A centre point to render (imaginary and real component)
+   A zoom level. A zoom level of 1 means a ratio of 1:100 pixels, 2 with 1:200 pixels, etc.
+   A width and height of image to render in pixels, this will determine the size of the final image
+   A location to save the image (chosen with a Tkinter dialog)
+   A csv file containing rgb values of colors to render in. Several samples are included.

The program will then save a PNG file to the location you specified. 