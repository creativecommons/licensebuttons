# licensebuttons

Creative Commons badges, license Buttons, etc. (<https://licensebuttons.net/>).


:warning: **Consolidation/Update in progress. This repository is in a state of
flux.**


## genicons.py

This is a script to generate Creative Commons icon badges in png format in a
variety of color schemes. These icons can then be served by a web server. It is
located at [`scripts/genicons.py`](scripts/genicons.py).


### Install

1. Assuming the repository is on Debian
2. Install required Python 2 packages:

    ```shell
    sudo apt-get install python-cairo python-gtk2
    ```

3. Install CC Icons font

    ```shell
    mkdir -p ~/.fonts
    ln -sf ${PWD}/www/cc-icons.ttf ~/.fonts/
    ```


### Usage

Execute with Python 2:

```shell
python genicons.py
```

This will generate the icons in the directory `www/i` directory.
