# Data Model

## HDU List

| No. |   Name | Type   |   Cards |  Dimensions |
| 0  |PRIMARY       | PrimaryHDU   |    6  | () |
|  1 | RAW           | CompImageHDU  |  164  | (6000, 6132) |
|  2 | POSITIONERTABLE    | BinTableHDU |    49 |  500R x 19C |
|  3 | WOKCOORDS     | BinTableHDU   |  47  | 561R x 18C   |
|  4 | FIDUCIALCOORDS    | BinTableHDU |    27 |  60R x 8C  |
|  5 | POSITIONERTABLEMEAS    |  BinTableHDU  |  197 |  500R x 93C |
|  6 | FIDUCIALCOORDSMEAS    | BinTableHDU  |  113 |  60R x 51C |
|  7 | FIBERDATA     | BinTableHDU   |  81  | 1500R x 35C |
|  8 | POSANGLES     | BinTableHDU   |  25  | 500R x 7C  |
|  9 | CENTROIDS     | BinTableHDU   |  85  | 558R x 37C |
| 10 | OFFSETS       | BinTableHDU   |  45  | 500R x 17C |

here lives the data model for proccessed fvc images.