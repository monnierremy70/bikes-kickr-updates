"""Verification publique, sans cle privee ni dependance Python externe."""
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
TARGETS = {"heltec-v4": (1, 9, 0x300000), "wroom32": (2, 0, 0x1E0000)}


def verify(data, model, version):
    target, chip, limit = TARGETS[model]
    if len(data) < 344:
        raise ValueError("Fichier tronque")
    magic, actual_target, fmt, reserved, size, digest, raw_version = struct.unpack("<8sBBHI32s16s", data[:64])
    if magic != b"KCALOTA2" or actual_target != target or fmt != 1 or reserved or not 24 <= size <= limit or len(data) != size + 320:
        raise ValueError("Modele, taille ou format invalide")
    actual_version = raw_version.split(b"\0", 1)[0].decode("ascii")
    if actual_version != version or not raw_version.endswith(b"\0") or not re.fullmatch(r"[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}", actual_version):
        raise ValueError("Version incoherente")
    if data[320] != 0xE9 or int.from_bytes(data[332:334], "little") != chip:
        raise ValueError("Image destinee a une autre puce")
    if hashlib.sha256(data[320:]).digest() != digest:
        raise ValueError("Empreinte du contenu incorrecte")
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        (directory / "metadata").write_bytes(data[:64])
        (directory / "signature").write_bytes(data[64:320])
        result = subprocess.run(["openssl", "dgst", "-sha256", "-verify", str(ROOT / "cle_publique.pem"), "-signature", str(directory / "signature"), str(directory / "metadata")], capture_output=True)
        if result.returncode:
            raise ValueError("Signature refusee")
    return hashlib.sha256(data).hexdigest()


def verify_all():
    request = json.loads((ROOT / "release-request.json").read_text())
    if not isinstance(request.get("draft"), bool):
        raise ValueError("Le champ draft doit etre un booleen")
    version = request["version"]
    if not isinstance(version, str) or not re.fullmatch(r"[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}", version):
        raise ValueError("Version invalide")
    expected = {f"BIKES_KICKR_{model}.kcal" for model in TARGETS}
    if {p.name for p in (ROOT / "release-files").iterdir()} != expected:
        raise ValueError("Le dossier de diffusion doit contenir uniquement les deux paquets publics")
    for model in TARGETS:
        path = ROOT / "release-files" / f"BIKES_KICKR_{model}.kcal"
        digest = verify(path.read_bytes(), model, version)
        print(f"OK {model} {version} SHA256 {digest}")
    return request


if __name__ == "__main__":
    verify_all()
