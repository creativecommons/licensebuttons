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


## License


### Code / Scripts

- [`LICENSE`](LICENSE) (Expat/[MIT][mit] License)

[mit]: http://www.opensource.org/licenses/MIT "The MIT License | Open Source Initiative"


### Icons / Images

- The icons contained within this repository are for use under the Creative
  Commons Trademark Policy (see [Policies - Creative Commons][ccpolicies]).
- **The icons are not licensed under a Creative Commons license** (also see
  [Could I use a CC license to share my logo or trademark? - Frequently Asked
  Questions - Creative Commons][tmfaq]).

[ccpolicies]: https://creativecommons.org/policies
[tmfaq]: https://creativecommons.org/faq/#could-i-use-a-cc-license-to-share-my-logo-or-trademark
