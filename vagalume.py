u"""Módulo para tratar os parâmetros e imprimir o resultado da busca."""

# importando modulo para cração de argumentos
from argparse import ArgumentParser

from vagalume_crawler import Crawler  # importando classe do Crawler


def main_func():
    u"""Função principal para tratamento dos parâmetros."""
    # criando help do programa
    parser = ArgumentParser(prog='Crawler Vagalume',  # nome do programa
                            # como usar os argumentos
                            usage='python vagalume.py [artista] -n [numero] '
                                  '-l[letra] -t -m [musica]',
                            # descrição do programa
                            description='\nBuscador de titulos de música '
                                        'baseado no artista especificado.')

    # definindo argumentos
    # -artista: Argumento obrigatório
    parser.add_argument('artista', help='Nome do artista à ser buscado.')
    # agrupando argumentos para que não sejam usados simultaneamente
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument('-n', '--numero', type=int, default=15,
                       help='Numero de musicas do TOP sendo no máximo 25.')
    grupo.add_argument('-l', '--letra', default='',
                       help='Primeira letra da lista de músicas a ser '
                            'buscada.\nUse "#" para caracteres '
                            'especiais/numeros')
    grupo.add_argument('-t', '--todas', action='store_true', default=False,
                       help='Mostra todas as musicas do artista.')
    grupo.add_argument('-m', '--musica', default='',
                       help='Musica para a letra ser buscada.')

    args = parser.parse_args()  # definindo argumentos

    # caso usuario peça a letra de uma musica mostra mensagem com titulo
    # senão a mensagem sera com o nome do artista
    # independente de como o usuario inserir o nome do artista ou da música
    # sempre mostrará com a primeira letra de cada palavra em maiúsculo
    if args.musica:
        print('Buscando por {}...\n'.format(args.musica.lower().title()))
    else:
        print('Buscando por {}...\n'.format(args.artista.lower().title()))
    # transforma nome do artista e musica para um formato buscável na url
    # tirando os espaços e colocando -
    artista = '-'.join(args.artista.lower().split())
    musica = '-'.join(args.musica.lower().split())
    # criando objeto e enviando os parametros inseridos pelo usuario
    # enviando valor padrão se não inserido
    crawler = Crawler(artista=artista, numero=args.numero,
                      letra=args.letra, todas=args.todas)
    # conteudo retorna falso se não encontrar o artista
    conteudo = crawler.conectar()

    if conteudo:
        if musica:
            lista = crawler.buscar_musica(conteudo,
                                          args.musica.lower().title())
            lista = 'Artista: {}\nCompositor: {}\nTitulo: {}\n\nLetra:\n{}'\
                    .format(lista['artista'], lista['compositor'],
                            lista['titulo'], lista['letra'])
            if not lista:
                print('Não foi possível encontrar a música especificada.')
        elif args.letra:
            lista = crawler.buscar_primeira_letra(conteudo)
            if not lista:
                print('Não foi possivel encontrar um titulo que inicie '
                      'com esse caractere.')
        elif args.todas:
            lista = crawler.buscar_todas(conteudo)
        else:
            lista = crawler.buscar_top_titulos(conteudo)
        if lista:
            print(lista)

            txt = str(input('\nDeseja exportar para txt? (s/n):\n')).upper()
            if txt in ['S', 'SIM']:
                crawler.exportar_txt(lista, musica)
    else:
        print('Não foi possível encontrar a artista especificada, '
              'por favor verifique sua conexão ou se o nome da artista '
              'está correto.')


if __name__ == '__main__':
    main_func()
