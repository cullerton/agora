from setuptools import setup

setup(
    name='agora',
    packages=['agora'],
    version="0.1",
    install_requires=['sqlalchemy'],
    author='mike cullerton',
    author_email='michaelc@cullerton.com',
    description='A forum for ideas.',
    url='https://github.com/cullerton/agora',
    download_url='https://github.com/cullerton/agora/tarball/0.1',
    keywords=['academic', 'simple', 'example'],
    classifiers=[],
    entry_points="""\
    [console_scripts]
    initialize_agora_db = agora.initialize_db:main
    """,
    package_data={
        '': ['*.txt', '*.rst', '*.ipynb'],
    },
)
