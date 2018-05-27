u"""
Crawler do site https://www.vagalume.com.br,
para apresentar títulos de músicas do artista inserido pelo usuário,
fazendo parte do top, com apenas a primeira letra ou todas as musicas,
podendo retornar a letra de alguma musica especifica e exportar para
um arquivo txt
"""

from requests import get
from bs4 import BeautifulSoup as bs


class Crawler:
    u"""
    Args:
        -artista: nome da artista
        -numero: quantos titulos retornar do top, com no máximo 25
        -letra: primeira letra dos titulos das musicas
        -todas: todas as músicas da url_artista
        -titulo: titulo de uma musica especifica
    """

    def __init__(self, artista, numero=15, letra=str(),
                 todas=False):
        self.url_base = 'https://www.vagalume.com.br/'
        self.artista = artista
        self.numero = numero
        self.letra = letra.upper()
        self.todas = todas
        self.musicas = list()
        self.url_artista = ''

    def conectar(self):
        u"""Retorna o html da página, caso haja erros na conexão do usuário
        ou se o artista não existir retorna uma mensagem de erro
        """
        # cria a url para a busca
        self.url_artista = self.url_base + self.artista+'/'
        vagalume_r = get(self.url_artista)  # faz a requisição no site
        # transforma o texto da página em html
        v_conteudo = bs(vagalume_r.text, 'lxml')

        # verifica se foi possivel acessar a url especificada
        try:
            v_conteudo.find_all('h1')[1]  # procura pelo nome do artista
        except IndexError:
            return 'Não foi possível encontrar a artista especificada, '\
                    'por favor verifique sua conexão ou se o nome da artista '\
                    'está correto.'  # mensagem de erro

        return v_conteudo  # retorna o conteúdo do site em html

    def buscar_top_titulos(self, conteudo):
        u"""Retorna os titulos das top músicas da artista.

        Args:
            -conteudo: Conteúdo do site em html
        """
        tops = conteudo.find('ol', {'class': 'artTops'})
        for top in range(0, int(self.numero)):
            self.musicas.append(tops.find_all('li')[top].find('span').text)

        return self.musicas

    def buscar_primeira_letra(self, conteudo):
        u"""Retorna os titulos das músicas pela primeira letra do titulo.

        Args:
            -conteudo: Conteúdo do site em html
        """
        musicas = conteudo.find('ul', {'class': 'tracks'})  # .find_all('li')
        lista_letra = list(musicas)
        if self.letra == '#':
            try:
                i = lista_letra.index(musicas.find(attrs={'data-index': 'A'}))
            except ValueError:
                try:
                    i = lista_letra.index(musicas.find(
                                attrs={'data-index': 'B'}))
                except ValueError:
                    i = len(lista_letra)
            if i == 1:
                return '\nNão foi possivel encontrar um titulo que inicie '\
                        'com essa letra'
            for j in range(0, i-1):
                self.musicas.append(musicas.find_all('li')[j]
                                    .find('span').text)
        else:
            try:
                i = lista_letra.index(musicas.find(
                            attrs={'data-index': self.letra}))
            except ValueError:
                return '\nNão foi possivel encontrar um titulo que inicie '\
                        'com essa letra'

            while i < len(lista_letra) and \
                musicas.find_all('li')[i].find('span').text\
                    .startswith(self.letra):

                self.musicas.append(musicas.find_all('li')[i]
                                    .find('span').text)
                i += 1

        return self.musicas

    def buscar_todas(self, conteudo):
        u"""Retorna todos os titulos das músicas do artista especificado.

        Args:
            -conteudo: Conteúdo do site em html
        """
        letra = conteudo.find('ul', {'class': 'tracks'}).find_all('li')
        for i in range(0, len(letra)):
            self.musicas.append(letra[i].find('span').text)

        return self.musicas

    def buscar_musica(self, conteudo, titulo):
        u"""Retorna a letra da música especificada.

        Args:
            -conteudo: Conteúdo do site em html.
            -titulo: Título da música para ser buscada.
        """
        tudo = {'titulo': titulo, 'artista': self.artista.lower().title()}
        musicas = conteudo.find('ul', {'class': 'tracks'}).find_all('li')
        titulo_url = '-'.join(titulo.lower().split())
        for i in range(0, len(musicas)):
            if titulo == musicas[i].find('span').text:
                var = self.url_artista+titulo_url+'.html'
                musica_r = get(var)
                m_conteudo = bs(musica_r.text, 'lxml')
                try:
                    tudo['compositor'] = m_conteudo\
                                        .find('p', {'id': 'extra'}).text[13:]
                except AttributeError:
                    pass
                tudo['letra'] = m_conteudo\
                    .find('div', {'itemprop': 'description'}).text
                break
        return tudo

    def exportar_txt(self, lista, titulo=str()):
        u"""Exporta a lista de musicas ou a letra de uma musica especifica para txt.

        Args:
            -lista: lista das musicas à serem exportadas.
            -titulo: titulo da música a ser exportada.
        """
        if titulo == '':
            arq = self.artista
        else:
            arq = titulo
        with open(arq+".txt", 'w') as f:
            f.write(str(lista))
