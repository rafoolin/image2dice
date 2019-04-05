#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import datetime

import cv2
# import inspect
import cairosvg


class Converter():
    '''This class Converts SVG to PNG.

    Produces PNG images from 6 faces of a die (with chosen style and length).
    Saves the PNG files for later use.

    Attributes:
        die: An Die object with chosen style and side length.
        dieSide: length of the die sides.
        resDir: Absolute path(address) of the module's resources directory.
        svgPath: Absolute path(address) of SVG file's directory.
        exportPath: Absolute path(directory) where to save the PNG images.
    '''

    def __init__(self, die):
        '''Initialize pathes.'''
        self.dieSide = die.getSide()
        # Path of module directory
        modulePath = os.path.realpath(__file__)
        self.resDir = os.path.join(os.path.dirname(modulePath), 'resources')
        self.svgPath = os.path.join(self.resDir, 'dice-styles', die.getStyle())
        self.exportPath = os.path.join(self.resDir, '.dice-png')
        # Creates PNG files directory
        if not os.path.exists(self.exportPath):
            os.mkdir(self.exportPath)

    def svg2png(self):
        '''Convert SVG to PNG images and return a dictionary of them.'''
        # dictionary of produced PNG images
        pngImages = {}

        for n in range(1, 7):
            # Path of <n> SVG file in directory
            url = os.path.join(self.svgPath, '{}.svg'.format(n))
            # Path of <n> PNG file will write to
            writeTo = os.path.join(self.exportPath, '{}.png'.format(n))
            # Convert from <n> SVG to <n> PNG
            cairosvg.svg2png(url=url, write_to=writeTo, scale=self.dieSide)
            # Add new PNG file to <pngImages> dictionary
            pngImages[n] = cv2.imread(writeTo, 0)
        print('Dice with style {} and side {} are successfully created!'
              .format(die.getStyle(), die.getSide()))
        return pngImages


class Die():
    '''This class simulates a die.

    A die can be built from a few styles.

    Attributes
        style: A code(a number) Specifying one of the SVG styles
        side: Length of the die's side
    '''

    def __init__(self, style, side):
        '''Initialize user defined die style and side length.'''
        self.style = str(style) if style else '1'
        self.side = side if side else 1

    def getStyle(self):
        '''Return die style.'''
        return self.style

    def getSide(self):
        '''Return die's side length.'''
        return self.side


class Image():
    '''This class make an image and do some operation on it.

    This class imports an image's path and make a grayscale image object.
    Replaces an area of the main image by another image intensities.
    Calculates mean of an specified area from image.
    Saves an image on Hard Disk.

    Attributes:
        imgPath: Path(address) of an image file.
        img: Image object(In Grayscale) from the given path.
    '''

    def __init__(self, imgPath):
        '''Initialize image object.'''
        self.imgPath = imgPath
        self.img = cv2.imread(self.imgPath, 0)

    def getImage(self):
        '''Return image.'''
        return self.img

    def setImage(self, newImg, r, c):
        '''Replace an area of main image by one die image.

        It replaces intensities from die image as much as possible.
        It chooses some intensities from die face.
        if remaining pixels on main image is less than the side of die.

        Args:
            newImg: One of the die faces in PNG.
            r: Row index of start Pixel.
            c: Column index of start Pixel.
        '''

        # number of rows and columns on image and die
        imgRows, imgCols = self.img.shape[:2]
        row, col = newImg.shape[:2]

        # Minimum row/col from main image and die
        minRow = min(row, imgRows-r)
        minCol = min(col, imgCols-c)

        # Set minimum
        self.img[r:r+minRow, c:c+minCol] = newImg[0:minRow, 0:minCol]

    def getAreaMean(self, x, y, width, height):
        '''Return intensities mean of desired shape in the image.

        It calculates pixel's intensities mean an area.
        Area's shape is a rectangle.

        Args:
            x: Left pixel poison of the rectangle shape.
            y: Top pixel position of the rectangle shape.
            width: width of the rectangle shape.
                   or number of columns from the x in the image.
            height: height of the rectangle shape.
                   or number of rows from the y in the image.

        Returns:
            Intensities mean of the desired area.

        '''
        # Extract desired rectangle shape from image
        imgSub = self.img[x:x+height, y:y+width]
        # calculates mean of intensities from extracted image
        mean = cv2.mean(imgSub)[0]
        return mean

    def saveImg(self):
        '''Saves an image on Hard Disk.

        It saves result beside the input image.
        And adds timestamp(formatted) to avoid overriding the results.
        '''
        dirname, basename = os.path.split(self.imgPath)
        fileName = os.path.splitext(basename)[0]

        # add timestamp in a formatted style to fileName
        fileName = '{}-{}.jpg'.format(
            fileName,
            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        )
        # Write image
        writePath = os.path.join(dirname, fileName)
        saved = cv2.imwrite(writePath, self.img)

        if saved:
            print('Image is saved on ', dirname)
        else:
            print("Error!!, Sorry image couldn't be saved.")


