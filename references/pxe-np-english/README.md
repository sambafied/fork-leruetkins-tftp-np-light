# PXE-NP English/menu reference — #863

PXEFORK-003 bounded donor-source recovery, using product authority 4915c495.
This is non-deployed reference material, not a rendered or themed production
menu. Do not serve, render, chain, import into generated menus, or execute these
files. Only two menu/template text files and the exact donor license are copied.
No executable, loader, helper script, vendor bundle, image or OS payload is added.
Current product files and maintained-fork boot/public trees are untouched.

## Pin, license and ancestry

Fresh donor fetch on 2026-10-26 confirmed HEAD and origin/main at
`1b6be33569b47972bf939a2a332b0c533fd2cccf`. `manifest.json` records original paths,
byte counts, SHA-256 and Git blob IDs. `source/LICENSE` preserves the Apache-2.0
license; `NOTICE` records provenance and the retained Geralt template annotation.
There was no separate donor NOTICE at this pin. Its license appendix contains
unfilled sample copyright fields; no actual holder/date is inferred from them.

The maintained fork integration was freshly fetched after recovery PR1 merged:
`87d76ebd3b2cafbe7a04aa7efcd191ee584e2763`. This branch starts there. Both
repositories are non-shallow. With donor objects exposed read-only through Git's
alternate object directory, `git merge-base` between the maintained upstream pin
`0666a03c3c57b998b2efc4b1d1d6da9d2e386125` and the donor pin returned exit 1,
no output or error: no common ancestor in available history. Maintained root is
`3057980ef8cdb6d3af44f679bf773e48995fdf8f`; donor root is
`36248a6c003640753bf7996cf805f99078946d30`. This is a selective source copy with
provenance, not a Git merge or proof of independent authorship.

## Reviewed source and translation plan

Useful source features: English grouped antivirus/OS/disk menus, explicit failure
return/countdown, reload/navigation labels, and a small BIOS/EFI memory-test
selection template. Original bytes remain unchanged, including historical
whitespace, branding and incomplete translations. These translations are a plan
for a future reviewed renderer/profile implementation, not edits applied here.

- Donor `public/menu.txt` corresponds conceptually to the historical maintained
  `public/menu.ejs` and a future generated per-profile menu. Neither path is a
  production destination in this slice. The donor reload target `/public/menu.txt`
  needs the actual published menu URL; do not preserve that endpoint implicitly.
- Donor `public/boot/soft/...` references must become validated immutable asset IDs
  and generated, escaped URLs. Historical maintained paths use `boot/soft/...`;
  stripping `public/` blindly is unsafe. Confirm case and actual catalog membership.
- `app_name`/`app_version` map to approved display metadata (historical maintained
  `version`); `boot_mode` maps to explicit profile firmware metadata, never guessed
  CPU architecture. PXE-NP branding is retained here, not applied to Sambafied.
- `server_ip`/`port` and derived `url` map to the configured boot-payload origin;
  `http_path` maps to an authorized asset-relative path. Validate schemes, escaping
  and path containment rather than concatenate client input.
- `nfs_ip`/`nfs_export`/`nfs_path` and hard-coded `/pxe-np` roots map to separately
  qualified export settings, not core storage paths or automatically created shares.
- `ipxes_path` in the memory-test template maps to an immutable published asset
  directory. `${platform}` must become an explicit validated firmware profile;
  `${cls}`/`space`/`esc` are presentation helpers. No binaries are recovered.
- `default_item`/`target` map to validated menu item IDs; `net0/mac:hexhyp` and `ip`
  are client display settings. `lockscreen` is presentation only; it is not auth.
  Commented `${url_dav}` replacements depend on an excluded helper script and are
  not an approved path/credential mechanism.

## Unsafe or unqualified entries retained for inspection

Line numbers below refer to `source/public/menu.txt` unless specified otherwise.
All source recipes remain unqualified. This list highlights concrete hazards;
absence from this list does not qualify an entry or downloaded software.

- Lines 4–5, 34 and 76–82: disabled lockscreen, plaintext HTTP origin, fixed secret
  key prompt and exposed shell/config/reboot/power controls. No authorization claim.
- Lines 86–99: Strelec recipe refers to wimboot, EFI, Windows PE/BCD and a
  `network_dav.cmd` helper absent from this recovery; commented `irepl` substitutions
  are not a recovered server or loader API. Payload licensing/firmware not qualified.
- Lines 101–133, 167–186: hard-coded `/pxe-np` NFS exports; ESET has
  embedded sample `user=serva,pass=avres,rw`. These are inherited public recipe
  literals, not operator credentials. Do not reuse them. Dr.Web still sets Russian
  language/keyboard options despite English labels; Avira/Dr.Web request manual
  `sudo dhclient`, which is not a proven networking workflow.
- Lines 159–163: MiniOS hard-codes `http://192.168.0.245:5555/...`, kernel/initrd
  version strings, repeated `ip=dhcp`, and `apparmor=0 selinux=0`. Do not carry this
  recipe into generated profiles without an explicit reviewed policy and artifacts.
- Lines 188–203: Acronis paths use `public/boot/soft/acronis/...`, whereas donor
  tree readme directories are under `public/boot/soft/hdd/acronis/...`; Russian
  `lang=RU_ru` and unprovided data payloads remain unqualified.
- Lines 206–208: EaseUS uses case-sensitive `public/boot/soft/EaseUS`, whereas
  donor readme directory is `public/boot/soft/hdd/easeus`; `sanboot --drive 0x80`
  has platform/disk semantics requiring explicit qualification.
- Lines 234–252: warm reboot, poweroff, config, BIOS boot-order exit and reload
  are boot-client actions, not central administration API operations.
- Memory-test template lines 7, 17–28: `bios/efi` annotation plus a pcbios/else EFI
  branch does not establish supported UEFI architectures. References to
  `memtest64.bin`/`.efi` and the displayed 6.2 version are unqualified; binaries
  deliberately excluded. It defaults every non-pcbios platform to EFI, which must
  not become a guessed production loader policy.

English menu labels are design input for PXEFORK-004/005. Preserve existing BIOS
iPXE and PXELINUX profiles and explicit supported UEFI defaults when later
implementing them. This donor does not itself implement PXELINUX selection.
Central React configuration/preview/apply remains through authenticated core API;
no second admin UI or legacy API is introduced. Runtime and handlers remain behind
#855/PXE-001; this source recovery does not unblock protocol acceptance.

## Verification and retained custody

Run `python3 references/pxe-np-english/verify.py` from the repository root. It checks
exact selected paths, source pin, sizes, SHA-256, Git blob IDs and non-executable
regular files. It never executes or renders recovered content. The source matches
`git show <donor-pin>:<path>` in the freshly fetched donor checkout at import time.
The verifier can run without retaining that checkout. Authored files pass
whitespace checks; raw recovered text has upstream trailing whitespace deliberately
preserved for exact-byte provenance. No network boot, service, helper or source
script was run. Worktree/branch and original donor checkout remain retained for
review; no merge, promotion, runtime or release acceptance is claimed.
