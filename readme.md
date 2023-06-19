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


