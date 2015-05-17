#coding:utf-8
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='csdncommenter',
    version='0.0.3',
    description='CSDN已下载资源自动批量评论脚本',
    long_description=open('README.md').read(),
    url='https://github.com/mzlogin/csdncommenter',
    author='Zhuang Ma',
    author_email='ChumpMa@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='csdn resource auto commenter',
    packages=['csdncommenter'],
    install_requires=[
        'requests',
        'BeautifulSoup'
    ],
    entry_points={
        'console_scripts': [
            'csdncommenter=csdncommenter.csdncommenter:main',
        ],
    },
)
