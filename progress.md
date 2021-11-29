# Stagehand Development

## 2021-11-29 3pm

- Set up development environment using conda and git 
- Followed instructions from https://blog.roboflow.com/m1-opencv/ to install OpenCV on Apple Silicon 
- Install `pyvirtualcam` from https://github.com/letmaik/pyvirtualcam 

### Note 1

The sample script from `pyvirtualcam` works - it displays a grayscale image on the screen. Setting up the OBS virtual camera was a bit finnicky, but the tutorial on the github page seemed to work. It involves turning on and off the virtual camera in OBS and possibly closing OBS. 

### Note 2

The next step is to get the webcam working using OpenCV

Attempted to install using `pip install opencv-python` got the error:


Attempted to follow this tutorial: https://blog.roboflow.com/m1-opencv/. But when running
```python
import cv2
vc = cv2.VideoCapture(0)
```
I get an error: 
```
cv2.error: OpenCV(4.5.3) /Users/runner/miniforge3/conda-bld/libopencv_1632857378385/work/modules/videoio/src/cap.cpp:239: error: (-215:Assertion failed) !info.backendFactory.empty() in function 'open'


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/cory/Documents/Stagehand/test.py", line 6, in <module>
    vc = cv.VideoCapture(0)
SystemError: <class 'cv2.VideoCapture'> returned a result with an error set
```

- Googling didn't fix much

Next, tried to reinstall `OpenCV` by compiling it myself using this tutorial: https://sayak.dev/install-opencv-m1/ 

- Downloading the files from https://github.com/opencv/opencv/archive/4.5.3.zip and https://github.com/opencv/opencv_contrib/archive/4.5.3.zip
- Involved installing `cmake` and running this command:
```zsh
cmake \
  -DCMAKE_SYSTEM_PROCESSOR=arm64 \
  -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DWITH_OPENJPEG=OFF \
  -DWITH_IPP=OFF \
  -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=/Users/cory/Documents/OpenCV/opencv_contrib-4.5.3/modules \
  -D PYTHON3_EXECUTABLE=/Users/cory/opt/anaconda3/envs/stagehand/bin/python3 \
  -D BUILD_opencv_python2=OFF \
  -D BUILD_opencv_python3=ON \
  -D INSTALL_PYTHON_EXAMPLES=ON ..
```

Ended up getting an error:
```
ImportError: dlopen(/Users/cory/opt/anaconda3/envs/stagehand/lib/python3.9/site-packages/cv2.so, 0x0002): tried: '/Users/cory/opt/anaconda3/envs/stagehand/lib/python3.9/site-packages/cv2.so' (mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')), '/usr/local/lib/cv2.so' (no such file), '/usr/lib/cv2.so' (no such file), '/usr/local/lib/python3.9/site-packages/cv2/python-3.9/cv2.cpython-39-darwin.so' (mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')), '/usr/local/lib/cv2.cpython-39-darwin.so' (no such file), '/usr/lib/cv2.cpython-39-darwin.so' (no such file)
```
- Seems like it expects and intel version, maybe one of the packages wasn't installed correctly?

### Note 3

I think I got it working - had to reinstall OBS using the Intel version rather than the M1 version I got from Reddit...

### Note 4

When taking the webcame, need to convert the OpenCV `BRG` to regular `RGB`. 
```python
frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
```

## 2021-11-29 10pm

Face detection, using OpenCV: https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81 

- It works
- Is quite laggy when doing the calculation, would need to optimise, e.g. only calculate once very second
	- Fix this by adjusting the scaling factor when doing the computation
- Need to ensure that the dimensions of the cropped image align with the virtual camera
	- Use `cv.resize()` 

### Note 1

There is occassionally an error when using the virtual camera, where it exits:
```
Traceback (most recent call last):
  File "/Users/cory/Documents/Stagehand/test.py", line 84, in <module>
    frame_rgb = cv.resize(cv.cvtColor(frame_crop, cv.COLOR_BGR2RGB), (WIDTH, HEIGHT))
cv2.error: OpenCV(4.5.4) /Users/runner/work/opencv-python/opencv-python/opencv/modules/imgproc/src/color.cpp:182: error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'
```

- Might mean that the `frame_crop` is empty? 

## 2021-11-30 12am

Smoothing out the cropping motion using Kalman Filters. 
- https://stackoverflow.com/questions/42904509/opencv-kalman-filter-python 
