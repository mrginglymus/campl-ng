# campl-ng

[![Build Status](https://travis-ci.org/mrginglymus/campl-ng.svg?branch=master)](https://travis-ci.org/mrginglymus/campl-ng)

## Build Requirements

* [Git LFS](https://git-lfs.github.com/) - to check out (included with recent windows git installs, possibly an extra package on linux)
* [Yarn](https://yarnpkg.com/) - to build and test (included with recent node installs (I believe), or available standalone on windows via choco)

## Install

```shell
$ yarn install
```

## Build Assets

```shell
$ yarn webpack --progress
```

This will output assets to `build/`. The production assets are `campl.js`, `campl.css`, plus everything in `fonts/` and `images/`.

## Demo site

The demo site can be built with

```shell
$ yarn build
```

This will output a static html site to the `build/` directory. This directory can be served however you like, or
by using

```shell
$ yarn serve
```
