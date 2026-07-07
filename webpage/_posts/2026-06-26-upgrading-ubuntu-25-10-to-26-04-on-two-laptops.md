---
layout: post
title: Upgrading Ubuntu 25.10 to 26.04 on two laptops
date: 2026-06-26
ai_disclosure: I jotted the notes down during the month after the upgrade, then drafted an outline, handed it to Claude for a first pass and some fact checking, then edited.
---

I run Ubuntu as my daily OS on two laptops, and I'm still new enough that I'm cautious about upgrades. When 26.04 LTS came out I went looking for other people's reviews (good or bad) to decide whether to jump in or hold off, and didn't find much either way. So that led me to share what's changed for me, for anyone weighing the same upgrade or just curious about Ubuntu as a daily driver.

Keep in mind that a fair amount of this is really about GNOME rather than Ubuntu: 25.10 shipped GNOME 49 and 26.04 ships GNOME 50, so about half of what I noticed is the desktop not the distro.

The two machines:

- A 2014 MacBook, nice and light for working at coffee shops (I wrote up [getting Ubuntu onto it]({% post_url 2025-12-04-ubuntu-25-setup-for-a-2014-macbook-pro %}) separately).
- A 2023 Dell XPS, a hand-me-down from a previous job that's faster and heavier, and I keep it docked to an external monitor.

### What got better

- **Side-by-side window tiling.** The Super+Left / Super+Right keybindings used to be flaky for me. Now they just work.
- **Per-monitor fractional scaling is more reliable.** This matters most on the Dell, because the laptop panel and the external monitor have very different DPI. At the same scale, one screen ends up either too hard to read or comically large. In 25.10 when I tried it, display changes would often glitch: a window might display on one monitor but take mouse clicks on the other, or its visible bounds wouldn't match its click bounds. That could happen when I got home from a coffee shop and docked. 26.04 isn't perfect; I still occasionally see the visible size not match the clickable size, but it's clearly better.
- **The Files app feels faster sometimes**, though not consistently.

*Update 7/7/2026: I haven't noticed any Bluetooth keyboard stutter, which would happen now and then on 25.10 and earlier.*

### What got worse

- **Automatic brightness is on by default and I find it distracting.** The dimming algorithm is less smooth and predictable compared to OS X or Windows, and it's enough to distract me while reading. I just turned it off:

```shell
gsettings set org.gnome.settings-daemon.plugins.power ambient-enabled false
```

- **The new Resources app lost battery history.** I've only tried using it once after the update, and ironically it was for a feature I needed: I thought I'd seen the battery drop abruptly but the history is gone in the new app.
- **I'm not a fan of the new boot spinner.** The design idea seems interesting, but the alignment looks off, so when I glance at it I'm not sure whether it's intentional or a glitch.

### Mixed feelings

- **Waking from deep sleep on the MacBook.** Right after the upgrade it was dramatically faster, from about 10 seconds down to about 1. Then a couple of weeks later it regressed. What fixed it was disabling Panel Self Refresh with a kernel boot parameter, though it may cost a little battery:

```shell
# add to GRUB_CMDLINE_LINUX_DEFAULT in /etc/default/grub, then sudo update-grub
i915.enable_psr=0
```

*Update 7/7/2026: It reverted back to slow-waking and I haven't investigated yet :(*

- **GNOME extensions get disabled on upgrade.** I now understand one of the common gripes about them: when GNOME bumps versions, extensions go dark until the author adds the new version to the extension's compatibility list.
- **Google Drive mounting in Files is gone.** GNOME 50 dropped it because the underlying library had been unmaintained for years. And if that's also part of why Files feels snappier now, I'll call it a fair trade.

In the end it's net positive for me: the scaling and tiling fixes alone made the Dell nicer to use every day. I did expect a touch more polish from an LTS release, though I'm new enough to Ubuntu that maybe that expectation is unrealistic. If you're weighing the same upgrade, I hope this helps.
