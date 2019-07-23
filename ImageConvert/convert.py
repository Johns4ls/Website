import pymysql
from PIL import Image, ExifTags
import os
Path = "C:/Users/johns/Google Drive/ProgrammingProjects/Python/Flask/static/"
db = pymysql.connect(host='127.0.0.1', port=3306, user='WebServer', password='Momrocks38', db='mydb',autocommit=True)
cur = db.cursor()
query = ("Select Receipt FROM tTransaction")
cur.execute(query)
Transaction = cur.fetchall()
for Transaction in Transaction:
    Path = "C:/Users/johns/Google Drive/ProgrammingProjects/Python/Flask/static/"
    if(Transaction[0] is not ''):
        Path = Path + Transaction[0]
        if os.path.exists(Path):
            image = Image.open(Path)
            if hasattr(image, '_getexif'):
                orientation = 0x0112
                exif = image._getexif()
                if exif is not None:
                    orientation = exif[orientation]
                    rotations = {
                        3: Image.ROTATE_180,
                        6: Image.ROTATE_270,
                        8: Image.ROTATE_90
                    }
                    if orientation in rotations:
                        image = image.transpose(rotations[orientation])
                        image.save(Path, "JPEG", optimize=True, quality=85)
                        print("image Saved!")