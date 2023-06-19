# Data Model

## HDU List
Note: Generally FIDUCIALCOORDSMEAS and POSITIONERTABLEMEAS below will be the most interesting tables to look at.  They contain merged information from several other tables in the HDU List.  They contrain all centroid measurement data and fvc measurement data matched to specific robots or fiducials.

| No. |   Name | Type   |   Cards |  Dimensions | Description |
|---|---|---|---|---|---|
| 0  |PRIMARY       | PrimaryHDU   |    6  | () | N/A |
|  1 | RAW           | CompImageHDU  |  164  | (6000, 6132) | FVC image |
|  2 | POSITIONERTABLE    | BinTableHDU |    49 |  500R x 19C | positioner-specific calibration table (copied from fps_calibrations) |
|  3 | WOKCOORDS     | BinTableHDU   |  47  | 561R x 18C   | wok-specific calibration table (copied from fps_calibrations) |
|  4 | FIDUCIALCOORDS    | BinTableHDU |    27 |  60R x 8C  | fiducial-specific calibration table (copied from fps_calibrations)
|  5 | POSITIONERTABLEMEAS    |  BinTableHDU  |  197 |  500R x 93C | positioner-specific fvc measurements |
|  6 | FIDUCIALCOORDSMEAS    | BinTableHDU  |  113 |  60R x 51C | fiducial-specific fvc measurements |
|  7 | FIBERDATA     | BinTableHDU   |  81  | 1500R x 35C | unsure, used by jaeger? |
|  8 | POSANGLES     | BinTableHDU   |  25  | 500R x 7C  | positioner-commanded/reported alpha/beta angles |
|  9 | CENTROIDS     | BinTableHDU   |  85  | 558R x 37C | sep (source extractor) centroid detections and measurements |
| 10 | OFFSETS       | BinTableHDU   |  45  | 500R x 17C | unsure, used by jaeger? |

FIBERDATA and OFFSETS are tables used by jaeger for configuration building and fvc-looping.  They aren't described here.

