import os


def test_subdirectories_are_python_packages():
    subdirs = [
        os.path.join('src/vonage', o) for o in os.listdir('src/vonage') if os.path.isdir(os.path.join('src/vonage', o))
    ]
    print(subdirs)
    for subdir in subdirs:
        if '__pycache__' in subdir:
            continue
        elif os.path.isfile(f'{subdir}/__init__.py'):
            print(f'all good for {subdir}')
        else:
            print(f'Subfolder {subdir} doesn\'t have an __init__.py file')
            assert False
