# licensebuttons

Creative Commons badges, license Buttons, etc. (<https://licensebuttons.net/>).


:warning: **Consolidation/Update in progress. This repository is in a state of
flux.**


## Code of Conduct

[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md):

> The Creative Commons team is committed to fostering a welcoming community.
> This project and all other Creative Commons open source projects are governed
> by our [Code of Conduct][code_of_conduct]. Please report unacceptable
> behavior to [conduct@creativecommons.org](mailto:conduct@creativecommons.org)
> per our [reporting guidelines][reporting_guide].

[code_of_conduct]: https://opensource.creativecommons.org/community/code-of-conduct/
[reporting_guide]: https://opensource.creativecommons.org/community/code-of-conduct/enforcement/


## Contributing

We welcome contributions for bug fixes, enhancement and documentation. Please
follow [`CONTRIBUTING.md`](CONTRIBUTING.md) while contributing.


## genicons.py

This is a script to generate Creative Commons icon badges in png format in a
variety of color schemes. These icons can then be served by a web server. It is
located at [`scripts/genicons.py`](scripts/genicons.py).


### Install

1. Assuming the repository is on Debian
2. Install Python 3 and required Python 3 packages:

    ```shell
    sudo apt-get install gir1.2-pango-1.0 python3-gi-cairo
    ```

3. Install CC Icons font

    ```shell
    mkdir -p ~/.fonts
    ln -sf ${PWD}/www/cc-icons.ttf ~/.fonts/
    ```


### Usage

Execute with Python 3:

```shell
python3 scripts/genicons.py
```

This will generate the icons in the directory `www/i` directory.


### Development

- Style/Syntax
  - Github Actions check the style and syntax with [black][black] and
    [flake8][flake8]. Run the following commands before submitting a pull
    request:
    - Reformat with black using a maxiumum of 79 charaters per line:
        ```shell
        black -l 79 ./scripts/genicons.py
        ```
    - Check syntax with flake8:
        ```shell
        flake8 ./scripts/genicons.p
        ```
- Dependencies
  - *Pycairo is a Python module providing bindings for the cairo graphics
    library* ([Overview — Pycairo documentation][pycairo]).
  - *PyGObject is a Python package which provides bindings for GObject based
    libraries such as GTK, GStreamer, WebKitGTK, GLib, GIO and many more*
    ([Overview — PyGObject][pygobject]).
  - PangoCairo is used to load the system fonts and check if the "CC Icons" font
    is available. See [PangoCairo.FontMap - Interfaces -
    PangoCairo 1.0][pcfontmap].

[black]: https://github.com/python/black
[flake8]: https://gitlab.com/pycqa/flake8
[pycairo]: https://pycairo.readthedocs.io/en/latest/
[pygobject]: https://pygobject.readthedocs.io/en/latest/index.html
[pcfontmap]: https://lazka.github.io/pgi-docs/PangoCairo-1.0/classes/FontMap.html#PangoCairo.FontMap


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
