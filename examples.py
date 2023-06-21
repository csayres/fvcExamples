from astropy.io import fits
from skimage.exposure import equalize_hist
from skimage.transform import SimilarityTransform
import numpy
import matplotlib.pyplot as plt

from zhaoburge import getZhaoBurgeXY, fitZhaoBurge

ff = fits.open("proc-fimg-fvc1n-0100.fits")
imgHeader = ff[1].header
fcm = ff["FIDUCIALCOORDSMEAS"].data  # fiducial measurement table
ptm = ff["POSITIONERTABLEMEAS"].data  # robot measurement table


def getImgData():
    # subtract the median value column by column
    # as a rough bias subtraction
    imgData = ff[1].data
    imbias = numpy.median(imgData, axis=0)
    imbias = numpy.outer(
        numpy.ones(imgData.shape[0]), imbias
    )
    imgData = imgData - imbias
    return imgData


def plotDetections():
    # creates figures 1 a and b.
    imgData = getImgData()

    plt.figure(figsize=(10,10))
    # equalize_hist does something like z-scale
    plt.imshow(equalize_hist(imgData), origin="lower", cmap="bone")
    plt.xlabel("x CCD (pixels)")
    plt.ylabel("y CCD (pixels)")
    plt.savefig("fig_1_a.png", dpi=250)

    # plot a white circle around metrolgy fiber detections
    # only keep trusted detections
    _ptm = ptm[ptm["wokErrWarn"] == False]
    x = _ptm["x"]
    y = _ptm["y"]
    plt.plot(x, y, 'o', ms=5, mew=0.5, mfc="none", mec="white", label="metrology fibers")

    # plot cyan squares around fiducial fiber detections
    # only keep trusted detections
    _fcm = fcm[fcm["wokErrWarn"] == False]
    x = _fcm["x"]
    y = _fcm["y"]
    plt.plot(x, y, 's', ms=8, mew=0.5, mfc="none", mec="cyan", label="fiducial fibers")

    plt.legend()
    plt.savefig("fig_1_b.png", dpi=250)
    # plt.show()
    # import pdb; pdb.set_trace()


def plotNudgeCorrection():
    # creates figure 2 a
    # for each metrology fiber show the effect of the nudge
    # correction
    _ptm = ptm[ptm["wokErrWarn"] == False]
    x = _ptm["x"]
    y = _ptm["y"]
    dx = _ptm["xNudge"] - x
    dy = _ptm["yNudge"] - y

    plt.figure(figsize=(10,10))
    q = plt.quiver(x,y,dx,dy,angles="xy",units="xy",scale=0.001, width=10)
    plt.quiverkey(q,0.9,0.9,0.25,"0.25 pixels",coordinates="figure")
    plt.axis("equal")
    plt.xlabel("x CCD (pixels)")
    plt.ylabel("y CCD (pixels)")
    plt.title("Nudge Correction for Metrology Fiber Detections")

    plt.savefig("fig_2_a.png", dpi=250)
    # plt.show()


