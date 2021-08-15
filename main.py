import sys
import pandas as pd
import os
from PIL import Image, ExifTags
import glob

def main():
    counter = 0
    exif_dict = {}
    gps_info = {}
    ext = getext()
    path = getpath()
    filelist = glob.glob(path + "*" + ext)
    writer = pd.ExcelWriter('export.xlsx', engine='xlsxwriter')
    for element in filelist:
        name = getname(counter, ext, path)
        worksheetname = name  #the name must not exceed the 31 chars
        im = Image.open(element)
        im_exif = im._getexif()
        counter += 1

        try:
            if im_exif is None:
                print("exif data not available")
            else:
                for key, val in im_exif.items():
                    if key in ExifTags.TAGS:
                        exif_dict[ExifTags.TAGS[key]] = val
                for key, val in exif_dict['GPSInfo'].items():
                    if key in ExifTags.GPSTAGS:
                        gps_info[ExifTags.GPSTAGS[key]] = val
                exif_dict.update(gps_info)
                exif_dict.pop("GPSInfo") #delete double GPSInfo tag

        except KeyError:
            print("Some exif tags might have been not found.")

        except:
            print("Ni dobro:", sys.exc_info()[0], "occurred.")
        df = pd.DataFrame(list(exif_dict.items()), columns=['Tags', 'Values'])
        df.to_excel(writer, index=False, sheet_name=worksheetname)
    writer.save()
    print("Exif tags exported successfully.")

def getname(count, ext, path):
    names = [os.path.basename(x) for x in glob.glob(path + "*" + ext)] #get the names from the file list
    n0 = str(names[count])
    if len(n0) > 31:
        n = n0[:31]
    else:
        n = n0
    return n

def getpath():
    try:
        path = input(str("Provide the path where you stored your photos: "))
        if path[-1] == "\\":
            pass
        elif path[-1] != "\\":
            path = path + "\\"

        if os.path.isdir(path):
            print(f"Path provided: {path}")
        else:
            print(f" '{path}' is not a valid path. The default path used is where this script is located.")
            path = os.path.abspath(os.path.dirname(__file__)) + "\\" #takes the directory where the script is located
    except:
        print("Ni dobro:", sys.exc_info()[0], "occurred.")
    return path

def getext():
    extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".tiff", ".riff", "jpg", "jpeg", "jpe", "jif", "jfif", "jfi", "tiff", "riff"] #compatible extensions, it's not elegant but it works
    ext = input("Provide the file extension of the photos ")
    if ext in extensions:
        if ext[0] == ".":
            print("")
        else:
            ext = "." + ext
    else:
        getext()
    return ext

if __name__ == '__main__':
    main()
