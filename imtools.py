import os
from PIL import Image
from numpy import array, interp
from pylab import histogram

def get_imlist(path):
    """
    Returns a list of filenames for
    all jpg images in a directory.
    """
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".jpg")]

def imresize(im,sz):
    """
    Resize an image array using PIL.
    """
    return array(Image.fromarray(uint8(im)).resize(sz))

def histeq(im,nbr_bins=256):
    """
    Histogram equalization of a grayscale image.
    """
    # get image histogram
    imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
    cdf = imhist.cumsum() # cumulative distribution function
    cdf = 255 * cdf / cdf[-1] # normalize
    # use linear interpolation of cdf to find new pixel values
    im2 = interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape), cdf

def compute_average(imlist):
    """
    Compute the average of a list of images.
    """
    # open first image and make into array of type float
    averageim = array(Image.open(imlist[0]))
    size = averageim.shape
    skipped = 0.0
    for imname in imlist[1:]:
        try:
            #averageim += array(Image.open(imname))
            averageim += imresize(array(Image.open(imname)),size)
        except:
            print(imname + "...skipped")
            skipped += 1
        averageim /= (len(imlist)-skipped)
        # return average as uint8
        return array(averageim, "uint8")
