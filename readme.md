# Data Model

## HDU List

| No. |   Name | Type   |   Cards |  Dimensions | Description |
|---|---|---|---|---|
| 0  |PRIMARY       | PrimaryHDU   |    6  | () | N/A |
|  1 | RAW           | CompImageHDU  |  164  | (6000, 6132) | FVC image |
|  2 | POSITIONERTABLE    | BinTableHDU |    49 |  500R x 19C | positioner-specific calibration table (copied from fps_calibrations) |
|  3 | WOKCOORDS     | BinTableHDU   |  47  | 561R x 18C   | wok-specific calibration table (copied from fps_calibrations) |
|  4 | FIDUCIALCOORDS    | BinTableHDU |    27 |  60R x 8C  | fiducial-specific calibration table (copied from fps_calibrations)
|  5 | POSITIONERTABLEMEAS    |  BinTableHDU  |  197 |  500R x 93C | positioner-specific fvc measurements |
|  6 | FIDUCIALCOORDSMEAS    | BinTableHDU  |  113 |  60R x 51C | fiducial-specific fvc measurements |
|  7 | FIBERDATA     | BinTableHDU   |  81  | 1500R x 35C | unsure |
|  8 | POSANGLES     | BinTableHDU   |  25  | 500R x 7C  | positioner-commanded/reported alpha/beta angles |
|  9 | CENTROIDS     | BinTableHDU   |  85  | 558R x 37C | source extractor centroid detections and measurements |
| 10 | OFFSETS       | BinTableHDU   |  45  | 500R x 17C | unsure |

here lives the data model for proccessed fvc images.