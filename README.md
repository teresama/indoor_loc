# Indoor Localization App

Configure your phone to detect in which room of a mapped space you are located. 

The map corresponds to a campus building with a long corridor.

![alt text](https://github.com/teresama/indoor_loc/blob/master/image.jpg?raw=true)

## Choose the android version

Change the android version under "bayes_localization/MyApplication2/app" in file "build.gradle"

## Data collection of your indoor map area

It is necessary to generate a file "MyFileRawGaus.txt" with the SSID list of WiFi stations in the indoor area to be mapped.
Check "map_file" directory to generate the same format of text file and once created needs to be added in the "Files/Downloads" of your Android device.

## Map of the area to get localized and working of app

By pressing the button FIND ME, the user is mapped onto the specific room that is supposedly in.

An image of the GUI of indoor_loc app can be found below:

![alt text](https://github.com/teresama/indoor_loc/blob/master/App2_Bayesian.jpeg?raw=true)
