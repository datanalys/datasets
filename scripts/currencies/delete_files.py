import os



files = os.listdir('datasets/currencies/crypto/historical/')

for file in files:
    file_path = 'datasets/currencies/crypto/historical/' + file
    file_size = os.path.getsize(file_path)
    if(file_size == 0):
        print(file, "deleted")
        os.remove(file_path)