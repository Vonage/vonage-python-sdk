resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-gnp-sim-swap',
    dependencies=[
        ':pyproject',
        ':readme',
        'gnp_sim_swap/src/vonage_gnp_sim_swap',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)
