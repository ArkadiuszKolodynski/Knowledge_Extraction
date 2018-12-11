import os


def main():
    os.mkdir('response_data')
    for filename in os.listdir('data'):
        file = open('data/' + filename, 'r', encoding='utf=8').read()
        file = file.split("\n\n")

        response_string = [s for s in file if 'nif:isString' not in s]

        response_file = open('response_data/' + filename, 'w')
        response_file.write(file[0] + '\n\n')
        for block in response_string[1:]:
            response_file.write(block + '\n\n')


if __name__ == '__main__':
    main()
