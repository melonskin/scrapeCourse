import os

for dirname, dirnames, filenames in os.walk('.'):
    print(dirnames)
    print(dirname)
    print(filenames)
    for subdirname in dirnames:
        print(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        print(os.path.join(dirname, filename))
        filename2, file_extension = os.path.splitext(os.path.join(dirname, filename))
        if file_extension == '.pdf':
            os.remove(os.path.join(dirname, filename))

