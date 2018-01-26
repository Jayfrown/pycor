# pycor
python2 rewrite of [Container/Overlay](https://github.com/Jayfrown/container-overlay).

&nbsp;

## What?
It leverages [OverlayFS](https://wiki.archlinux.org/index.php/Overlay_filesystem) under unprivileged [LXD](https://linuxcontainers.org/lxd/introduction/) containers to share a single `r/o` rootfs. Containers write their changes (i.e. local packages, drop-in configuration, application data) to their respective `r/w` overlay directories.

It can be useful in a development environment where resources are scarce. OverlayFS inherently saves diskspace, but also saves memory usage and disk I/O by utilizing the Linux [Page Cache](https://en.wikipedia.org/wiki/Page_cache), essentially providing a single cached operating system shared by all containers.

## Why?
I wrote it trying to simplify simulating a managed hosting environment.

It provides atomic centralized control over shared packages and configuration. Local configuration can usually be included as drop-in files written to `r/w` overlays, which allows configuration management with puppet, ansible, etc.

Instantly configure packages and middleware across all containers by configuring the `base` container, and remounting the overlays:
```bash
lxc start base
lxc shell base
  # update packages, run puppet, do whatever
lxc stop base

for overlay in $(awk '$1 == "overlay" {print $2}' /etc/mtab); do
  mount -o remount $overlay
done
```

## Performance
OverlayFS, as a mainline kernel-level overlay implementation, is very efficient in terms of performance. Containers reading a file from the `r/o` filesystem will result in one disk I/O operation, adding the file(s) to the Linux [Page Cache](https://en.wikipedia.org/wiki/Page_cache). Further `read()` calls will effectively read from RAM.

Processes across containers essentially reference a single cached operating system: binaries, shared libraries/objects, and default configuration can all be read from RAM. Local drop-in configuration can be maintained in individual `r/w` overlays and easily changed during runtime.

Containers suffer less I/O overhead since the operating system is mostly cached, reducing access to secondary storage. At scale, this significantly decreases IOPS on the storage cluster, adding another performance benefit.
