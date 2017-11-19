# pycor-cli
work-in-progress python rewrite/refactor of
[Container/Overlay](https://github.com/Jayfrown/container-overlay).

&nbsp;

## What it does
Leverage [OverlayFS](https://wiki.archlinux.org/index.php/Overlay_filesystem)
under [LXD](https://linuxcontainers.org/lxd/introduction/) operating system
containers to share a `r/o` rootfs, each container writing changes (i.e.
local configuration, application data) to its respective `r/w` overlay.

It can be useful in a development environment where resources are scarce, as
OverlayFS saves diskspace, but in operation also saves memory usage and disk
I/O, which ultimately means more containers on the same hardware.

Maybe it's stable enough for production scale workloads. Hasn't failed me yet!

&nbsp;

## How it works
OverlayFS, as a mainline kernel-level overlay implementation, is very efficient
in-memory. Containers reading a file from the `r/o` filesystem will result in
one disk I/O operation, adding the file(s) to the Linux Page Cache.

Processes across containers essentially reference a single cached operating
system: binaries, shared libraries/objects, etc. Like running application
containers without exposing the host operating system.

Containers suffer less I/O overhead as they don't need to read from their
respective rootfs located on seperate storage. Given enough host RAM, the
entire `r/o` operating system fits in the page cache.

&nbsp;

## Orchestration benefits
This allows for perfect centralized control over packages and their
global configuration. Local configuration can usually be included from files
written to `r/w` overlays - which could be puppet managed.

In terms of Apache HTTPd: `httpd.conf` resides in the `r/o` operating system,
while the included `vhost.conf` is puppet-managed per container.

upgrade/install/remove/configure packages and middleware across containers by
doing so on the `base` container, and remounting the overlays:
```bash
lxc start base
lxc shell base
  # update packages, run puppet, do whatever
lxc stop base

for overlay in $(awk '$1 == "overlay" {print $2}' /etc/mtab)
  mount -o remount $overlay
done
```
