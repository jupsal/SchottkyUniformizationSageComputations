# run this using sage
try:
    import sage
except ImportError:
    raise ImportError('Run runtests.py with Sage:\tsage runtests.py')

try:
    import nose
except ImportError:
    raise ImportError('Install nose:\t$ sage -i nose')

nose.main(module='my_package')
