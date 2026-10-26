# Historical admin UI reference — #863

PXEFORK-001/002 source recovery only, against product authority 4915c495.
These files are non-deployed reference material. Do not mount this directory at
`/app/public`, render its EJS, import its scripts into the React app, or execute its
menu text. No server handlers, Rust protocol engine, loader, executable, launch
script or second administration service is recovered here. Existing current-base
files outside this directory are unchanged.

## Provenance and custody

Exact source: leruetkins/tftp-np-light commit
`b0aeaa128c16d70a29ccbba841ff9dcfbdaa53fc` (2024-07-04), retained in this fork's
history. `manifest.json` records every original path, byte count, Git blob ID and
SHA-256; `source/LICENSE` preserves the MIT notice, copyright 2023 leruetkins.
The selected EJS includes the original inline Vue application. Third-party Vue,
Tailwind, SweetAlert and Calamansi distributions, images, fonts, boot payloads and
helper scripts are intentionally excluded. Their historical URL references remain
for fidelity; this is not a runnable bundle. Repository-level license attribution
does not independently establish authorship of every upstream fragment.

The fork's upstream `main` at `0666a03c3c57b998b2efc4b1d1d6da9d2e386125`
was freshly confirmed before deliberately establishing missing `sambafied/main`
and `sambafied/develop` there. Upstream `main`, `beta` and seven tags were retained.
This work branches from `sambafied/develop`; no promotion or merge is implied.

## Backend inventory and centralized feature mapping

These are client-observed contracts, not recovered server implementations.

- `config.ejs:41-55,195`: POST `/api`, JSON `{method:"get_config"}`; expects JSON
  server/share entries with value and description. Map to typed React configuration
  forms through authenticated core `/api/v1/pxe`, using the PXE-004 config/status
  contract behind the core. Do not replicate the legacy method dispatcher.
- `config.ejs:280-286`: POST `/api`, multipart `method=update_config`, `data` JSON
  containing server/share sections. Map to validation preview and conditional apply;
  desired/applied revision and restart-required must stay visible. Legacy port
  redirect behavior is not proof of successful apply.
- `menu_editor.ejs:73-90`: POST `/api`, JSON `{method:"get_menu"}`, text response.
  Map to per-profile generated-menu preview via the authorized core facade.
- `menu_editor.ejs:109-124`: POST `/api`, multipart `method=update_menu`, `textFile`
  blob named `text.txt`. Map to validated per-profile preview/apply and immutable
  asset publication. Preserve revision/precondition checks; raw menu overwrite is
  not an approved new API.
- `console.ejs:195,260-270`: WebSocket `ws://${window.location.host}` (root path),
  outgoing JSON `{command: string}`, incoming JSON `.data` console lines; reconnect
  after 1000 ms on unclean close. Map useful activity/history to authorized
  status/audit views and explicitly supported actions. Arbitrary command execution
  and this unauthenticated plaintext socket are not authorized.
- `index.ejs`: homepage/news/version, donation/community links and navigation to
  `/`, `/files`, `/config`, `/menu_editor`, `/console`. EJS requires server-supplied
  variables. Map homepage to centralized dashboard/asset catalog; file operations
  use the existing authorized storage/publication APIs.
- `assets/js/index.js`: filter, keyboard navigation, uploads through dynamic
  `form.method/form.action`, and POST deletion to dynamic `form.action` plus encoded
  fields. The selected sources do not establish concrete file handler paths or
  backend security. Map to authorized asset staging, validation and publication.
- `menu.ejs`: iPXE template with server/path substitutions and boot recipes, retained
  as design reference only. Map to validated firmware/profile menu generation;
  external payload links and legacy locale choices are not reviewed deployment assets.

Product authority: `docs/specs/service-stack-extension.md` at 4915c495,
PXEFORK-002/004, PXE-004 and ADMIN-001..003. These mappings are implementation work
for #858, not a claim those centralized endpoints/screens have shipped. Browser
clients must use ZITADEL/Cedar-authenticated core API, never PXE IPC directly.

## Source gate evidence (#855)

Fresh `git fetch origin` on 2026-10-26; repository is not shallow. All 185 available
commits reachable from local/remote branches and tags were inspected via
`git rev-list --objects --all`. No path matching Cargo.toml, Cargo.lock or `.rs`
(case insensitive) exists in that reachable object inventory. This establishes
absence in the available history only, not private/deleted/unreachable upstream
source. Server handlers and newer screenshot GUI source remain unavailable.
Opaque existing binaries cannot establish a rebuildable Rust source gate.

## Verification

Run `python3 references/admin-ui-2024/verify.py` from the repository root. The
read-only verifier checks the exact selected file set, sizes, SHA-256, original
Git blob bytes and non-executable modes, and rejects extra recovered payloads.
No browser, server, command socket, network listener or legacy script was run.
