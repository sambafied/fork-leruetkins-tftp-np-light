# Sambafied static text-first profile sources — #863

Bounded PXEFORK-004/005 asset preparation, product authority 4915c495.
These new files are NON-DEPLOYED source templates and a static manifest. No
existing `boot/`, `public/`, configuration, runtime, product or donor source file
is changed. There is no production renderer, DHCP server, API or network readiness
claim. No loader, executable, kernel, initrd, image or OS provisioning recipe is
included. Templates offer only a text menu and return control; they cannot install
or select an operating system. Do not install or serve these files as-is.

## Profiles and publication requirements

- `bios-ipxe/menu.ipxe`: BIOS iPXE text menu. Requires separately reviewed,
  hashed and qualified published `loaders/bios/undionly.kpxe`; intended generated
  menu path is `menus/bios-ipxe.ipxe`.
- `bios-pxelinux/default.cfg` and `menu.txt`: BIOS PXELINUX plain DISPLAY/PROMPT
  configuration, not a graphical menu module. Requires separately reviewed,
  hashed and qualified `loaders/bios/pxelinux.0`; intended display path is
  `menus/bios-pxelinux.txt`. The generated configuration would need publication at
  the loader's separately qualified PXELINUX configuration lookup location.
- `uefi-x86_64-ipxe/menu.ipxe`: explicit UEFI x86_64 iPXE text profile. Requires
  separately reviewed, hashed and qualified `loaders/uefi-x86_64/ipxe.efi`;
  intended generated menu path is `menus/uefi-x86_64-ipxe.ipxe`.

These exact-case loader paths are declared requirements, not references to files
bundled here. Their source/build/license, content SHA-256 and protocol receipts
must be established before publication/selection. No placeholder checksum is
presented as a real artifact identity. The common declared future asset namespace
is `assets/sambafied`; no payload in it is selected. Manifest firmware and CPU
architecture are separate from `kernel`, whose selection is false and architecture
is null. Client firmware does not assert the PXE server compilation target.

## Fail-closed selection policy

`manifest.json` defines candidate requirements only: DHCP architecture 0 permits
BIOS iPXE by default or an explicit BIOS PXELINUX override; architecture 7 and 9
each permit only the explicit UEFI x86_64 iPXE profile. Architecture 7's EFI BC
code is not proof of x86_64 support: it requires its own exact loader/firmware
interoperability receipt. Architecture 9 qualification cannot qualify code 7 or
vice versa. There is no blanket non-BIOS fallback. Unknown/missing/unsupported
architecture, invalid override, missing qualification or mismatched loader path
must select no loader. All actual qualifications are `NOT_RUN`, so none of these
loader requirements is currently eligible for runtime selection.

The Python function `select_fixture` exercises this policy with synthetic receipt
keys only. It is not production admission or receipt verification. The coordinator
owns the Rust renderer, typed admission/validation and runtime integration. Future
implementation must bind receipts to the exact source/hash/config/client scenario,
preserve current BIOS iPXE/PXELINUX and supported UEFI behavior, and keep defaults
unchanged until reviewed. Current existing profiles/trees remain byte-for-byte
unchanged by this PR.

## Template contract

Known placeholders use `@@NAME@@` syntax. `PUBLIC_BASE_URL` must be a validated
HTTPS public origin with no credentials/path/query/fragment; `MENU_PATH` and
`ASSET_ROOT` are exact declared relative POSIX paths. Rendering must reject
unknown/unresolved placeholders, traversal, empty segments, spaces/newlines and
case mismatch. No donor variable, client expression, user label or URL is inserted
as executable script text. The public origin/asset root are display text here;
PXELINUX DISPLAY uses the declared menu path. There is no remote script chain.

The fixture renderer is used with a controlled synthetic origin and the declared
paths for tests; it is not a runtime implementation. The text contains no host,
credential, shell/config/reboot/power action, graphics requirement, kernel/initrd
launch or OS provisioning recipe. iPXE's `exit 0` returns control from the menu
script and does not prove exit to firmware in every calling context. PXELINUX's
`LOCALBOOT -1` expresses return control; firmware behavior remains unqualified.
Neither menu is an authentication control or central management application.

## Provenance and notices

`NOTICE` describes adaptation and changed files. The old MIT TFTP-NP menu at
`b0aeaa128c16d70a29ccbba841ff9dcfbdaa53fc:public/menu.ejs` and Apache-2.0 PXE-NP
menu at `1b6be33569b47972bf939a2a332b0c533fd2cccf:public/menu.txt` inspired the
minimal menu/item/choose/exit expressions and English return labels. Their full
MIT/Apache notices are retained in `notices/`. New source uses Sambafied English
text, strips all boot recipes, graphics and shutdown/configuration commands, and adds
safe declared placeholders. The PXELINUX source is newly authored. The separate
exact-byte donor references remain intact; this does not relicense bundled
third-party payloads because none are included.

## Verification and limits

Run `python3 profiles/sambafied/verify.py`. It renders four controlled fixtures in
memory, checks known placeholders, ASCII English source, exact-case menu/asset
paths, safe origins, expected text-only commands and no executable/symlink files.
Negative cases cover path traversal/case changes, unknown placeholders, unsafe
origins, unsupported architectures, missing receipts, mismatched loader paths
and cross-code qualification reuse. Original historical and donor source
verifiers must continue to pass. A scoped Git diff against the fresh integration
base `142f91e402269d5893e06cee5243ce8150dfaac9` must list only
`profiles/sambafied/` changes, preserving existing trees.

Tests establish static template/policy consistency only. NOT_RUN: actual iPXE/
PXELINUX parser or firmware execution, rendering by Rust, published assets or
hash admission, BIOS/UEFI transfer/network fixtures, default profile compatibility,
PXE protocol runtime, OS provisioning and graphical UI/theme acceptance. #855's
source gate remains separate. Keep the review branch/worktree until the coordinator
lands or explicitly preserves it; no merge, promotion or release is authorized by
this source preparation slice.
