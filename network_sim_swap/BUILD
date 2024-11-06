resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-network-sim-swap',
    dependencies=[
        ':pyproject',
        ':readme',
        'network_sim_swap/src/vonage_network_sim_swap',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)
