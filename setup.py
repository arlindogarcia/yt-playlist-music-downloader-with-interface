from cx_Freeze import setup, Executable

setup(
    name="PlaylistDownloader",
    version="0.1",
    description="DownloadPlaylist - v1.0",
    options = {
        "build_exe": {
            "include_files":["icone.ico"],
            "packages": ["os","pytube","datetime","PySimpleGUI","tkinter","requests","ctypes"],
        },
        "bdist_msi": 
        {'data': 
            {"Shortcut": 
                [
                    ("DesktopShortcut",
                    "DesktopFolder",
                    "PlaylistDownloader",
                    "TARGETDIR",
                    "[TARGETDIR]DownloadPlaylistMusicaYoutube.exe",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    'TARGETDIR'
                    )
                ] 
            }
        },
    },
    executables = [
        Executable(
            "DownloadPlaylistMusicaYoutube.py", base=None,icon="icone.ico"
        )
    ]
)