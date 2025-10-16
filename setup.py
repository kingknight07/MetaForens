from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='metaforens',
    version='1.0.0',
    author='kingknight07',
    author_email='shuklaayush0704@gmail.com',
    description='Advanced AI image detection library using forensic analysis',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/kingknight07/MetaForens',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.19.0',
        'Pillow>=8.0.0',
        'opencv-python>=4.5.0',
        'scipy>=1.5.0',
    ],
    extras_require={
        'gui': ['tkinter'],
        'dev': [
            'pytest>=6.0.0',
            'black>=21.0',
            'flake8>=3.9.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'metaforens=metaforens:main',
        ],
    },
    keywords='ai detection, deepfake detection, image forensics, gan detection, fake image detection',
    project_urls={
        'Bug Reports': 'https://github.com/kingknight07/MetaForens/issues',
        'Source': 'https://github.com/kingknight07/MetaForens',
    },
)
