import os
import re
import toml

# Define the paths to the vonage packages
packages = [
    "vonage-utils",
    "vonage-http-client",
    "vonage-account",
    "vonage-application",
    "vonage-messages",
    "vonage-number-insight",
    "vonage-numbers",
    "vonage-sms",
    "vonage-subaccounts",
    "vonage-users",
    "vonage-verify",
    "vonage-verify-v2",
    "vonage-video",
    "vonage-voice",
]


# Function to read the version from _version.py
def get_version(package_path):
    version_file = os.path.join(
        package_path, "src", package_path.replace("-", "_"), "_version.py"
    )
    with open(version_file, "r") as f:
        content = f.read()
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
    version = get_version(package)
    dependencies.append(f"{package}=={version}")

pyproject["project"]["dependencies"] = dependencies

# Write the updated pyproject.toml
with open("pyproject.toml", "w") as f:
    toml.dump(pyproject, f)

print("pyproject.toml updated with local package versions.")
