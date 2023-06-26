from compansation import Compansation

def read(path):
    height = Compansation().board.shape[1] // 2 # height adapt
    width = Compansation().board.shape[0] // 2 # width adapt
    with open(path, 'r') as file:
        origin_contents = file.readlines()
        contents = []
        for content in origin_contents:
            str_lst = content.split()
            tmp_lst = []
            index = 0
            for string in str_lst:

                if index % 2 != 0:
                    tmp_lst.append(height - int(string))
                elif index == len(str_lst) - 1:
                    tmp_lst.append(int(string))
                else:
                    tmp_lst.append(int(string) + width)
                index += 1
            contents.append(tmp_lst)


    return contents

if __name__ == '__main__':
    file_path = './parameters.txt'
    contents = read(file_path)
    print(contents)