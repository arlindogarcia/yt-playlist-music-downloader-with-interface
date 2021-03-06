import ctypes
# Retira console ao iniciar
ctypes.windll.kernel32.FreeConsole()
from pytube import YouTube
from pytube import Playlist
from datetime import date
import PySimpleGUI as sg
import tkinter
import os
import requests

def verificaArquivoExistente(diretorio):
    return os.path.isfile(diretorio)

def criaDiretorio(diretorio):
    if not os.path.isdir(diretorio):
        os.makedirs(diretorio)

def muliplosReplaces(texto):
    for char in '/.:;|,\'"#$%':
        texto = texto.replace(char, "")
    return texto

def diretorioPadrao():
    return os.path.join(os.path.expanduser("~\Desktop"), "Musicas " + date.today().strftime('%d-%m-%Y'))

def main():
    data = []

    layout = [
        [
            sg.Text(
                'Link Playlist',
                size=(9)
            ),
            sg.Input(
                key='link',
                size=(99, 2)
            )
        ],
        [
            sg.Text(
                'Diretório',
                size=(9),
            ),
            sg.In(
                size=(81,1),
                enable_events=True,
                key='diretorio',
                readonly=True,
                default_text=diretorioPadrao()
            ),
            sg.FolderBrowse()
        ],
        [
            sg.Button(
                'Baixar'
            ),
            sg.Button(
                'Sair',
                button_color=(
                    'white',
                    'firebrick3'
                )
            ),
            sg.Text(
                '0% - 0/0',
                size=(15),
                key='detalhe_progresso',
                justification='right'
            ),
            sg.ProgressBar(
                1,
                orientation='h',
                size=(55, 20),
                bar_color=[
                    'Green',
                    'White'
                ],
                key='progresso',
            )
        ],
        [
            sg.Table(
                values=data, 
                headings=[
                    'Status',
                    'Música'
                ], 
                auto_size_columns=False,
                justification='left',
                num_rows=15, 
                alternating_row_color=sg.theme_button_color()[1],
                row_height=20,
                display_row_numbers=False,
                expand_x=True,
                expand_y=True, 
                key='table',
                col_widths=[8,77],
                vertical_scroll_only=True,
            )
        ]
    ]

    janela = sg.Window(
        'Baixar Playlist de Músicas do YouTube',
        layout,
        size=(750,450)
    )

    while True:
        evento, values = janela.Read()
            
        if evento in ('Sair', None): break
        if evento == 'Baixar':
            link =  values['link']
            diretorio = values['diretorio']

            if link == "":
                tkinter.messagebox.showerror(title="Erro", message="Preencha o link da playlist!")
            else:
                try:
                    item_atual = 0

                    if requests.get(link).status_code != 200:
                        tkinter.messagebox.showerror(title="Erro", message="Link inválido!")

                    # Busca Playlist
                    yt = Playlist(link)

                    total_itens = len(yt.video_urls)

                    if total_itens == 0:
                        tkinter.messagebox.showerror(title="Erro", message="Essa playlist possui 0 músicas!")
                    else:
                        criaDiretorio(diretorio)

                    for url in yt.video_urls:
                        item_atual += 1
                        status_musica = ''
                        ys = YouTube(url)

                        # Caso o arquivo existir ir pra próxima música
                        if verificaArquivoExistente(diretorio + "\\" + muliplosReplaces(ys.title) + ".mp3"):
                            status_musica = 'JÁ EXISTE'
                        else:
                            status_musica = 'BAIXADO'

                        # Atualiza tabela
                        data.append([status_musica, ys.title])
                        janela.Element('table').Update(values=data, num_rows=len(data))
                        janela.Element('progresso').UpdateBar(item_atual, total_itens)
                        janela.Element('detalhe_progresso').Update(str(round((item_atual*100)/total_itens,1)) + '% - ' + str(item_atual) + "/" + str(total_itens))
                        janela.refresh()

                        if (status_musica == 'JÁ EXISTE'):
                            continue

                        # Baixa arquivo e pega diretório
                        arquivo_saida = ys.streams.get_audio_only().download(diretorio)

                        # Troca a extensão do arquivo de .mp4 para .mp3
                        base, ext = os.path.splitext(arquivo_saida)
                        novo_arquivo = base + '.mp3'
                        os.rename(arquivo_saida, novo_arquivo)

                    tkinter.messagebox.showinfo(title="Sucesso!", message="Downloads concluidos!")

                except Exception as e:
                    tkinter.messagebox.showerror(title="Erro", message="Erro! Verifique o link ou o diretório especificado.")

main()