def plotWokCorrections(refit=True):
    """If refit=True, then refit the CCD to wok transforms based on
    centroid data for fiducials, if False then read the coefficients from the
    fits header.
    """
    if refit:
        # fit distortion models using fiducial coordinates
        _fcm = fcm[fcm["wokErrWarn"] == False]
        xCCD = _fcm["xNudge"]
        yCCD = _fcm["yNudge"]
        xWok = _fcm["xWok"]
        yWok = _fcm["yWok"]

        xyCCD = numpy.array([xCCD,yCCD]).T
        xyWok = numpy.array([xWok,yWok]).T
        simTrans = SimilarityTransform()
        simTrans.estimate(xyCCD,xyWok)

        xyWokFit = simTrans(xyCCD)

        # provide a list of which ZB terms to use
        # 33 is the max number of terms
        polids = numpy.arange(33, dtype=numpy.int16)

        polids, coeffs = fitZhaoBurge(
            xyWokFit[:, 0],
            xyWokFit[:, 1],
            xyWok[:, 0],
            xyWok[:, 1],
            polids=polids,
        )
    else:
        translation = [imgHeader["FVC_TRAX"], imgHeader["FVC_TRAY"]]
        rotation = numpy.radians(imgHeader["FVC_ROT"])
        scale = imgHeader["FVC_SCL"]
        simTrans = SimilarityTransform(translation=translation, rotation=rotation, scale=scale)

        # extract the 33 Zhao-Burge polynomial model
        # coeffs saved in header
        polids = numpy.arange(33, dtype=numpy.int16)
        coeffs = []
        for polid in polids:
            coeffs.append(imgHeader["FVC_ZB%i"%polid])


    # begin with "good" xyNudge CCD locations
    # of robot metrology fibers
    _ptm = ptm[ptm["wokErrWarn"] == False]
    x = _ptm["xNudge"]
    y = _ptm["yNudge"]
    xyNudge = numpy.array([x,y]).T

    # convert from nudge to (undistorted) wok coordinates
    xyWok = simTrans(xyNudge)

    plt.figure(figsize=(10,10))
    plt.plot(xyWok[:,0],xyWok[:,1],"o",mec="black", mfc="none", ms=5)
    plt.axis("equal")
    plt.xlabel("x wok (mm)")
    plt.ylabel("y wok (mm)")
    plt.title("xyNudge coordinates translated/rotated/scaled into wok frame.")
    plt.savefig("fig_3_a.png", dpi=250)


    dx, dy = getZhaoBurgeXY(
        polids,
        numpy.array(coeffs),
        xyWok[:, 0],
        xyWok[:, 1],
    )

    q = plt.quiver(xyWok[:,0], xyWok[:,1], dx, dy, angles="xy", units="xy", scale=0.05, width=1)
    plt.quiverkey(q,0.9,0.9,0.5,"500 micron",coordinates="figure")
    plt.title("Zhao-Burge polyfit from fiducials (dynamic distortion model)")
    plt.savefig("fig_3_b.png", dpi=250)

    # apply the model correction
    xyWok = xyWok + numpy.array([dx,dy]).T

    # finally show the final correction (ZB fit from dither residuals)
    plt.figure(figsize=(10,10))
    plt.plot(xyWok[:,0],xyWok[:,1],"o",mec="black", mfc="none", ms=5)
    plt.axis("equal")
    plt.xlabel("x wok (mm)")
    plt.ylabel("y wok (mm)")

    q = plt.quiver(xyWok[:,0], xyWok[:,1], _ptm.xWokAdjMetrology, _ptm.yWokAdjMetrology, angles="xy", units="xy", scale=0.002, width=1)
    plt.quiverkey(q,0.9,0.9,0.050,"50 micron",coordinates="figure")
    plt.title("Zhao-Burge polyfit from dither residuals (zbplus2 static distortion model)")
    plt.savefig("fig_3_c.png", dpi=250)


def plotFiberPositionError():
    # creates figure 4 a

    # plots the difference between desired and measured
    # metrology fiber location, this is what the FVC loop
    # minimizes iteratively
    fd = ff["FIBERDATA"].data

    # filter for only metrology fibers
    fd = fd[fd["fibre_type"] == "Metrology"]

    # filter out dubious fibers
    fd = fd[fd["DUBIOUS"] == False]

    xExpect = fd["xwok"]
    yExpect = fd["ywok"]
    xMeas = fd["xwok_measured"]  # note should match "xWokMeasMetrology" in POSITIONERTABLE
    yMeas = fd["ywok_measured"]  # note should match "xWokMeasMetrology" in POSITIONERTABLE
    dx = xExpect - xMeas
    dy = yExpect - yMeas

    plt.figure(figsize=(10,10))
    q = plt.quiver(xMeas, yMeas, dx, dy, angles="xy", units="xy", scale=0.005, width=1)
    plt.quiverkey(q,0.9,0.9,0.1,"100 micron",coordinates="figure")
    plt.axis("equal")
    plt.xlabel("x wok (mm)")
    plt.ylabel("y wok (mm)")
    plt.title("Metrology Fiber Position Errors")
    # plt.show()

    plt.savefig("fig_4_a.png", dpi=250)


if __name__ == "__main__":
    plotDetections()
    plotNudgeCorrection()
    plotWokCorrections(refit=True)
    plotFiberPositionError()