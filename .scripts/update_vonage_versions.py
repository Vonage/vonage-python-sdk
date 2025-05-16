import os
import re

import toml

# Define the paths to the vonage packages
packages = [
    "vonage-account",
    "vonage-application",
    "vonage-http-client",
    "vonage-messages",
    "vonage-network-auth",
    "vonage-network-sim-swap",
    "vonage-network-number-verification",
    "vonage-number-insight",
    "vonage-numbers",
    "vonage-sms",
    "vonage-subaccounts",
    "vonage-users",
    "vonage-utils",
    "vonage-verify",
    "vonage-verify-legacy",
    "vonage-video",
    "vonage-voice",
]


# Function to read the version from _version.py
def get_version(folder_path: str, package_path: str) -> str:
    content = None
    try:
        version_file = os.path.join(
            folder_path.replace("-", "_"),
            "src",
            package_path.replace("-", "_"),
            "_version.py",
        )

        with open(version_file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        if folder_path == "vonage-numbers":
            return get_version("number-management", "vonage-numbers")
        folder_path_fragments = package_path.split("-")
        folder_path = "_".join(folder_path_fragments[1:])
        return get_version(folder_path, package_path)

    version_match = re.search(r'__version__\s*=\s*[\'"]([^\'"]+)[\'"]', content)
    if version_match:
        return version_match.group(1)
    raise ValueError(f"Version not found in {version_file}")


# Read the existing pyproject.toml
with open("vonage/pyproject.toml", "r") as f:
    pyproject = toml.load(f)

# Update the dependencies with the versions from _version.py
dependencies = []
for package in packages:
    version = get_version(package, package)
    dependencies.append(f"{package}>={version}")

pyproject["project"]["dependencies"] = dependencies

# Write the updated pyproject.toml
with open("vonage/pyproject.toml", "w") as f:
    toml.dump(pyproject, f)

print("pyproject.toml updated with local package versions.")
