# r2plugin

This directory contains the make and meson files required to link r2ai
inside radare2 through the external plugin system (XPS).

```console
cd radare2
make -C libr/xps EXTERNAL_PLUGINS=r2ai
./configure-plugins
make
```

For meson builds, place this repository at `libr/xps/p/r2ai` and make
`libr/xps/p/meson.build` include:

```meson
subdir('r2ai/r2plugin')
```
