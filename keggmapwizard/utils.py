import os

if 'KEGG_MAP_WIZARD_DATA' in os.environ:
    KEGG_MAP_WIZARD_DATA = os.environ['KEGG_MAP_WIZARD_DATA']

else:
    KEGG_MAP_WIZARD_DATA = input('Enter KEGG_MAP_WIZARD_DATA path '
                                 '(or press Enter to create a new folder in the current directory): ')
    if KEGG_MAP_WIZARD_DATA == '':
        KEGG_MAP_WIZARD_DATA = './KEGG_MAP_WIZARD_DATA'
        os.makedirs(KEGG_MAP_WIZARD_DATA, exist_ok=True)

    os.environ['KEGG_MAP_WIZARD_DATA'] = KEGG_MAP_WIZARD_DATA

if not os.path.isdir(KEGG_MAP_WIZARD_DATA):
    raise NotADirectoryError(f'The {KEGG_MAP_WIZARD_DATA=} path is not a valid directory')

if not os.path.isdir(KEGG_MAP_WIZARD_DATA):
    os.mkdir(KEGG_MAP_WIZARD_DATA)