POSITIONERTABLE, WOKCOORDS, and FIDUCIALCOORDS are copies of the tables included in the [fps_calibrations](https://www.github.com/sdss/fps_calibrations) product.  They describe things like where holes are located in the wok, the alpha/beta zeropoints and armlengths for each robot, the locations of science and metrology fibers for each robot, and the locations of the fiducials in the wok, etc.  They are copied into each FVC image for reprocessing purposes because the calibration files can change overtime (eg when robots are swapped, or when better robot calibrations are fit).

### POSANGLES Table
POSANGLES contains the commanded alpha/beta angles and the reported alpha/beta angles for each robot.  Column descriptions are:

| Column Name | Description |
|---|---|
|positionerID| unique id for robot |
| alphaReport | alpha angle as reported by robot encoders |
| betaReport | beta angle as reported by robot encoders |
| cmdAlpha | commanded alpha angle for robot |
| cmdBeta | commanded beta angle for robot |
| startAlpha | starting alpha position of robot before motion |
| startBeta | starting beta position of robot before motion|


### CENTROIDS Table
CENTROIDS is a table containing all the automatically detected and measured sources in the image.  The majority of the columns are described in the [sep](https://sep.readthedocs.io/en/v1.1.x/) documentation specifically the returned "objects" array [here](https://sep.readthedocs.io/en/v1.0.x/api/sep.extract.html).  Several extra columns are added to this table as part of FVC image processing: [x|y]Nudge, [x|y]Rot, [x|y]NudgeRot, and centroidID.  A **subset** of column descriptions are:

| Column Name | Description |
|---|---|
|npix| number of pixels contributing to centroid |
|x| x pixel location of centroid |
|y| y pixel location of centroid |
|x2| x 2nd moment of centroid (psf spread)|
|y2| y 2nd moment of centroid (psf spread)|
|peak| peak counts found in centroid |
|flux| total flux counted in centroid |
|xNudge| corrected x pixel location from nudge model|
|yNudge| corrected y pixel location from nudge model|
|xRot| x coordinate after rotating xy coordinates by instrument rotator angle (IPA) for centroid to robot/fiducial matching |
|yRot| y coordinate after rotating xy coordinates by instrument rotator angle (IPA) for centroid to robot/fiducial matching |
|xNudgeRot| x coordinate after rotating xyNudge coordinates by instrument rotator angle (IPA) for centroid to robot/fiducial matching |
|yNudgeRot| y coordinate after rotating xyNudge coordinates by instrument rotator angle (IPA) for centroid to robot/fiducial matching |
| centroidID | unique id for each detected centroid |

### FIDUCIALCOORDSMEAS Table
FIDUCIALCOORDSMEAS is a table merged from FIDUCIALCOORDS and CENTROIDS after matching was performed between CCD spots and specific fiducials.  In addition to the columns described in CENTROIDS, an additional **subset** of new columns are:

| Column Name | Description |
|---|---|
|xWok| the expected x wok location (mm) of the fiducial (CMM measured)|
|yWok| the expected y wok location (mm) of the fiducial (CMM measured)|
|xWokMeas| the FVC-measured x wok (mm) location of the fiducial after all fitting is performed|
|yWokMeas| the FVC-measured y wok (mm) location of the fiducial after all fitting is performed|
|wokErr| the distance between expected and FVC-measured location in wok coordinates (mm) |
|wokErrWarn| boolean value true if wokErr is greater than the max threshold for a valid match between a centroid and a fiducial (usually indicating a dead fiducial fiber) |

### POSITIONERTABLEMEAS Table
POSITIONERTABLEMEAS is a table merged from WOKCOORDS, POSITIONERTABLE, POSANGLES and CENTROIDS after matching was performed between CCD spots and specific fiducials.  Columns from all these tables are included, and an additional **subset** of new columns are:

| Column Name | Description |
|---|---|
|xWokReportMetrology| the expected x wok location (mm) of the metrology fiber given the robot's reported alpha/beta angles|
|yWokReportMetrology| the expected y wok location (mm) of the metrology fiber given the robot's reported alpha/beta angles|
|xWokMeasMetrology| FVC-measured x wok location (mm) of the metrology fiber after all fitting is performed|
|yWokMeasMetrology| FVC-measured y wok location (mm) of the metrology fiber after all fitting is performed|
|alphaMeas| robot's FVC-measured alpha angle derived from the FVC-measured location of the metrology fiber |
|betaMeas| robot's FVC-measured beta angle derived from the FVC-measured location of the metrology fiber |
|xWokAdjMetrology| static extra added distortion in x fit from dithers (only zbplus and zbplus2 at APO)|
|yWokAdjMetrology| static extra added distortion in y fit from dithers (only zbplus and zbplus2 at APO)|
|wokErrWarn| boolean. True if there was a problem matching this robot to a metrology fiber spot.  Likely indicating either a large robot motion error, centroid missmatch, or a dead fiber.|

## FITS Headers
Below is an example of the full table of headers for an FVC image:

|Name| Value | Comment|
|---|---|---|
XTENSION | 'IMAGE   '           | Image extension |
BITPIX   |                   16 | data type of original image |
NAXIS    |                    2 | dimension of original image |
NAXIS1   |                 6000 | length of original image axis |
NAXIS2   |                 6132 | length of original image axis |
PCOUNT   |                    0 | number of parameters |
GCOUNT   |                    1 | number of groups |
BSCALE   |                    1 | |
BZERO    |                32768 | |
EXTNAME  | 'RAW     '           | extension name |
CAMNAME  | 'fvc1n   '           | Camera name |
VCAM     | '0.6.0   '           | Version of the camera library |
IMAGETYP | 'object  '           | The image type of the file |
EXPTIME  |                  5.0 | Exposure time of single integration [s] |
EXPTIMEN |                  5.0 | Total exposure time [s] |
STACK    |                    1 | Number of stacked frames |
STACKFUN | 'median  '           | Function used for stacking |
TIMESYS  | 'TAI     '           | Time reference system |
SJD      |                60039 | SDSS custom Julian Day |
DATE-OBS | '2023-04-05 03:14:21.936606' | Time of the start of the exposure [TAI] |
CCDTEMP  |                -10.0 | Degrees C |
BEGX     |                 1000 | Window start pixel in X |
BEGY     |                    0 | Window start pixel in Y |
ENDX     |                 7000 | Window end pixel in X |
EDNY     |                 6132 | Window end pixel in Y |
BINX     |                    1 | Binning in X |
BINY     |                    1 | Binning in Y |
GAIN     |                 0.58 | The CCD gain [e-|ADUs] |
READNOIS |                 10.3 | The CCD read noise [ADUs] |
PIXELSC  |               0.2214 | Scale of unbinned pixel on sky [arcsec|pix] |
WCSAXES  |                    2 | Number of coordinate axes |
CRPIX1   |                  0.0 | Pixel coordinate of reference point |
CRPIX2   |                  0.0 | Pixel coordinate of reference point |
CDELT1   |                  1.0 | Coordinate increment at reference point |
CDELT2   |                  1.0 | Coordinate increment at reference point |
CRVAL1   |                  0.0 | Coordinate value at reference point |
CRVAL2   |                  0.0 | Coordinate value at reference point |
LATPOLE  |                 90.0 | [deg] Native latitude of celestial pole |
MJDREF   |                  0.0 | [d] MJD of fiducial time |
OBSERVAT | 'APO     '           | Observatory |
OBJSYS   | 'Mount   '           | The TCC objSys |
RA       | 'NaN     '           | Telescope is not tracking the sky |
DEC      | 'NaN     '           | Telescope is not tracking the sky |
RADEG    | 'NaN     '           | Telescope is not tracking the sky |
DECDEG   | 'NaN     '           | Telescope is not tracking the sky |
SPA      | 'NaN     '           | Telescope is not tracking the sky |
ROTTYPE  | 'Mount   '           | Rotator request type |
ROTPOS   |                285.0 | Rotator request type |
BOREOFFX |                  0.0 | TCC Boresight offset, deg |
BOREOFFY |                  0.0 | TCC Boresight offset, deg |
ARCOFFX  |                  0.0 | TCC ObjArcOff, deg |
ARCOFFY  |                  0.0 | TCC ObjArcOff, deg |
CALOFFX  |                  0.0 | TCC CalibOff, deg |
CALOFFY  |                  0.0 | TCC CalibOff, deg |
CALOFFR  |                  0.0 | TCC CalibOff, deg |
GUIDOFFX |                  0.0 | TCC GuideOff, deg |
GUIDOFFY |                  0.0 | TCC GuideOff, deg |
GUIDOFFR |                  0.0 | TCC GuideOff, deg |
AZ       |           121.000015 | Azimuth axis pos. (approx, deg) |
ALT      |    70.00001399999999 | Altitude axis pos. (approx, deg) |
IPA      |           285.000014 | Rotator axis pos. (approx, deg) |
CARTID   | 'FPS-N   '           | Cart ID |
CONFIGID |                 9326 | Configuration ID |
DESIGNID |               125094 | Design ID associated with CONFIGID |
FIELDID  |               103371 | Field ID associated with CONFIGID |
RAFIELD  |     115.680450284378 | Field right ascension |
DECFIELD |    -4.62992787101049 | Field declination |
FIELDPA  |            33.581146 | Field position angle |
BIASFILE | '' | Bias file associated with this image |
CHECKSUM | 'KInTMImQKImQKImQ'   | HDU checksum updated 2023-04-05T03:07:14 |
DATASUM  | '4233659729'         | data unit checksum updated 2023-04-05T03:07:14 |
FVCITER  |                    1 | FVC iteration |
FITRMS   |                41.66 | RMS full fit [um] |
PERC90   |                 57.8 | 90% percentile [um] |
FVCREACH |                  3.0 | Targets that have reached their goal [%] |
CAPPLIED |                    F | FVC correction applied |
TEMPRTD2 |                14.92 | Wok temperature 1 |
TEMPRTD3 |                14.82 | Wok temperature 2 |
TEMPT3   |    3.692434461500902 | Wok temperature 3 |
LED1     |                  0.0 | LED 1 power (half of metrology fibers) |
LED2     |                  0.0 | LED 2 power (other half of metrology fibers) |
LED3     |                  0.0 | Not hooked up |
LED4     |                  0.0 | Not hooked up |
FVC_NWRN |                    4 | number of robots out of measurement spec |
FVC_MAXD |                  0.5 | distance beyond to consider robot out of spec ( |
FVC_CNTT | 'zbplus2 '           | centroid type used for fitting |
FVC_BSIG |                  3.5 | above background sigma for centroid detection |
FVC_MNPX |                  100 | minimum number of pixels for a valid centroid |
FVC_WSIG |                  0.7 | sigma for winpos centroid algorithm |
FVC_WBSZ |                    3 | box size for winpos centroid algorithm (pix) |
FVC_SSIG |                    1 | sigma for simple centroid algorithm (pix) |
FVC_SPLM |                   19 | box size for simple centroid algorithm (pix) |
FVC_RMS  |    1.042388240483354 | robot rms (mm) |
FVC_FRMS |    2.544694308767215 | fiducial rms (mm) |
FVC_CRMS |    0.041561754568332 | in-spec (outlier-clipped) robot rms (mm) |
FVC_SCL  |   0.1214890517222512 | FVC model fit scale |
FVC_TRAX |     495.802071115937 | FVC model fit X translation |
FVC_TRAY |    144.2517686486808 | FVC model fit Y translation |
FVC_ROT  |    149.6960347447619 | FVC model fit rotation (deg) |
FVC_ZB0  | -0.00893343727010725 | zhao-burge transform coeff for polid 0 |
FVC_ZB1  | -0.00532919161722097 | zhao-burge transform coeff for polid 1 |
FVC_ZB2  | -0.00561282271966201 | zhao-burge transform coeff for polid 2 |
FVC_ZB3  | 9.71201433128561E-05 | zhao-burge transform coeff for polid 3 |
FVC_ZB4  | -6.0572064808234E-05 | zhao-burge transform coeff for polid 4 |
FVC_ZB5  | 2.59066252352451E-07 | zhao-burge transform coeff for polid 5 |
FVC_ZB6  | 2.11385570786903E-07 | zhao-burge transform coeff for polid 6 |
FVC_ZB7  | 2.91547800192162E-08 | zhao-burge transform coeff for polid 7 |
FVC_ZB8  | -1.4203634367774E-07 | zhao-burge transform coeff for polid 8 |
FVC_ZB9  | 1.44272672291423E-08 | zhao-burge transform coeff for polid 9 |
FVC_ZB10 | 1.61321128186530E-11 | zhao-burge transform coeff for polid 10 |
FVC_ZB11 | -8.3406857207855E-10 | zhao-burge transform coeff for polid 11 |
FVC_ZB12 | 4.33930660572635E-10 | zhao-burge transform coeff for polid 12 |
FVC_ZB13 | 5.12047259113167E-10 | zhao-burge transform coeff for polid 13 |
FVC_ZB14 | -3.6448576384583E-13 | zhao-burge transform coeff for polid 14 |
FVC_ZB15 | -5.2993457761797E-13 | zhao-burge transform coeff for polid 15 |
FVC_ZB16 | 2.38226583439239E-13 | zhao-burge transform coeff for polid 16 |
FVC_ZB17 | -1.7234171481147E-13 | zhao-burge transform coeff for polid 17 |
FVC_ZB18 | -3.2474603477061E-14 | zhao-burge transform coeff for polid 18 |
FVC_ZB19 | -5.8815833459830E-14 | zhao-burge transform coeff for polid 19 |
FVC_ZB20 | 7.62127409031418E-15 | zhao-burge transform coeff for polid 20 |
FVC_ZB21 | 1.26724688995419E-15 | zhao-burge transform coeff for polid 21 |
FVC_ZB22 | 3.96557058649114E-17 | zhao-burge transform coeff for polid 22 |
FVC_ZB23 | -1.7418117424674E-15 | zhao-burge transform coeff for polid 23 |
FVC_ZB24 | -1.0647751725829E-15 | zhao-burge transform coeff for polid 24 |
FVC_ZB25 | 2.04352662462059E-17 | zhao-burge transform coeff for polid 25 |
FVC_ZB26 | -8.0590620827682E-17 | zhao-burge transform coeff for polid 26 |
FVC_ZB27 | -2.7283244076139E-06 | zhao-burge transform coeff for polid 27 |
FVC_ZB28 | 3.48234677777306E-08 | zhao-burge transform coeff for polid 28 |
FVC_ZB29 | -5.6662283478954E-08 | zhao-burge transform coeff for polid 29 |
FVC_ZB30 | 6.66041529502092E-12 | zhao-burge transform coeff for polid 30 |
FVC_ZB31 | 2.68110119175206E-11 | zhao-burge transform coeff for polid 31 |
FVC_ZB32 | 1.34326827315788E-10 | zhao-burge transform coeff for polid 32 |