class Img2dice():
    '''This Class build up the given image by dice.

    instead of main image pixel it replaces one of die's faces.
    all these dice make a representation of the main image.

    Attributes:
        image: An Image object
        die: An Die object
        diceImages: Dictionary of PNG images from die's faces.

    '''

    def __init__(self, image, die):
        '''Initialize the user defined image and die.'''
        self.image = image
        self.die = die
        converter = Converter(die)
        self.diceImages = converter.svg2png()

    def img2dice(self):
        '''Return built image from dice.

        Instead of 256 intensity level, there will be 6 (die sides).
        For Light Die 0 Intensity is mapped to 6 and 255 is mapped to 1
        For dark Die 0 Intensity is mapped to 1 and 255 is mapped to 6
        and based on the die's side length, each part of the image,
        which is equal to the die area will be replaced by the die's faces.
        based on the intensities mean of that area on the main image.

        Returns:
            an image made of die faces.

        '''
        # height, width of Image
        row, col = self.image.getImage().shape[:2]
        # die side length
        side = self.die.getSide()
        style = self.die.getStyle()

        for r in range(0, row, side):
            for c in range(0, col, side):
                mean = self.image.getAreaMean(r, c, side, side)
                # Convert image intensity range from 0-255 to 1-6
                # And Choose the right formula
                if style in ['5', '6']:
                    dieNum = int(mean * 5 / 255 + 1)
                else:
                    dieNum = int(abs(255 - mean) * 5 / 255 + 1)

                # replace intensities by the die intensities
                self.image.setImage(self.diceImages[dieNum], r, c)

        print('Image converted to dice successfully!')
        return self.image.getImage()


# -------------------  End of Modules ------------------------------

def isImageFile(path):
    '''Check if path is an image address.

    It checks if given addres is a valid addres for an image.
    And if it is in a valid format(accepted formats).

    Args:
        path: addres of an image file.

    Returns:
        absolute address of the image file.

    Raise:
        ArgumentTypeError: Error occurs when path is invalid.
            If it's an inalid path or of another file but image.
            And if it is not in a valid image's format.
    '''

    # Valid formats
    validFormat = {'.jpeg', '.jpg', '.png', '.bmp'}
    basename = os.path.splitext(path.lower())

    if not (os.path.isfile(path) and basename[-1] in validFormat):
        msg = '\n\nSome Error has happend:' \
              '\n\t1.File not exists.' \
              '\n\t2.Not an image file.' \
              '\n\t3.Valid formats are :[{}].'.format(', '.join(validFormat))
        raise argparse.ArgumentTypeError(msg)
    return os.path.realpath(path)


def getArgs():
    '''Return Terminal/Command line arguments.

    Run one of the bellow commands in Terminal/Command line.
    To see more information on how to use this module.
        >>> img2dice -h
        >>> python3 img2dice -h
    '''
    parser = argparse.ArgumentParser(
        prog='img2dice',
        formatter_class=argparse.RawTextHelpFormatter,
        description='''This Module builds up an image from die \
            \n----------------------------------------------------- \
            \nSome Example : \
                \n\t./img2dice.py ./sample/input/sample1.jpg -side 10 -style 2 --save \
                \n\t./img2dice.py ./sample/input/sample2.jpg -side 1 --save \
                \n\t./img2dice.py ./sample/input/sample2.jpg  -style 3 --save \
                \n\t./img2dice.py ./sample/input/sample1.jpg''')

    parser.add_argument('input',
                        type=isImageFile,
                        help='Path of an image file')

    parser.add_argument('-style',
                        type=int,
                        choices=range(1, 7),
                        help="Choose one of the style's code")

    parser.add_argument('-side',
                        type=int,
                        help="Enter a number as length of die's side")

    parser.add_argument('--save',
                        action='store_true',
                        help='Save the result as an Image')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 1.0.0')

    return parser.parse_args()


if __name__ == "__main__":
    '''Run when module run directly.'''
    args = getArgs()

    die = Die(style=args.style, side=args.side)
    img = Image(imgPath=args.input)
    converter = Img2dice(img, die)

    newImg = converter.img2dice()
    cv2.imshow('Image In Dice ( Press any key to quit... )', newImg)
    cv2.waitKey()
    cv2.destroyAllWindows()

    if args.save:
        img.saveImg()
