"""Locate RPCS3's key files (key_vault.cpp + key_vault.h).

No keys are stored in this repo. They are read from RPCS3's public source: either a local
checkout's rpcs3/Crypto directory, or downloaded once from GitHub into ~/.cache/crt-4x3-patches/.
"""
import os, urllib.request

RAW = 'https://raw.githubusercontent.com/RPCS3/rpcs3/master/rpcs3/Crypto/'
CACHE = os.path.join(os.path.expanduser('~'), '.cache', 'crt-4x3-patches', 'rpcs3-crypto')


def keys_dir(path=None):
    if path:
        return path
    os.makedirs(CACHE, exist_ok=True)
    for name in ('key_vault.cpp', 'key_vault.h'):
        dst = os.path.join(CACHE, name)
        if not os.path.exists(dst):
            print(f'downloading {name} from RPCS3 GitHub')
            urllib.request.urlretrieve(RAW + name, dst)
    return CACHE
