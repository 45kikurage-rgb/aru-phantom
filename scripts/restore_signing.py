"""Restore only Aru-Phantom's dedicated release key. Never prints secrets.
Requires cryptography. Inputs: private recovery ZIP A and private repo part B.
"""
import base64
import json
import os
import sys
import zipfile
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def restore(part_a_zip: Path, part_b_file: Path, destination: Path):
    with zipfile.ZipFile(part_a_zip) as archive:
        envelope = json.loads(archive.read('envelope.json'))
        part_a = archive.read('part-a.bin')
    part_b = base64.b64decode(part_b_file.read_text().strip(), validate=True)
    if len(part_a) != 32 or len(part_b) != 32:
        raise ValueError('Invalid recovery component size')
    if envelope['format'] != 'aru-phantom-signing-v1':
        raise ValueError('Wrong signing backup format')
    key = bytes(a ^ b for a, b in zip(part_a, part_b))
    payload = json.loads(AESGCM(key).decrypt(
        base64.b64decode(envelope['nonce_b64']),
        base64.b64decode(envelope['ciphertext_b64']),
        base64.b64decode(envelope['aad_b64']),
    ))
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    for filename, content in [
        ('release.p12', base64.b64decode(payload['keystore_b64'])),
        ('password', payload['password'].encode()),
        ('alias', payload['alias'].encode()),
    ]:
        path = destination / filename
        with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'wb') as out:
            out.write(content)
    return destination

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('Usage: restore_signing.py RECOVERY_A.zip PART_B.b64 PRIVATE_OUTPUT_DIR')
    restore(*(Path(x) for x in sys.argv[1:]))
    print('Dedicated signing key restored. Secrets were not printed.')
