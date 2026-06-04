# Progetto 2
Il seguente progetto è diviso in due parti principali, la prima è lo sviluppo di 
una DCT "fatta in casa" confrontandola con la FFT della libreria **Scipy**. 
La seconda parte comprende lo sviluppo di un'interfaccia che implementa un 
algoritmo di compressione direttamente sulle immagini (.bmp).  
Il progetto è interamente fatto in Python (3.11.4) e l'interfaccia 
è sviluppata in Qt per Python (con PySide 6)

## How to run
Innanzitutto è necessario scaricare le librerie esterne:
1. numpy
2. scipy
3. matplotlib 
4. PySide6  

Solitamente è consigliato creare una cartella *venv* per contenere le librerie, anche se non è necessaria, si crea con:
```
python -m venv .venv
```
E si attiva con:
**Windows**
```
.venv\Scripts\activate
```
**Linux/macOS**
```
source .venv/bin/activate
```
Successivamente è possibile installare tutte le librerie con:
```
pip install -r requirements.txt
```
Oppure singolarmente con:
```
pip install <NOME_LIBRERIA>
```

Successivamente, per eseguire l'interfaccia (dalla cartella /src) bisogna lanciare il comando:
```
python main.py
```
Invece per lanciare i benchmark (dalla cartella /src/test):
```
python test.py
```
