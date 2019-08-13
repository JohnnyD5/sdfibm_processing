## Steps to auto download files to local machine
1. Use winscp to go to the selected folder
2. make a download folder under such folder
```
mkdir download
```
![pic1](pic1.png)
3. go to `download` folder and make all subfolders by running the python file
```
cd download
python mkdir_cases.py
```
*Note*: Need to make changes to the python file for the subfolder parameters

4. go back to the big folder
```
cd ..
python download_cases.py
```
*Note*: Need to make changes to the python file for the subfolder parameters

5. download everything in `download` folder to local folder
