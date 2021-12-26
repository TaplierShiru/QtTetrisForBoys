# QtTetrisForBoys

This repo is a simple Tetris application written with Qt framework in Python. 
The main purpose of this repo is to improve knowledge in Qt 
framework. I hope you find it useful for your future code experience!

## How to start

You have the following options in order to start use code/application in this repo:
1. Setup your python environment (see paragraph below) and run `main.py` script in `tetris_fb` folder;
2. Build .exe file from source for someone else (see paragraph below);
3. Download one of the latest release (.zip file) and execute `main.exe`;


## Setup for code

Update your python environment from `requirements.txt` file with following command:
```
pip install -r requirements.txt
```

Start script with
```
python tetris_fb/main.py
```


## How to build app from source
After configuration of python environment, in project folder type next command:
```
pyinstaller main.spec
```

You will create two folders: `build` and `dist`.
For production purposes (for users) use files in `dist` folder.

For more info you can explore `main.spec` file and official docs in PyInstaller. 

Hope my example can help you to understand PyInstaller better!
