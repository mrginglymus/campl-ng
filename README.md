# campl-ng

[![Build Status](https://travis-ci.org/mrginglymus/campl-ng.svg?branch=master)](https://travis-ci.org/mrginglymus/campl-ng)

## Requirements

Python, with virtualenv

## Install

To install the dependencies, run make install. This will install (within a virtual environment) node and all the package dependencies

## Build

To build, you will need to enter the virtual environment with 

    $ source venv/bin/activate
    
Then you can run gulp

    $ gulp build

To cache images locally (takes about a minute) run

    $ gulp cache-images
