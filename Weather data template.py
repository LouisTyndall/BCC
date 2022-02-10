import logging
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO)


def getDeviceData(gatewayNo, sensorNo, startTimestamp, stopTimestamp):
    """Queries the Vaisala WX Beacon API against a specific device and returns a Pandas dataframe of data."""
    #API documentation
    #https://www.vaisala.com/sites/default/files/documents/Vaisala-Wx-Beacon-XML-API-Reference-in-English-M212639EN.pdf

    url="https://wxbeacon.vaisala.com/api/xml"
    APIkey="" #k INSERT YOUR API KEY HERE
    maxCount=50000 #c

    #example URL of a working request
    #https://beacon.vaisala.com/api/xml?d=T1010653&k=c39b635bfdf840c29750acbb3b36b0e3&t0=2021-11-23T00:00:00&t1=2021-11-23T02:00:00&c=100

    #set up the paramters for the API request query
    params = {
        'd': gatewayNo,
        'k': APIkey,
        't0': startTimestamp,
        't1': stopTimestamp,
        'c': maxCount,
        's': sensorNo
    }
    
    #headers =  {"Content-Type":"application/x-www-form-urlencoded"}
    
    #send the request to the server
    request = requests.get(url, params=params) #, headers=headers)

    #check it returned a valid response
    if request.status_code == 200:
        logging.info('API request OK')
    else:
        logging.error('API request failed!')
        logging.error("Status code: " + str(request.status_code))
        logging.error("Reason: " + request.reason)
        quit()

    #read the returned XML into a Pandas dataframe
    dataframe = pd.read_xml(request.text, xpath=".//measurements/meas")
    #append the serial number of the device as an extra column in the dataframe. Useful when dataframes from different sites get merged.
    dataframe['device'] = gatewayNo
    dataframe['sensor'] = sensorNo

    #change the timestamp to a Pandas datetime
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])

    if len(dataframe.index) == maxCount:
        logging.error("Data requested exceeded maximum message request size (parameter c). There will be gaps in the data!")

    return dataframe


def getDataBatch(devices, startTimestamp, stopTimestamp):
    """Loops through the list of device serial numbers, calling the getDeviceData function for each one."""
    #The dataframe from each site will first be dumped into a list
    listOfDataFrames = []

    #Loop through all the serial numbers of all the devices we want data for
    for gatewayNo, sensorsList in devices.items():
        for sensorNo in sensorsList:
            #run the API request function and append each dataframe to the list.
            listOfDataFrames.append(getDeviceData(gatewayNo, sensorNo, startTimestamp, stopTimestamp))
    
    #Create a master dataframe from all the data in the list
    dataframe = pd.concat(listOfDataFrames, ignore_index=True)

    return dataframe

def main():
    """Retreives data as a Pandas Data Frame from the Vaisala web API for a list of devices and sensors on a specified time range"""
    #dictionary of devices, each containing a list of sensors
    devices = {
        "T3710616":["AQT530-T2820375"], #V97 air quality
        "T3740449":["WXT530-T2840153"], #V11 weather
        "T3730241":["WXT530-T3150938", "AQT530-T2350418"], #V5 weather and air quality
    }
    
    startTimestamp="2022-01-19T00:00:00" #Format is yyyy-mm-ddThh:mm:ss
    stopTimestamp="2022-01-20T12:00:00"

    df = getDataBatch(devices, startTimestamp, stopTimestamp)

    print("Available data types:")
    print(df.groupby(['type']).mean())
   
    print("done")

#Make this script executable
if __name__ == "__main__":
    main()
