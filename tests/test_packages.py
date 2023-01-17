import os


def test_subdirectories_are_python_packages():
    subdirs = [
        os.path.join('src/vonage', o) for o in os.listdir('src/vonage') if os.path.isdir(os.path.join('src/vonage', o))
    ]
    for subdir in subdirs:
        if '__pycache__' in subdir or os.path.isfile(f'{subdir}/__init__.py'):
            continue
        else:
            raise Exception(f'Subfolder {subdir} doesn\'t have an __init__.py file')
