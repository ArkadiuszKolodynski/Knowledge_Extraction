import os


def main():
    os.mkdir('request_data')
    for filename in os.listdir('data'):
        file = open('data/' + filename, 'r', encoding='utf=8').read()
        file = file.split("\n\n")

        request_string = [s for s in file if 'nif:isString' in s]

        request_file = open('request_data/' + filename, 'w')
        request_file.write(file[0] + '\n\n')
        request_file.write(request_string[0])


if __name__ == '__main__':
    main()
