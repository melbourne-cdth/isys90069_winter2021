import numpy as np
#from skimage.io import imshow
import os
import pydicom
import pandas as pd
import ipywidgets as ipw
import altair as alt

from ipywidgets import interact, fixed

DDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./data/")

def win_lev(img, w, l, maxc=255):
    """
    Window (w) and level (l) data in img
    img: numpy array representing an image
    w: the window for the transformation
    l: the level for the transformation
    maxc: the maximum display color
    """

    m = maxc/(2.0*w)
    o = m*(l-w)
    return np.clip((m*img-o),0,maxc).astype(np.uint8)

def view_img(img,w,l):
    imshow(win_lev(img.pixel_array, w, l), cmap="gray")

def view_volume(img,s, w, l):
    imshow(win_lev(liver.pixel_array[s,:,:],w,l))

def view_dicom_name(img, item):
    try:
        print(img[item])
    except Exception as error:
        print(error)
        print()

def get_img_histo(img, win=None, nbins=100):

    idata = img.pixel_array.flatten()
    label = "Pixel Values: %s= %s (%+4d - %+4d)"%(img[(0x008, 0x0060)].name,
                                                         img[(0x008, 0x0060)].value,
                                                         np.min(idata), np.max(idata))
    if win == None:
        win = [np.min(idata), np.max(idata)]
    tmp = np.extract((idata >=win[0])& (idata <=win[1]), idata)
    hist, bin_edges = np.histogram(tmp, bins=nbins)
    data = pd.DataFrame({label:bin_edges[:-1],
                         "count":hist})
    return alt.Chart(data).mark_bar().encode(
                 x=label,
                 y='count').properties(width=256, height=256)





def get_examine_dicom_widget(imgs, allmin, allmax):
    img_select = ipw.Dropdown(options=imgs.items(),
                             layout=ipw.Layout(width="256px"))

    win_select = ipw.IntRangeSlider(value=[allmin, allmax],
                                        max=allmax,
                                        min=allmin,
                                       layout=ipw.Layout(width="300px"))

    a = interact(get_img_histo,img=img_select, win=win_select, nbins=50)
    a.widget.layout = ipw.Layout(width="375px")
    win = ipw.IntSlider(value=500, min=1, max=5000)
    lev = ipw.IntSlider(values=500, min=allmin, max=allmax)
    iow = ipw.Output(layout=ipw.Layout(width="300px"))

    def view_img(img, w, l):
        iimg = img.pixel_array
        with iow:
            imshow(win_lev(iimg, w, l), cmap="gray")

    b = interact(view_img, img=img_select, w=win, l=lev)
    b.widget.layout = ipw.Layout(width='375px')
    return ipw.HBox([b.widget, a.widget])

def get_data():
    return {i:pydicom.dcmread(os.path.join("data",f"I{i}.dcm")) for i in [1,2,3,4]}

