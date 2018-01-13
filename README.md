# pycor-cli
work-in-progress python rewrite/refactor of [Container/Overlay](https://github.com/Jayfrown/container-overlay).

&nbsp;

## What?
Leverage [OverlayFS](https://wiki.archlinux.org/index.php/Overlay_filesystem) under unprivileged OS-level [LXD](https://linuxcontainers.org/lxd/introduction/) containers to share a `r/o` rootfs, each container writing changes (i.e. local packages, drop-in configuration, application data) to its respective `r/w` overlay.

It can be useful in a development environment where resources are scarce, as OverlayFS inherently saves diskspace, but also saves memory usage and disk I/O by sharing a single cached base OS, which ultimately allows more containers on the same hardware.

## Why?
Atomic centralized control over shared packages and configuration. Local configuration can usually be included as drop-in files written to `r/w` overlays, which allows configuration management with puppet, ansible, etc.

Instantly configure packages and middleware across all containers by configuring the `base` container, and remounting the overlays:
```bash
lxc start base
lxc shell base
  # update packages, run puppet, do whatever
lxc stop base

for overlay in $(awk '$1 == "overlay" {print $2}' /etc/mtab)
  mount -o remount $overlay
done
```

## Performance
OverlayFS, as a mainline kernel-level overlay implementation, is very efficient in terms of performance. Containers reading a file from the `r/o` filesystem will result in one disk I/O operation, adding the file(s) to the Linux [Page Cache](https://en.wikipedia.org/wiki/Page_cache). Further `read()` calls will effectively read from RAM.

Processes across containers essentially reference a single cached operating system: binaries, shared libraries/objects, and default configuration is first read from the `r/o` filesystem, and later from the Linux Page Cache. Local drop-in configuration can be maintained in individual `r/w` overlays and easily changed during runtime.

Containers suffer less I/O overhead since the operating system is mostly cached, reducing access to secondary storage. At scale, this significantly decreases disk I/O for the hypervisor, adding another performance benefit.
