u"""Módulo para fazer a busca."""

from requests import get  # modulo de requisição
from bs4 import BeautifulSoup as bs  # modulo para fazer html parse


class Crawler:
    u"""
    Classe que compõe as funções de busca e exportação.

    Args:
        -artista: nome da artista
        -numero: quantos titulos retornar do top, com no máximo 25
        -letra: primeira letra dos titulos das musicas
        -todas: todas as músicas da url_artista
    """

    def __init__(self, artista, numero=15, letra=str(), todas=False):
        self.url_base = 'https://www.vagalume.com.br/'
        self.artista = artista
        self.numero = numero  # quantidade de músicas do TOP
        self.letra = letra.upper()  # letra para ser buscada
        self.todas = todas  # todas as musicas
        self.musicas = list()  # lista de múscas
        self.url_artista = ''

    def conectar(self):
        u"""Retorna o html da página."""
        # cria a url para a busca
        self.url_artista = self.url_base + self.artista+'/'
        vagalume_r = get(self.url_artista)  # faz a requisição no site
        # transforma o texto da página em html
        v_conteudo = bs(vagalume_r.text, 'lxml')

        # verifica se foi possivel acessar a url especificada
        try:
            v_conteudo.find_all('h1')[1]  # procura pelo nome do artista
        except IndexError:
            return False

        return v_conteudo  # retorna o conteúdo do site em html

    def buscar_top_titulos(self, conteudo):
        u"""Retorna os titulos das top músicas da artista.

        Args:
            -conteudo: Conteúdo do site em html
        """
        # inserindo lista das TOP musicas na variavel
        tops = conteudo.find('ol', {'class': 'artTops'}).find_all('li')
        # iterando até o numero inserido pelo usuario
        for top in range(0, int(self.numero)):
            # adicionando as musicas na lista que será retornada na função
            self.musicas.append(tops[top].find('span').text)

        return '\n'.join(self.musicas)

    def verificar_especiais(self, lista_mus, musicas):
        u"""
        Verifica qual é a letra após a sessão de caracteres especiais/números.

        Args:
            -lista_mus: lista de músicas para parse
            -musicas: lista de músicas para indexar
        """
        # caso o primeiro caractere da proxima sessão não seja A nem B
        # considera que o artista tem apenas titulos de músicas iniciadas
        # por caracteres especiais ou numeros
        try:
            # busca se o caractere da proxima sessão é A
            p_char = lista_mus.index(musicas.find(attrs={'data-index': 'A'}))
        except ValueError:
            try:
                # busca se o caractere da proxima sessão é B
                p_char = lista_mus.index(musicas.find(
                            attrs={'data-index': 'B'}))
            except ValueError:
                # passa o tamanho da lista de musicas para a variavel
                p_char = len(lista_mus)
        return p_char

    def buscar_primeira_letra(self, conteudo):
        u"""Retorna os titulos das músicas pela primeira letra do titulo.

        Args:
            -conteudo: Conteúdo do site em html
        """
        # insere a lista de todas as musicas do artista na variavel
        musicas = conteudo.find('ul', {'class': 'tracks'})
        # transforma a variavel de tipo bs4 em lista
        lista_mus = list(musicas)
        # a '#' é a representação dos caracteres especiais/numeros do vagalume
        if self.letra == '#':
            p_char = self.verificar_especiais(lista_mus, musicas)
            # se a variavel for igual a 1 significa que a primeira sessão
            # do artista não é de caracteres especiais
            if p_char == 1:
                return False
            # iterando até a posição da próxima sessão
            for j in range(0, p_char-1):
                self.musicas.append(musicas.find_all('li')[j]
                                    .find('span').text)
        else:
            # caso não haja sessão com a letra que o usuario inseriu
            # retorna falso
            try:
                u_char = lista_mus.index(musicas.find(
                            attrs={'data-index': self.letra}))
            except ValueError:
                return False

            # itera enquanto a variavel for menor que a quantidade de músicas
            # e se a primeira letra ainda é igual à que o usuario inseriu
            while u_char < len(lista_mus) and \
                musicas.find_all('li')[u_char].find('span').text\
                    .startswith(self.letra):

                self.musicas.append(musicas.find_all('li')[u_char]
                                    .find('span').text)
                u_char += 1

        return '\n'.join(self.musicas)

    def buscar_todas(self, conteudo):
        u"""Retorna todos os titulos das músicas do artista especificado.

        Args:
            -conteudo: Conteúdo do site em html
        """
        # insere a lista de todas as musicas do artista na variavel
        letra = conteudo.find('ul', {'class': 'tracks'}).find_all('li')
        # itera da primeira à ultima musica da lista
        for i in range(0, len(letra)):
            self.musicas.append(letra[i].find('span').text)

        return '\n'.join(self.musicas)

    def buscar_musica(self, conteudo, titulo):
        u"""Retorna a letra da música especificada.

        Args:
            -conteudo: Conteúdo do site em html.
            -titulo: Título da música para ser buscada.
        """
        # criação de dicionario para retornar todas as imformações da musica
        tudo = {'titulo': titulo, 'artista': self.artista.lower().title()}
        # inserindo lista de musicas na variavel
        musicas = conteudo.find('ul', {'class': 'tracks'}).find_all('li')
        # itera pelas músicas buscando alguma que seja igual à inserida.
        for i in range(0, len(musicas)):
            if titulo == musicas[i].find('span').text:
                # pegando o URL da música encontrada
                titulo_url = self.url_base + musicas[i].find('a')['href']
                # requisição na url da música
                musica_r = get(titulo_url)
                # transformando pagina em html
                m_conteudo = bs(musica_r.text, 'lxml')
                # nem todas as músicas tem o compositor especificado no site
                # portanto não contem a tag com o compositor
                try:
                    tudo['compositor'] = m_conteudo\
                                        .find('p', {'id': 'extra'}).text[13:]
                except AttributeError:
                    tudo['compositor'] = 'Não especificado'
                # pega a letra da musica e transforma os <br> em \n
                tudo['letra'] = m_conteudo\
                    .find('div', {'itemprop': 'description'}).get_text('\n')
                break
        # se a música não for encontrada retorna falso
        else:
            return False
        return tudo

    def exportar_txt(self, lista, titulo=str()):
        u"""Exporta a lista de musicas ou a letra de uma musica para txt.

        Args:
            -lista: lista das musicas à serem exportadas.
            -titulo: titulo da música a ser exportada.
        """
        # verifica se o que será exportado é uma lista de musicas ou
        # a letra de uma musica para colocar como nome do arquivo
        if titulo == '':
            arq = self.artista
        else:
            arq = titulo
        with open(arq+".txt", 'w') as f:
            f.write(str(lista))
