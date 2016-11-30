def extract_data(file0='test_data.html'):
    mode = 'r'
    prefix = '/* stats start */'
    suffix = '/* stats end */'

    file_object = open(file0, mode)

    pythonfile = open('data.py', 'w')

    enable_write = False
    for line in file_object:
        if suffix in line:
            enable_write = False
        if enable_write:
            l = line.replace('null', 'None')
            pythonfile.write(l)
        if prefix in line:
            enable_write = True

    file_object.close()
    pythonfile.close()
