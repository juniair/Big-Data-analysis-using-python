import csv
import datetime as dt
from operator import itemgetter
from functools import reduce
import re

def GetKeyDict(args = []):
    return {x: True for x in args}

def IsAnyKey(target = {}, *args):
    isFind = False
    for arg in args:
        if target.get(arg):
            isFind = True
            break
        pass
    return isFind


def MakeData():
    csvFile = open("large_bike.csv", "r", encoding='utf-8')
    csvReader = csv.DictReader(csvFile, skipinitialspace=True)
    headers = csvReader.fieldnames
    keyDict = GetKeyDict(headers)
    
    items = {}
    cnt = 0
    for row in csvReader:

        # location
        location = row["location"]

        # casual
        casual = row["casual"]
        
        # registered
        registered = row["registered"]
        
        # datetime
        datetime = row["datetime"]
        
        # Data value equal header name check.
        if IsAnyKey(keyDict, location, casual, registered, datetime):
            continue

        if type(casual) is str:
            casual = int(casual)

        if type(registered) is str:
            registered = int(registered)

        # Convert datetime string to date string 
        date = re.sub(" \d{1,2}:\d{1,2}", "", datetime)
        
        # item setting
        
        if not items.get(location): # New item init
            items[location] = []
        
        item = items[location]

        dateInfo = next((x for x in item if x["date"] == date), {})
            
        if not bool(dateInfo):
            dateInfo["date"] = date
            dateInfo["casual"] = [0]
            dateInfo["registered"] = [0]
            item.append(dateInfo)

        dateInfo["casual"].append(casual)
        dateInfo["registered"].append(registered)

        if date == '2011-01-02':
            cnt = cnt + 1


    
    csvFile.close()

    for key in items:
        sortedItem = sorted(items[key], key=itemgetter("date"))
        items[key] = sortedItem

    return items

def searchLocation(location, items):
    if not items.get(location) or len(items[location]) <= 0:
        return False
    
    dateInfoList = items[location]

    for dateInfo in dateInfoList:
        casualSum = reduce(lambda x, y : x + y, dateInfo["casual"])
        registeredSum =  reduce(lambda x, y : x + y, dateInfo["registered"])
        printString = '{date}: casual: {casual}, registered:{registered}'.format(date = dateInfo["date"], casual = casualSum, registered = registeredSum)
        print(printString)

    return True

def diffenceLocation(location, date, items):
    if not items.get(location) or len(items[location]) <= 0:
        return False
    
    targetDateInfoList = items[location]
    targetDateInfo = next((x for x in targetDateInfoList if x["date"] == date), {})

    if not bool(targetDateInfo):
        return False

    targetCasualSum = reduce(lambda x, y : x + y, targetDateInfo["casual"])
    targetRegisteredSum = reduce(lambda x, y : x + y, targetDateInfo["registered"])


    otherItems = {key: value for key, value in items.items() if key != location}
    for otherLocation, otherItem in otherItems.items():

        # 데이터가 조회 안될때 차이도 확인 하고 싶을시 아래 주석 제거
        # otherDateInfo = next((x for x in otherItem if x["date"] == date), {"casual" : [0], "registered": [0]})


        # 데이터가 조회 안될때 차이도 확인 하고 싶을시 아래 주석 추가
        otherDateInfo = next((x for x in otherItem if x["date"] == date), {"casual" : [0], "registered": [0]})

        # 데이터가 조회 안될때 차이도 확인 하고 싶을시 아래 주석 추가
        if not bool(otherDateInfo):
            continue

        otherCasualSum = reduce(lambda x, y : x + y, otherDateInfo["casual"])
        otherRegisteredSum = reduce(lambda x, y : x + y, otherDateInfo["registered"])

        diffrenceCasualSum = targetCasualSum - otherCasualSum
        diffrenceRegisteredSum = targetRegisteredSum - otherRegisteredSum
        
        printString = "{other} 대비: casual: {casual}, registered: {registered}".format(other = otherLocation, casual = diffrenceCasualSum, registered = diffrenceRegisteredSum)
        print(printString)

    return True




def getCommands(args):
    commands = [None, None]
    for index in range(len(args)):
        commands[index] = args[index]
    return (commands, len(args))

def main():
    isRunning = True
   
    while isRunning:
        items = MakeData()
        try:
            argv, argc = getCommands(input("input : ").split())

            if argc == 1:
                location = argv[0]
                isRunning = searchLocation(location, items)
            elif argc == 2:
                location = argv[0]
                date = argv[1]
                isRunning = diffenceLocation(location, date, items)
            else:
                isRunning = False
            
        except ValueError as e:
            isRunning = False
    return 0


if __name__ == "__main__":
    main()