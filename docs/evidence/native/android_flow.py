import json
import pathlib
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = pathlib.Path('/Users/md.touhidulislam/Projects/product_assignment/docs/evidence/native')
ROOT.mkdir(parents=True, exist_ok=True)
APP = 'com.shopdiscover'
events = []


def adb(*args):
    return subprocess.check_output(['adb', '-s', 'emulator-5554', *args], timeout=30)


def ui():
    adb('shell', 'uiautomator', 'dump', '/sdcard/shopdiscover-window.xml')
    raw = adb('exec-out', 'cat', '/sdcard/shopdiscover-window.xml')
    return ET.fromstring(raw), raw


def find(tree, label):
    for node in tree.iter('node'):
        if any(label.casefold() == value.casefold() for value in
               (node.get('text', ''), node.get('content-desc', ''))):
            return node
    return None


def wait(label, timeout=25):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        tree, raw = ui()
        # A system dialog left by earlier host-memory pressure is not app UI.
        if find(tree, "System UI isn't responding") is not None:
            dismiss = find(tree, 'Close app')
            x1, y1, x2, y2 = map(int, re.findall(r'\d+', dismiss.get('bounds')))
            adb('shell', 'input', 'tap', str((x1 + x2) // 2), str((y1 + y2) // 2))
            print('Restarted unresponsive emulator System UI', flush=True)
            continue
        node = find(tree, label)
        if node is not None:
            return node
        time.sleep(0.5)
    raise AssertionError(f'Missing {label}: {raw.decode()}')


def tap(label):
    node = wait(label)
    x1, y1, x2, y2 = map(int, re.findall(r'\d+', node.get('bounds')))
    adb('shell', 'input', 'tap', str((x1 + x2) // 2), str((y1 + y2) // 2))


def capture(name):
    tree, raw = ui()
    (ROOT / f'{name}.xml').write_bytes(raw)
    (ROOT / f'{name}.png').write_bytes(adb('exec-out', 'screencap', '-p'))
    events.append({'step': name, 'capturedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    print(name, flush=True)
    return tree


wifi = adb('shell', 'settings', 'get', 'global', 'wifi_on').decode().strip()
mobile = adb('shell', 'settings', 'get', 'global', 'mobile_data').decode().strip()
try:
    adb('shell', 'am', 'force-stop', APP)
    adb('shell', 'am', 'start', '-n', f'{APP}/.MainActivity')
    wait('Search products', 40)
    capture('android-online')
    tap('Search products')
    adb('shell', 'input', 'text', 'phone')
    adb('shell', 'input', 'keyevent', '66')
    wait('16 of 194 products')
    capture('android-phone-search')
    tap('Filters')
    tap('In stock only')
    wait('15 of 194 products')
    tap('Maximum price')
    adb('shell', 'input', 'text', '500')
    adb('shell', 'input', 'keyevent', '4')
    tap('Apply price range')
    wait('12 of 194 products')
    tap('Hide filters')
    adb('shell', 'input', 'swipe', '720', '2450', '720', '1400', '400')
    tree = capture('android-filtered-scrolled')
    cards = [n for n in tree.iter('node') if n.get('content-desc', '').startswith('View details for ')]
    assert cards, 'No product cards visible'
    card = next(n for n in cards if int(re.findall(r'\d+', n.get('bounds'))[1]) > 1100)
    label, bounds = card.get('content-desc'), card.get('bounds')
    tap(label)
    wait('Product details')
    capture('android-details')
    adb('shell', 'input', 'keyevent', '4')
    wait('12 of 194 products')
    returned = wait(label)
    assert returned.get('bounds') == bounds, (bounds, returned.get('bounds'))
    capture('android-back-preserved')
    tap('Filters')
    tree, _ = ui()
    assert any(n.get('text') == '500' for n in tree.iter('node')), 'Price draft lost'
    tap('Reset all')
    wait('194 of 194 products')
    capture('android-reset')

    # Wait beyond the 1s persistence throttle, then really terminate and reopen.
    time.sleep(2)
    adb('shell', 'svc', 'wifi', 'disable')
    adb('shell', 'svc', 'data', 'disable')
    wait('Offline — showing saved products')
    adb('shell', 'am', 'force-stop', APP)
    adb('shell', 'am', 'start', '-n', f'{APP}/.MainActivity')
    wait('Offline — showing saved products', 40)
    wait('194 of 194 products')
    capture('android-offline-restart')
    tap('Search products')
    adb('shell', 'input', 'text', 'phone')
    adb('shell', 'input', 'keyevent', '66')
    wait('16 of 194 products')
    tap('View details for iPhone 5s')
    wait('Offline — showing saved product information')
    capture('android-offline-details')
    adb('shell', 'input', 'keyevent', '4')
    wait('16 of 194 products')
    capture('android-offline-back')
finally:
    adb('shell', 'svc', 'wifi', 'enable' if wifi == '1' else 'disable')
    adb('shell', 'svc', 'data', 'enable' if mobile == '1' else 'disable')
    (ROOT / 'android-checks.json').write_text(json.dumps(events, indent=2) + '\n')

# Stale-cache reconnect may refresh; the user's search must remain.
wait('16 of 194 products')
end = time.monotonic() + 20
while time.monotonic() < end:
    tree, _ = ui()
    if find(tree, 'Offline — showing saved products') is None:
        break
    time.sleep(0.5)
else:
    raise AssertionError('Offline notice did not clear after restoring networking')
capture('android-reconnected')
(ROOT / 'android-checks.json').write_text(json.dumps(events, indent=2) + '\n')
print('PASS: search, filters, details, exact scroll bounds, reset, offline restart/details and reconnect', flush=True)
