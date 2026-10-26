"""Offline controlled-fixture checks only; no runtime renderer or DHCP implementation."""
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r'@@([A-Z_]+)@@')


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def safe_path(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]*', value), 'unsafe path')
    require(all(part not in ('', '.', '..') for part in value.split('/')), 'unsafe path')


def render_fixture(source, values, profile):
    require(set(values) == {'PUBLIC_BASE_URL', 'MENU_PATH', 'ASSET_ROOT'}, 'unknown/missing placeholder')
    origin = urlsplit(values['PUBLIC_BASE_URL'])
    require(origin.scheme == 'https' and origin.hostname and not origin.username and not origin.password,
            'unsafe public origin')
    require(not origin.path and not origin.query and not origin.fragment and
            re.fullmatch(r'https://[A-Za-z0-9.-]+(?::[0-9]+)?', values['PUBLIC_BASE_URL']), 'unsafe public origin')
    for key, field in [('MENU_PATH', 'menu_path'), ('ASSET_ROOT', 'asset_root')]:
        safe_path(values[key])
        require(values[key] == profile[field], 'path case/catalog mismatch')
    require(set(TOKEN.findall(source)) <= set(values), 'unknown template placeholder')
    result = TOKEN.sub(lambda match: values[match[1]], source)
    require('@@' not in result and '${' not in result, 'unresolved template expression')
    require(result.isascii(), 'non-English fixture text')
    return result


def select_fixture(manifest, arch, receipts, override=None):
    """Exercise declared policy with synthetic receipts; never offer a real loader."""
    policy = manifest['dhcp_architecture_policy'].get(arch)
    if policy is None:
        return None
    profile = override or policy['default_profile']
    if profile not in policy['allowed_profiles']:
        return None
    selected = next(p for p in manifest['profiles'] if p['id'] == profile)
    asset = selected['loader']['required_asset_path']
    return asset if (arch, profile, asset) in receipts else None


def rejected(action):
    try:
        action()
    except ValueError:
        return
    raise AssertionError('invalid fixture accepted')


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    repo = ROOT.parents[1]
    require((ROOT / 'notices/MIT.txt').read_bytes() == (repo / 'references/admin-ui-2024/source/LICENSE').read_bytes(), 'MIT notice changed')
    require((ROOT / 'notices/Apache-2.0.txt').read_bytes() == (repo / 'references/pxe-np-english/source/LICENSE').read_bytes(), 'Apache notice changed')
    require(manifest['status'] == 'STATIC_REFERENCE_ONLY', 'unexpected status')
    require(set(manifest['dhcp_architecture_policy']) == {'0', '7', '9'}, 'architecture policy changed')
    require(manifest['unknown_architecture'] == manifest['missing_qualification'] == 'NO_LOADER', 'unsafe fallback')
    expected_templates = {'bios-ipxe/menu.ipxe', 'bios-pxelinux/default.cfg',
                          'bios-pxelinux/menu.txt', 'uefi-x86_64-ipxe/menu.ipxe'}
    require({p for profile in manifest['profiles'] for p in profile['templates']} == expected_templates,
            'template set mismatch')
    require({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.suffix in ('.ipxe', '.cfg') or p.name == 'menu.txt'}
            == expected_templates, 'extra menu source')
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'symlink in static profile')
        if path.is_file():
            require(not path.stat().st_mode & 0o111, 'executable static profile file')
    rendered = 0
    for profile in manifest['profiles']:
        safe_path(profile['loader']['required_asset_path'])
        require(profile['loader']['qualification'] == 'NOT_RUN' and not profile['loader']['bundled'], 'false qualification')
        require(profile['kernel'] == {'architecture': None, 'required_assets': [], 'selected': False}, 'unexpected kernel recipe')
        if profile['firmware'] == 'uefi':
            require(profile['cpu_architecture'] == 'x86_64', 'unsupported UEFI profile')
        else:
            require(profile['firmware'] == 'bios', 'unsupported firmware')
        values = {'PUBLIC_BASE_URL': 'https://boot.example.invalid',
                  'MENU_PATH': profile['menu_path'], 'ASSET_ROOT': profile['asset_root']}
        for name in profile['templates']:
            source = (ROOT / name).read_text()
            require(not re.search(r'(?im)^\s*(chain|shell|config|reboot|poweroff|kernel|initrd|imgargs|sanboot|console|ui|menu\s+background)\b', source),
                    'unqualified action/graphics/recipe')
            require('192.168.' not in source and 'password' not in source.lower() and 'http://' not in source, 'unsafe source literal')
            require('Sambafied' in source, 'missing branding')
            render_fixture(source, values, profile)
            for bad in ['../escape', '/absolute', 'menus//empty', 'menus/with space', profile['menu_path'].upper()]:
                rejected(lambda: render_fixture(source, dict(values, MENU_PATH=bad), profile))
            for bad in ['http://boot.example.invalid', 'https://user:pass@boot.example.invalid',
                        'https://boot.example.invalid/x', 'https://boot.example.invalid?x=1', 'https://boot.example.invalid\ninjected']:
                rejected(lambda: render_fixture(source, dict(values, PUBLIC_BASE_URL=bad), profile))
            rejected(lambda: render_fixture(source + '@@UNKNOWN@@', values, profile))
            rejected(lambda: render_fixture(source, dict(values, ASSET_ROOT='../escape'), profile))
            rejected(lambda: render_fixture(source, dict(values, ASSET_ROOT=profile['asset_root'].upper()), profile))
            rendered += 1
        if profile['id'] == 'bios-pxelinux':
            cfg = (ROOT / 'bios-pxelinux/default.cfg').read_text()
            require('DISPLAY /@@MENU_PATH@@' in cfg and 'LOCALBOOT -1' in cfg and 'PROMPT 1' in cfg,
                    'PXELINUX text/firmware-return contract changed')
        else:
            source = (ROOT / profile['templates'][0]).read_text()
            require('menu Sambafied boot menu' in source and 'item return Return control' in source and
                    source.endswith('exit 0\n'), 'iPXE text/firmware-return contract changed')
    for arch in ['0', '7', '9', '6', '11', '', 'unknown', None, 7]:
        require(select_fixture(manifest, arch, set()) is None, 'unqualified loader selected')
    for arch, policy in manifest['dhcp_architecture_policy'].items():
        require(policy['qualification_required_for_each_architecture'], 'missing receipt gate')
        for profile_id in policy['allowed_profiles']:
            profile = next(p for p in manifest['profiles'] if p['id'] == profile_id)
            loader = profile['loader']['required_asset_path']
            receipt = {(arch, profile_id, loader)}
            require(select_fixture(manifest, arch, receipt, profile_id) == loader, 'declared qualified fixture rejected')
            for unknown in ['6', '11', '', 'unknown']:
                require(select_fixture(manifest, unknown, receipt, profile_id) is None, 'unknown architecture fallback')
            require(select_fixture(manifest, arch, {(arch, profile_id, loader.upper())}, profile_id) is None,
                    'loader path case mismatch accepted')
            if arch in ('7', '9'):
                other = '9' if arch == '7' else '7'
                require(select_fixture(manifest, other, receipt) is None, 'qualification reused across architectures')
    print(f'PASS: {rendered} controlled text fixtures; known placeholders, exact-case paths, safe origins, no recipes/graphics; architecture/qualification denials')


if __name__ == '__main__':
    main()
