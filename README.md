# Comment ça marche 

## Pour tester le projet
1. Installez les dépendances avec `pip install -r requirements.txt`
2. Lancez le projet avec `python main.py`

## Pour créer un .exe
1. Installez PyInstaller avec `pip install pyinstaller`
2. Exécutez la commande suivante :
`pyinstaller --onefile --noconsole --add-data "data:data" --add-data "style:style" --add-data "assets:assets" main.py`