# pycor-cli
###### disclaimer: this project is how I'm teaching myself python

work-in-progress python rewrite/refactor of [Container/Overlay](https://github.com/Jayfrown/container-overlay).

## What it does
Leverage [OverlayFS](https://wiki.archlinux.org/index.php/Overlay_filesystem)
under [LXD](https://linuxcontainers.org/lxd/introduction/) containers to share
a r/o rootfs, each container writing changes to its respective r/w overlay.

It can be useful in a development environment where resources are scarce, as an
overlay implementation saves on diskspace, but in operation it also saves on
memory usage and disk I/O.

## How it works
OverlayFS, as a kernel-level overlay implementation, is very efficient in-memory.
It eliminates storage duplicates on-disk as well as in page caches, so processes
across containers reference single cached copies of binaries, shared libraries,
etc.

## Who needs orchestration?
upgrade/install/remove/configure packages across containers by doing so on
the `base` container, and just remounting the overlays:
```bash
lxc start base
lxc shell base
  # update system, configure middleware, do whatever
lxc stop base

for overlay in $(awk '$1 == "overlay" {print $2}' /etc/mtab)
  mount -o remount $overlay
done
```
