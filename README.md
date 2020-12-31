# Indoor Localization App

Configure your phone to detect in which room of a mapped space you are located. 

The map corresponds to the corridor and rooms of an Electrical Engineering faculty building:

<img src="https://github.com/teresama/indoor_loc/blob/master/images/image.jpg?raw=true" width="130">

## Choose the right android version

Change the android version in [build.gradle](bayes_localization/MyApplication2/app/build.gradle). The current Android version used is 22.

## Data collection of your indoor map area

The file [MyFileRawGaus.txt](map_file/MyFileRawGaus.txt) was generated after performing a scan of all the existing WiFi routers (with its associated SSID) that could be reached in all the areas to be mapped in the app.

Consequently, it is required to generate a file with the SSID list of WiFi stations in the indoor area to be mapped.
Check therefore the example file [MyFileRawGaus.txt](map_file/MyFileRawGaus.txt) to generate the same format of text file.
In [dataProcessing_gaussian.py](python_processing/data_processing/dataProcessing_gaussian.py) the file "MyFileRawGaus.txt" is generated. Please note that the files under [measurementSMS](python_processing/measurementSMS) are the SSIDs scans performed per room. Therefore the SSIDs collected in those files CORRESPONDS to the corridor of the campus building. Modify with your own data.

Once created [MyFileRawGaus.txt](map_file/MyFileRawGaus.txt), it needs to be added in the "Files/Downloads" of your Android device since It is accessed in the app in here: [MainActivity.java](https://github.com/teresama/indoor_loc/blob/02684334bf182e2f329218ac7206efee3449f748/bayes_localization/MyApplication2/app/src/main/java/com/example/myapplication2/MainActivity.java#L110).

## Map of the area to get localized and working of app

By pressing the button FIND ME, the user is mapped onto the specific room that is supposedly in.

An image of the GUI of indoor_loc app can be found below:

<img src="https://github.com/teresama/indoor_loc/blob/master/images/App2_Bayesian.jpeg?raw=true" width="130">
