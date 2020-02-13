# licensebuttons

Creative Commons badges, license Buttons, etc. (<https://licensebuttons.net/>).


:warning: **Consolidation/Update in progress. This repository is in a state of
flux.**


## genicons.py

This is a script to generate Creative Commons icon badges in png format in a
variety of color schemes. These icons can then be served by a web server.


### Install

```shell
sudo apt-get install python2.7 python-cairo python-gtk2
```

### Usage

```shell
python genicons.py
```

This will generate the icons in the directory "build" in the same directory as
the script.

The directory can then be moved into position using `mv`.
