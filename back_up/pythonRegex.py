import sys
import re

def extractFeature(inputString):
    #Only display the first candidate
    nameTagContent = inputString[inputString.index("<name>"):inputString.index("</name>")]
    name_to_display = ""
    if nameTagContent:
        name_to_display = nameTagContent.split(",")[0].strip("<name>name: ")

    ageTagContent = inputString[inputString.index("<age>"):inputString.index("</age>")]
    age_to_display = ""
    if ageTagContent:
        age_to_display = ageTagContent.split(",")[0].strip("<age>age: ")

    phoneTagContent = inputString[inputString.index("<phone>"):inputString.index("</phone>")]
    phone_to_display = ""
    if phoneTagContent:
        phone_to_display = phoneTagContent.split(",")[0].strip("<phone>phone: ")

    ethnicityTagContent = inputString[inputString.index("<ethnicity>"):inputString.index("</ethnicity>")]
    ethnicity_to_display = ""
    if ethnicityTagContent:
        ethnicity_to_display =  ethnicityTagContent.split(",")[0].strip("<ethnicity>ethnicity: ")

    locationTagContent = inputString[inputString.index("<location>"):inputString.index("</location>")]
    location_to_display = ""
    if locationTagContent:
        location_to_display = locationTagContent.split(",")[0].strip("<location>location: ")

    hairColorTagContent = inputString[inputString.index("<hair_color>"):inputString.index("</hair_color>")]
    hairColor_to_display = ""
    if hairColorTagContent:
        hairColor_to_display = hairColorTagContent.split(",")[0].strip("<hair_color>hair_color: ")

    result = [name_to_display,age_to_display,phone_to_display,ethnicity_to_display,location_to_display,hairColor_to_display]
    delimeter = "SharonDelimeter"
    print(delimeter.join(result)+delimeter)

def extractImg(inputString):
    imgTagPattern = r"<img.*?>"
    results = re.findall(imgTagPattern,inputString)
    imgResult = []
    for result in results:
        urlPattern = r"src=[\'\"](.*?)[\'\"]"
        src = re.findall(urlPattern,result)
        if src:
            imgResult.append(src[0])
    imgResult = imgResult[:3] #only show the first 3 images
    delimeter = "ImageDelimeter"
    if imgResult:
        print(delimeter.join(imgResult)+delimeter)

if __name__ == "__main__":
    f = open("output.txt")
    lines = f.readlines()
    f.close()
    inputString = " ".join(lines)
    extractFeature(inputString)
    extractImg(inputString)
