# campl-ng

[![Build Status](https://travis-ci.org/mrginglymus/campl-ng.svg?branch=master)](https://travis-ci.org/mrginglymus/campl-ng)

## Requirements

Python, with virtualenv

## Install

To install the dependencies, run ``make install``. This will install (within a virtual environment) node and all the package dependencies

## Build

To build, you will need to enter the virtual environment with 

    $ source venv/bin/activate
    
Then you can run gulp

    (venv)$ gulp build

To cache images locally (takes about a minute) run with the option ``--cache-images`` i.e.

    (venv)$ gulp build --cache-images

To use photos rather than placeholder images (slow to load) run with the option ``--photo`` ie.

    (venv)$ gulp build --photo

If you want to build so you can deploy to a non-root location, run build with the option ``--root`` e.g.

    (venv) $ gulp build --root /campl-ng

To run a local webserver to view the demo site (default [localhost:8000](http://localhost:8000)) run

    (venv)$ gulp run

Specify port and host with ``--port <port>`` and ``--host <host>`` respectively

You can also run individual commands for each component, e.g. ``gulp css``, ``gulp js`` or ``gulp html``. ``html`` is the only command which takes note of the two optional arguments above.