# image2dice

> This is a really simple project but I tried to treat
it as a real project for educational purposes :)

This project builds an image
from dice pieces and die's style
and side length can be defined.
Idea for this project is from [YouTube](https://youtu.be/yDU-0cN43eQ) or
[Jadi](https://github.com/jadijadi/educational_python_scripts/tree/master/image2dice_pattern)
, but I changed some of it's features.

Instead of defining number of dice in
rows and columns to build the main image,
I decided to define the length of the die(in Pixel) to replace
Pixels of the image, so number of dice in rows and columns of the image depends on die side's length.

There are 6 styles for die to be chosen:

|Style 1| Style2| Style3| Style4| Style5| Style6|
|-------|-------|-------|-------|-------|-------|
|![syle1](./git-res/style-1.png)|![syle2](./git-res/style-2.png)|![syle3](./git-res/style-3.png)|![syle4](./git-res/style-4.png)|![syle5](./git-res/style-5.png)|![syle6](./git-res/style-6.png)|


# Getting Started

These instruction helps You to run the project.

# Prerequisites

```
OpenCV > 3.0.0

Python3

cairosvg
```
# Installation
You can install OpenCV and cairo
(for Windows user in order to  install cairosvg)
with less effort with the help of [Anaconda](https://www.anaconda.com/)
rather than building them from the source code.


1. To install **Python3** You can use the official
[WEBSITE](https://www.python.org/downloads/).

2. **Skip this step if You used Anaconda.**

    To install [OpenCV](https://opencv.org/) You can check the website 
    or on Linux You can use this command:
    ```shell
    sudo apt install python3-opencv
    ```
    Or to build it from the source code, if You're on Linux this [SCRIPT](https://milq.github.io/install-opencv-ubuntu-debian/)
    may help You a lot.

3. To install **cairosvg** follow this [LINK](https://cairosvg.org/).


To test if modules are installed correctly or not, do the following:

1. Open Terminal / Command Line

2. Type python or python3 (if default is Python 2.7) and press Enter, if it is installed correctly
  You should see something like this(Python interactive mode):
    ```shell
    Python 3.7.2+ (default, Feb 27 2019, 15:41:59)
    [GCC 8.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    ```
3. Import OpenCV and cairosvg modules(Type bellow commands after >>>)
    ```python
    import cv2  
    import cairosvg
    ```

If it showed nothing that means both are installed successfully but
if not, You should try to install the one which failed.


# Running the tests
After installing prerequisites follow the bellow steps to test the project:
1. Download the project and unzip it.
2. Open the Terminal / Command Line.
3. Change to the project directory where **img2dice.py** is located
(I assumed project directory is on Download directory)
    ```bash
    cd /Download/image2dice-master/image2dice-master/image2dice
    ```
4. Run the below command on Terminal/Command Line to get more information: (Remove 3 if it doesn't work)

    ```bash
    python3 image2dice.py -h
    ```

# Samples
There are two samples.

## First Sample:
```
Die:
    Length: 1
    Style: 2
```
Paste the following command in Terminal/Command Line:
```bash
python3 img2dice.py ./sample/input/sample1.jpg -side 1 -style 2 --save
```
Result is like this:
### Input:
![img](./image2dice/sample/input/sample1.jpg)

### Output:
![img](./image2dice/sample/output/sample1-2019-03-16_17-40-12.jpg)


## Second Sample:
```
Die:
    Length: 20
    Style: 1
```
Paste the following command in Terminal/Command Line:
```bash
python3 img2dice.py ./sample/input/sample2.jpg -side 20 -style 1 --save
```
Result is like this:
### Input:
<img width="600" src="./image2dice/sample/input/sample2.jpg">

### Output:
> In this output, dice faces are noticeable.(download it to see)

<img width="600" src="./image2dice/sample/output/sample2-2019-03-16_17-41-03.jpg">

# To-Do

- [ ] Use better algorithm.
- [ ] Remove `cairosvg` and use Math packages to define die faces.
- [ ] Add GUI version.


# License

Code is under [MIT](./LICENSE) License.

First photo by [Eye for Ebony](https://unsplash.com/photos/OWi1sIWiCAI?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com)


Second photo by [Rodrigo Pereira](https://unsplash.com/photos/GFwzGcv2gqc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com)
