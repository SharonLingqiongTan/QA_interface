# March 6 change display first pre-annotation result to display search feature if in pre-annotation
# author: Sharon
import sys
import re

def extractFeature(inputString, query):
    query = query.strip()
    key_value = query.split(";")
    dic = {}
    if ";" in query:
        for el in key_value:  # get search features
            if el != "":
                pair = el.split(":")
                dic[pair[0]] = pair[1]

    # get name to display for snippet
    nameTagContent = inputString[inputString.index("<name>"):inputString.index("</name>")]
    name_to_display = ""
    if nameTagContent:
        names = nameTagContent.split(",")
        if "name" in dic and dic["name"] and dic["name"] in nameTagContent:
            name_to_display = dic["name"]
        else:
            name_to_display = names[0].strip("<name>name: ")

    # age
    ageTagContent = inputString[inputString.index("<age>"):inputString.index("</age>")]
    age_to_display = ""
    if ageTagContent:
        ages = ageTagContent.strip("<age>age:").split(",")
        if "age" in dic and dic["age"]:
            minAge = dic["age"][:2]
            maxAge = dic["age"][2:]
            # age_found = False
            for age in ages:
                if int(age) >= int(minAge) and int(age) <= int(maxAge):
                    # age_found = True
                    age_to_display = age
                    break
            # if age_found:
            #     age_to_display = minAge + " to " + maxAge
        if not age_to_display:
            age_to_display = ages[0]

    # phone
    phoneTagContent = inputString[inputString.index("<phone>"):inputString.index("</phone>")]
    phone_to_display = ""
    if phoneTagContent:
        phones = phoneTagContent.split(",")
        if "phone" in dic and dic["phone"] and dic["phone"] in phones:
            phone_to_display = dic["phone"]
        else:
            phone_to_display = phones[0].strip("<phone>phone:")

    # ethnicity / nationality
    ethnicityTagContent = inputString[inputString.index("<ethnicity>"):inputString.index("</ethnicity>")]
    ethnicity_to_display = ""
    if ethnicityTagContent:
        nationalities = ethnicityTagContent.split(",")
        if "nationality" in dic and dic["nationality"] and dic["nationality"] in ethnicityTagContent:
            ethnicity_to_display = dic["nationality"]
        else:
            ethnicity_to_display = nationalities[0].strip("<ethnicity>ethnicity:")

    # location
    locationTagContent = inputString[inputString.index("<location>"):inputString.index("</location>")]
    location_to_display = ""
    if locationTagContent:
        locations = locationTagContent.split(",")
        if "state" in dic and dic["state"] and dic["state"] in locationTagContent:
            location_to_display = dic["state"]
            if "city" in dic and dic["city"] and dic["city"] in locationTagContent:
                location_to_display = dic["city"] + ", " + location_to_display
        else:
            location_to_display = locations[0].strip("<location>location:")

    # hair_color
    hairColorTagContent = inputString[inputString.index("<hair_color>"):inputString.index("</hair_color>")]
    hairColor_to_display = ""
    if hairColorTagContent:
        hairs = hairColorTagContent.split(",")
        if "hairColor" in dic and dic["hairColor"] and dic["hairColor"] in hairColorTagContent:
            hairColor_to_display = dic["hairColor"]
        else:
            hairColor_to_display = hairs[0].strip("<hair_color>hair_color:")

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
    f = open("output.txt") # read document content
    lines = f.readlines()
    f.close()

    f = open("structureQuerylog") # read current query
    logs = f.readlines()
    query = logs[-1]
    f.close()

    inputString = " ".join(lines)
    extractFeature(inputString, query)  # match query key word with doc pre-annotation
    extractImg(inputString)
