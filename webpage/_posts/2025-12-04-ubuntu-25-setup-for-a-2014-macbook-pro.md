---
layout: post
title: Ubuntu 25 setup for a 2014 Macbook Pro
date: 2025-12-04
---

Apple stopped providing OS updates for my old MacBook Pro (Retina, 13-inch, Mid 2014, Intel CPU) even though the hardware is good enough for common web and development tasks. Eventually Chrome stopped providing updates for the OS version too. Then Docker stopped providing updates for it. Even DuckDB (a Python module) stopped supporting it!

The install and setup was not always straightforward and some of the guides were outdated so I wanted to write it all down for anyone else trying this.

The effort has made software development much better on the machine, standardized with my other Ubuntu machine, and slightly improved ordinary things like web browsing.

### Freeing up space

I used Perplexity to help guide me through the diagnostic process in freeing up space, and to create a safe plan to test what was safe to delete. The biggest discovery was a whole partition from an old OS X update that I could delete.

### Trying and installing Ubuntu

The Mac is very picky about the USB drive. What worked:

- Formatting as MS‑DOS (FAT) with GUID Partition Map in Disk Utility (other formats run on my other computer were not recognized) [link](https://discourse.ubuntu.com/t/create-a-bootable-usb-stick-on-macos/14016)
- dd to flash the iso (steps below)
- Boot with Option held down and choose EFI Boot.

I followed [these steps](https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command/) to flash the ISO:

```shell
# 1) List disks and identify your USB (e.g., /dev/disk2)
/usr/sbin/diskutil list

# 2) Unmount the whole USB device (not just a partition)
/usr/sbin/diskutil unmountDisk /dev/diskN

# 3) Write the ISO to the raw device for speed (DANGER: correct N!)
sudo dd if=/path/to/ubuntu-desktop.iso of=/dev/rdiskN bs=1m

# 4) Ensure buffers are flushed, then eject
sync
/usr/sbin/diskutil eject /dev/diskN
```

The steps above were maybe the 4th attempt. In previous attempts, either the USB wasn't listed in the boot menu or else it was listed but booting from it would just hang on a black screen.

### Installing wifi drivers (Broadcom BCM4360)

Ubuntu doesn't come with wifi drivers for the Broadcom BCM4360 chip. So I ordered a cheap USB Ethernet adapter and used it to test Ubuntu then install the correct wifi chip drivers.

When installing Ubuntu I made sure to select additional drivers, which I think enabled the restricted package source containing the following drivers.

Then: `sudo apt install broadcom-sta-dkms` (Not the older `bcmwl-kernel-source`)

Then I rebooted and wifi worked!

### Installing webcam drivers (Broadcom FaceTime HD / 1570)

Even though the guides were quite old, they still worked for the webcam.

- Double-check the hardware model against the guide you're following. In my case `lspci -nn | grep 1570`
- Install prerequisites: `sudo apt install linux-headers-generic build-essential git curl cpio xz-utils`
- Install firmware: `git clone https://github.com/patjak/facetimehd-firmware.git && cd facetimehd-firmware && make && sudo make install`
- Install driver: `git clone https://github.com/patjak/bcwc_pcie.git && cd bcwc_pcie && make && sudo make install && sudo depmod`
- Load the driver: `sudo modprobe facetimehd` and I verified it in Google Meet in Chrome

Note that kernel updates will cause Ubuntu to lose the webcam and you'll need to do this again. I tried looking into [a DKMS package for it](https://gbatemp.net/threads/debian-ubuntu-facetimehd-webcam-driver.584652/), but the download link no longer works. I may search around for DKMS package in the future or make my own.

Sources:

- [link](https://andreafortuna.org/2024/08/24/from-faceless-to-facetime-installing-webcam-drivers-on-a-debian-powered-macbook-air)
- [link](https://gist.github.com/johnjeffers/3006011ec7767a4101cdd118e8d64290)

### Issue: Red light from the audio jack

Sometimes a red light would shine through the audio jack. To quote Perplexity,

> That red light shining through your MacBook's headphone jack is the optical digital audio (TOSLINK / S/PDIF) output, which shares the same jack as the analog output on older Mac models like the 2014 MacBook Pro. When the light turns on, it means the hardware has switched the port into optical mode.

Steps to resolve:

- Run `alsamixer`
- Press F6 to pick the sound card, navigate to S/PDIF, IEC958, or Digital Output channels, then press M to mute.
- Run `sudo alsactl store`

I haven't had problems since.

### Improving battery life

Short version: TLP works well without additional customization.

### TLP

[TLP](https://linrunner.de/tlp/index.html) is a popular all-in-one package to optimize battery life and it doesn't require customization.

```shell
sudo apt install tlp
sudo tlp start
```

I've found that battery life while sleeping seems better, and it's a little better during normal usage (compared to balanced power mode all the time).

I've only had one issue with TLP and that's when playing Youtube videos in Chrome (deb package) on battery. Sometimes it causes the video to stutter badly enough to nearly lock up the tab, and that didn't happen pre-TLP on Balanced power mode.

### Special note about Spotify

If you use Spotify via the deb package, be sure to minimize the window while playing music in the background. I found that the laptop was drawing 30–45W with Spotify playing in the background when not visible but not minimized, and only around 10W when minimized. This appears to be a common, old issue [1](https://community.spotify.com/t5/Desktop-Linux/High-CPU-usage-on-desktop-client/td-p/5264603), [2](https://github.com/flathub/com.spotify.Client/issues/223), [3](https://forum.garudalinux.org/t/spotify-high-gpu-usage/45648).

### Semi-failed: Low-effort wattage monitoring

Initially I wanted low-effort monitoring in the top bar. That led me to PowerTracker.

- Setup Gnome extensions and install PowerTracker [link](https://www.ubuntumint.com/powertracker-ubuntu-battery-life-monitor/)
- Manually edit `~/.local/share/gnome-shell/extensions/marcs14@gmail.com/metadata.json` to allow it in Gnome 49, then relogin. This isn't normally needed, but the extension hasn't been updated for Gnome 49 yet.

I used the machine for about a week on `balanced` power mode before installing TLP. Then after I installed TLP I also kept an eye on it. I wasn't able to notice major trends through PowerTracker like I'd hoped, even though the battery seemed to last longer. If I could do it again, I'd try a widget that smooths out the power usage more.

That said, it did help me discover the Spotify issue.

### Failed effort: Hardware video acceleration

I'm including this section to discourage others from wasting time on this.

This hardware has the Intel Iris 5100 chip and can do hardware acceleration of h264 video but not newer video codecs.

Initially I tried getting hardware video acceleration working in Chrome with the deb package but I wasn't able to get Chrome to use it. When I gave up, I had the feeling that it was possible but would take more time than I was willing to put in.

I pivoted and I was able to get it working in Firefox using the Flatpak package, but when I benchmarked Firefox with hardware video acceleration against Chrome without video acceleration, the battery usage was similar. The description below is what I did to get it working in Firefox in case it helps others.

Installing the driver: `sudo apt install vainfo libva-intel-driver`

Then I could confirm that it saw i965 with `vainfo`:

```shell
libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/i965_drv_video.so
libva info: Found init function __vaDriverInit_1_22
libva info: va_openDriver() returns 0
vainfo: VA-API version: 1.22 (libva 2.22.0)
vainfo: Driver version: Intel i965 driver for Intel(R) Haswell - 2.4.1
```

Firefox setup:

```shell
flatpak install flathub org.mozilla.firefox
flatpak run org.mozilla.firefox
```

Then run `flatpak info org.mozilla.firefox` and note the version number under runtime or SDK. In my case it's 24.08.

I also had to install these:

```shell
flatpak install flathub org.freedesktop.Platform.ffmpeg-full//VERSION
flatpak install flathub org.freedesktop.Platform.VAAPI.Intel//VERSION
```

If you don't specify the version, you can pick it from a list.

And because my hardware only accelerates h264, I installed the h264ify plugin to force Youtube to use h264 streams rather than VP9/AV1.

Older online guides said I'd need to edit Firefox settings but that's no longer needed.

`intel-gpu-top` is useful for confirming that it's working. To install: `sudo apt install intel-gpu-tools`. Then run the top command while playing a video and confirm that there's non-zero usage in the Video row: `sudo intel_gpu_top`

### Failed effort: Battery health saver

TLP has some pointers on how to set this up with Apple silicon (M chips) but not Intel. That said, I've noticed that it tends to stop at around 95% which is good enough for me.

### Failed effort: Wake speed

On OS X, my Macbook would wake from sleep in about 1 second. On Ubuntu, it takes maybe 10 seconds.

I can see the options here:

```shell
> cat /sys/power/mem_sleep
s2idle [deep]
```

Then changed it to s2idle: `echo s2idle | sudo tee /sys/power/mem_sleep`

Sadly that drained the battery overnight, so I'll just live with the slower waking for now.

If you're trying to get a few extra years out of this old hardware, I hope this helps!
