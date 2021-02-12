from setuptools import setup

modules=['cvutils', 'Point', 'jupyter_utils', 'SliceableDeque']
setup(name='lmello-utils',
    version='1.2',
    description='Lucas Mello utilities',
    url='https://github.com/Lucashsmello/lmello-utils',
    author='Lucas Mello',
    license='public',
    py_modules=["lmelloutils.%s" % m for m in modules],
    install_requires=[
        "numpy >= 1.17",
    ],
    zip_safe=False)
