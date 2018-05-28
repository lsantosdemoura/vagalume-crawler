# VAGALUME CRAWLER

Python 3.5.3
---
## Objetivo

Crawler do site www.vagalume.com, apresenta uma lista de músicas baseada no artista que o usuário inserir ou a letra da música especificada pelo usuário,  também sendo possível exportá-las para um arquivo de texto.
---
## Instalação

```
$ git clone https://github.com/lsantosdemoura/vagalume-crawler.git
$ cd vagalume_crawler
$ pip3 install -r requirements.txt
```
---
## Uso

Para retornar apenas as 15 primeiras músicas do TOP:

```
$ python vagalume.py 'Megadeth'

Buscando por Megadeth...

Symphony Of Destruction
A Tout Le Monde
Holy Wars... The Punishment Due
Dystopia
Tornado Of Souls
She-Wolf
Trust
Hangar 18
In My Darkest Hour
The Threat Is Real
Peace Sells
Mechanix
Angry Again
Sweating Bullets
Lying in State
```

Caso deseje exportar para txt, é criado um arquivo com o nome do artista contendo a lista das músicas:

```
Deseja exportar para txt? (s/n):
s
```
---
Para retornar um número especifico de músicas do TOP sendo no máximo 25:

```
$ python vagalume.py 'faun' -n 12

Buscando por Faun...

Federkleid
Walpurgisnacht
Diese kalte Nacht
Odin
Sonnenreigen (Lughnasad)
Unda
Von Den Elben
Tanz Mit Mir (Duett Mit Santiano)
Tempus Transit
2 Falken Corrigida
Rosmarin
Minne Duett

Deseja exportar para txt? (s/n):
n
```
---
Para retornar as músicas de um artista baseado na primeira letra do titulo:

```
$ python vagalume.py 'MAMONAS ASSASSINAS' -l '#'

Buscando por Mamonas Assassinas...

1406

Deseja exportar para txt? (s/n):
n
```
---
Para retornar todas as músicas do artista:

```
$ python vagalume.py 'Rammstein' -t

Buscando por Rammstein...

A Sacrifice
Adios
Alter Mann
Alter Mann (inglês)
Amerika
Amerika (Alemão)
Amerika (English Version)
Amour
Asche Zu Asche
Ashes To Ashes
Barbie Girl
...
You Hate (Du Hast English Edition)
You Smell So Good
Zerstören
Zwitter

Deseja exportar para txt? (s/n):
n
```
---
Para retornar a letra de uma música:

```
$ python vagalume.py 'elvis presley' -m 'love me tender'

Buscando por Love Me Tender...

Artista: Elvis-Presley
Compositor: Elvis Presley / Vera Matson
Titulo: Love Me Tender

Letra:

Love me tender, love me sweet,
Never let me go.
You have made my life complete,
And I love you so.

Love me tender, love me true,
All my dreams fulfill.
For my darlin' I love you,
And I always will.

Love me tender, love me long,
Take me to your heart.
For it's there that I belong,
And we'll never part.

Love me tender, love me true,
All my dreams fulfill.
For my darlin' I love you,
And I always will.

Love me tender, love me dear,
Tell me you are mine.
I'll be yours through all the years,
Till the end of time.

Love me tender, love me true,
All my dreams fulfill.
For my darlin' I love you,
And I always will.

Deseja exportar para txt? (s/n):
n
```
---
Help do programa:

`$ python vagalume.py -h`
---
## License

This project is licensed under the MIT License - see [LICENSE](/LICENSE) for details.
