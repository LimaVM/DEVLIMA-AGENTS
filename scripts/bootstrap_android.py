"""Install pinned Android CLI tools on a Linux build host; no project credentials."""

import argparse
import hashlib
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

SDK_ARCHIVE = "commandlinetools-linux-16111833_latest.zip"
SDK_SHA1 = "e025545c62a8e64c7559119566a569fb1dec5f60"
GRADLE_VERSION = "8.13"


def download(url, path):
    with urllib.request.urlopen(url, timeout=120) as response, path.open("wb") as target:
        shutil.copyfileobj(response, target)


def extract(path, directory):
    root = directory.resolve()
    with zipfile.ZipFile(path) as archive:
        for item in archive.infolist():
            if not (root / item.filename).resolve().is_relative_to(root):
                raise RuntimeError("Unsafe archive path")
        archive.extractall(root)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", type=Path, default=Path("/srv/devlima-android-sdk"))
    parser.add_argument("--tools-root", type=Path, default=Path("/srv/devlima-build-tools"))
    parser.add_argument("--emulator", action="store_true")
    args = parser.parse_args()
    if not args.sdk_root.is_absolute() or not args.tools_root.is_absolute():
        raise SystemExit("Use absolute installation directories")
    for directory in (args.sdk_root, args.tools_root):
        directory.mkdir(parents=True, exist_ok=True)
    manager = args.sdk_root / "cmdline-tools/latest/bin/sdkmanager"
    with tempfile.TemporaryDirectory(prefix="devlima-android-") as temporary:
        staging = Path(temporary)
        if not manager.exists():
            archive = staging / "sdk.zip"
            download("https://dl.google.com/android/repository/" + SDK_ARCHIVE, archive)
            if hashlib.sha1(archive.read_bytes()).hexdigest() != SDK_SHA1:
                raise RuntimeError("Android archive checksum mismatch")
            extract(archive, staging)
            destination = args.sdk_root / "cmdline-tools/latest"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(staging / "cmdline-tools"), str(destination))
            for executable in (destination / "bin").iterdir():
                executable.chmod(0o755)
        gradle = args.tools_root / f"gradle-{GRADLE_VERSION}"
        if not gradle.exists():
            archive = staging / "gradle.zip"
            base = f"https://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-bin.zip"
            expected = urllib.request.urlopen(base + ".sha256", timeout=30).read().decode().strip()
            download(base, archive)
            if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
                raise RuntimeError("Gradle archive checksum mismatch")
            extract(archive, args.tools_root)
            (gradle / "bin/gradle").chmod(0o755)
    packages = ["platform-tools", "platforms;android-36", "build-tools;36.0.0"]
    if args.emulator:
        packages.extend(["emulator", "system-images;android-36;google_apis;x86_64"])
    log = args.tools_root / "android-sdk-install.log"
    with log.open("wb") as output:
        subprocess.run(
            [str(manager), f"--sdk_root={args.sdk_root}", "--licenses"],
            input=b"y\n" * 100,
            stdout=output,
            stderr=subprocess.STDOUT,
            check=True,
        )
        subprocess.run(
            [str(manager), f"--sdk_root={args.sdk_root}", *packages],
            input=b"y\n" * 100,
            stdout=output,
            stderr=subprocess.STDOUT,
            check=True,
        )
    print(
        {
            "sdk_root": str(args.sdk_root),
            "gradle": str(gradle / "bin/gradle"),
            "packages": packages,
            "log": str(log),
        }
    )


if __name__ == "__main__":
    main()
