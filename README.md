# licensebuttons

Creative Commons badges, license Buttons, etc. (<https://licensebuttons.net/>).


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


## Development


### Setup

Once this project's required dependencies (Docker, Git, etc.) are enabled on
your system, you will be able to run the legal-tools application and generate
static files.

For information on learning and installing the prerequisite technologies for 
this project, please see [Foundational technologies — Creative Commons Open
Source][found-tech].


### Docker

1. Build the containers.
    ```shell
    docker compose build
    ```
2. Run the containers.
    ```shell
    docker compose up
    ```
3. Generate icons in container
    ```shell
    ./dev/genicons.sh
    ```
4. Access NGINX site in web container: [127.0.0.1:8080](http://127.0.0.1:8080/)


## Style/Syntax

Github Actions check the style and syntax with [black][black] and
[flake8][flake8]. Run the following commands before submitting a pull request:
- Reformat with black using a maxiumum of 79 charaters per line:
    ```shell
    black -l 79 ./scripts/genicons.py
    ```
- Check syntax with flake8:
    ```shell
    flake8 ./scripts/genicons.py
    ```

[black]: https://github.com/python/black
[flake8]: https://gitlab.com/pycqa/flake8


### Dependencies

- *Pycairo is a Python module providing bindings for the cairo graphics
  library* ([Overview — Pycairo documentation][pycairo]).
- *PyGObject is a Python package which provides bindings for GObject based
  libraries such as GTK, GStreamer, WebKitGTK, GLib, GIO and many more*
  ([Overview — PyGObject][pygobject]).
- PangoCairo is used to load the system fonts and check if the "CC Icons" font
  is available. See [PangoCairo.FontMap - Interfaces -
  PangoCairo 1.0][pcfontmap].

[pycairo]: https://pycairo.readthedocs.io/en/latest/
[pygobject]: https://pygobject.readthedocs.io/en/latest/index.html
[pcfontmap]: https://lazka.github.io/pgi-docs/PangoCairo-1.0/classes/FontMap.html#PangoCairo.FontMap


## License


### CC Icons, Images, and Logos

- The icons, images, and logos contained within this repository are for use
  under the Creative Commons Trademark Policy (see [Policies - Creative
  Commons][ccpolicies]).
- **The icons, images, and logos are not licensed under a Creative Commons
  license** (also see [Could I use a CC license to share my logo or
  trademark? - Frequently Asked Questions - Creative Commons][tmfaq]).
- The [GLYPHICONS FREE](#glyphicons-free), below, are licensed separately.

[ccpolicies]: https://creativecommons.org/policies
[tmfaq]: https://creativecommons.org/faq/#could-i-use-a-cc-license-to-share-my-logo-or-trademark


### Code / Scripts

- [`LICENSE`](LICENSE) (Expat/[MIT][mit] License)

[mit]: http://www.opensource.org/licenses/MIT "The MIT License | Open Source Initiative"


### GLYPHICONS FREE

> #### GLYPHICONS FREE license for previous version 1.9.2
>
> are released under the [Creative Commons Attribution 3.0 Unported (CC BY
> 3.0)][cc-by-30]. The GLYPHICONS FREE can be used both commercially and for
> personal use, but you must always add a link to [GLYPHICONS.com][glyphicons]
> in a prominent place (e.g. the footer of a website), include the CC-BY
> license and the reference to [GLYPHICONS.com][glyphicons] on every page using
> icons.

([Previous version of GLYPHICONS sets v 1.9.2][old-free-license])

[cc-by-30]: https://creativecommons.org/licenses/by/3.0/ "Creative Commons — Attribution 3.0 Unported — CC BY 3.0"
[glyphicons]: https://glyphicons.com/ "Sharp and clean symbols - GLYPHICONS"
[old-free-license]: https://glyphicons.com/old/license.html#old-free-license "Previous version of GLYPHICONS sets v 1.9.2"
