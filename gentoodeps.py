#!/usr/bin/python3

#WTFPL
#find dependencies with equery b and ldd
from sys import argv
from subprocess import check_output
from os.path import basename
#helpers for Print

CODE = {
'BOLD':1,
'UNDERLINE':4,
'BLINK':5,
'INVERT':7,
'CONCEALD':8,
'STRIKE':9,
'GREY30':90,
'GREY40':2,
'GREY65':37,
'GREY70':97,
'GREY20_BG':40,
'GREY33_BG':100,
'GREY80_BG':47,
'GREY93_BG':107,
'DARK_RED':31,
'RED':91,
'RED_BG':41,
'LIGHT_RED_BG':101,
'DARK_YELLOW':33,
'YELLOW':93,
'YELLOW_BG':43,
'LIGHT_YELLOW_BG':103,
'DARK_BLUE':34,
'BLUE':94,
'BLUE_BG':44,
'LIGHT_BLUE_BG':104,
'DARK_MAGENTA':35,
'PURPLE':95,
'MAGENTA_BG':45,
'LIGHT_PURPLE_BG':105,
'DARK_CYAN':36,
'AUQA':96,
'CYAN_BG':46,
'LIGHT_AUQA_BG':106,
'DARK_GREEN':32,
'GREEN':92,
'GREEN_BG':42,
'LIGHT_GREEN_BG':102,
'BLACK':30
}

def termcode(num = 0): # 0 means color resetting
    'Return terminal code for color. Default - reset'
    return '\033[{}m'.format(num)

def colorstr (s, color):
    'colorize s by color'
    return termcode(CODE[color])+s+termcode()


def notfound(lib):
    'print not found message'
    print (colorstr('library {} not found!!!'.format(lib), 'RED'),
     'Search at http://www.portagefilelist.de/site/query/file')
    print('\n')


def find_package (lib):
    'Find library with equery and print the results'

    print(colorstr(lib+':', 'BLUE'))
    try:
        print(colorstr(check_output(['equery','b', lib], universal_newlines=True), 'GREEN'))
    except:
        notfound(lib)

def find_deps(file):
    'call ldd on file, return list holding all libraries linked'
    return check_output(['ldd', file], universal_newlines=True).splitlines()
    

if __name__ == '__main__':
    if len(argv) != 2:
        print ("{}: Too few/many arguments, exiting".format(argv[0]))
        exit()

    for dep in find_deps(argv[1]):
        lib_lst = dep.split (' => ')
        if len(lib_lst) == 2:
            library = lib_lst[1].strip()
            if library == 'not found':
                notfound(lib_lst[0].strip())
            else:
                find_package(basename(library.split()[0].strip()))
