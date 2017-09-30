# pycor-cli
### container/overlay rewrite in python
###### disclaimer: this project is how I'm teaching myself python

Tracking a work-in-progress python rewrite of [Container/Overlay](https://github.com/Jayfrown/container-overlay).
It leverages [OverlayFS](https://wiki.archlinux.org/index.php/Overlay_filesystem) under
[LXD](https://linuxcontainers.org/lxd/introduction/) containers to share a single r/o base system,
each container writing changes to its respective r/w overlay.


OverlayFS is a kernel-level overlay filesystem which is very efficient in-memory.
Containers already share a kernel, and now they can share a base system as well.
OverlayFS eliminates storage duplicates on-disk as well as in page caches,
so binaries across containers will reference single cached copies of shared libraries, etc.


Configured correctly, you can upgrade packages across all containers by simply
upgrading packages in the `base` container, and remounting the overlays:
```bash
/usr/bin/lxc start base
/usr/bin/lxc exec base "yum -y update"
/usr/bin/lxc stop base

for overlay in $(awk '$1 == "overlay" {print $2}' /etc/mtab)
  mount -o remount $overlay
done
```
