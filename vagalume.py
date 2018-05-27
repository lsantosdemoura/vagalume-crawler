u"""Módulo principal do Crawler, para fazer o tratamento dos parâmetros."""
from vagalume_crawler import Crawler
from argparse import ArgumentParser

parser = ArgumentParser(prog='Crawler Vagalume',  # nome do programa
                        usage='''python vagalume.py [artista] -n [numero] -l \
[letra] -t -m [musica]''',  # como usar os argumentos
                        description='''\n
                        Buscador de titulos de música baseado no artista \
                        especificado.''')  # descrição do programa)

# definindo argumentos
# -artista: Argumento obrigatório
parser.add_argument('artista', help='Nome do artista à ser buscado.')
# agrupando argumentos para que não sejam usados simultaneamente
grupo = parser.add_mutually_exclusive_group()
grupo.add_argument('-n', '--numero', type=int, default=15,
                   help='Numero de musicas do TOP sendo no máximo 25.')
grupo.add_argument('-l', '--letra', default='',
                   help='Primeira letra da lista de músicas a ser buscada.')
grupo.add_argument('-t', '--todas', action='store_true', default=False,
                   help='Mostra todas as musicas do artista.')
grupo.add_argument('-m', '--musica', default='',
                   help='Musica para a letra ser buscada.')

args = parser.parse_args()  # definindo argumentos

if args.musica:
    print('Buscando por {}...\n'.format(args.musica.lower().title()))
else:
    print('Buscando por {}...\n'.format(args.artista.lower().title()))
artista = '-'.join(args.artista.lower().split())

musica = '-'.join(args.musica.lower().split())
crawler = Crawler(artista=artista, numero=args.numero, letra=args.letra,
                  todas=args.todas)
conteudo = crawler.conectar()

if not str(conteudo).startswith('Não'):
    if musica:
        lista = crawler.buscar_musica(conteudo, args.musica.lower().title())
        print(lista)
    elif args.letra:
        lista = crawler.buscar_primeira_letra(conteudo)
    elif args.todas:
        lista = crawler.buscar_todas(conteudo)
    else:
        lista = crawler.buscar_top_titulos(conteudo)
    print('\n'.join(lista))

    txt = str(input('\nDeseja exportar para txt? (s/n):\n')).upper()
    if txt in ['S', 'SIM']:
        crawler.exportar_txt('\n'.join(lista), musica)
else:
    print(conteudo)
