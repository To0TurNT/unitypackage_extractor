from setuptools import setup

setup(
    name='unitypackage_extractor',
    version='1.2.0',
    description='Extractor for .unitypackage files (fork of Cobertos/unitypackage_extractor)',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/To0TurNT/unitypackage_extractor/',
    # Fork maintained by To0TurNT; original project by Cobertos (https://github.com/Cobertos)
    author='To0TurNT',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Filesystems'
    ],
    install_requires=[
        'tarsafe>=0.0.2',
    ],
    keywords='untiy unity3d unitypackage extract tar extractor',
    packages=['unitypackage_extractor']
)
