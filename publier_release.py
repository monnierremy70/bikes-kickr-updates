"""GitHub Actions publisher. Only the two previously verified public assets."""
import json
import os
import subprocess
from verifier_publication import ROOT, TARGETS, verify_all


def main():
    request = verify_all()
    repository = os.environ["GITHUB_REPOSITORY"]
    revision = os.environ["GITHUB_SHA"]
    tag = "v" + request["version"]
    common = ["--repo", repository]
    existing = subprocess.run(["gh", "release", "view", tag, *common, "--json", "isDraft"], capture_output=True, text=True)
    if existing.returncode == 0:
        if not json.loads(existing.stdout)["isDraft"]:
            print("Cette version est deja publiee : aucun fichier modifie.")
            return
    else:
        subprocess.run(["gh", "release", "create", tag, *common, "--draft", "--target", revision, "--title", "BIKES KICKR " + request["version"], "--notes-file", str(ROOT / "NOTES_VERSION.md")], check=True)
    assets = [str(ROOT / "release-files" / f"BIKES_KICKR_{model}.kcal") for model in TARGETS]
    subprocess.run(["gh", "release", "upload", tag, *common, *assets, "--clobber"], check=True)
    if not request["draft"]:
        subprocess.run(["gh", "release", "edit", tag, *common, "--draft=false", "--latest"], check=True)
    print("Release preparee : " + tag)


if __name__ == "__main__":
    main()
