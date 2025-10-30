#!/bin/bash
echo "🔮 Avvio installazione dell'app Oroscopo Astrale..."

# Controlla che Python3 sia installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Errore: Python3 non trovato. Installa con: sudo apt install python3-full"
    exit 1
fi

# Crea l'ambiente virtuale se non esiste
if [ ! -d "venv" ]; then
    echo "✨ Creazione ambiente virtuale..."
    python3 -m venv venv
else
    echo "🪄 Ambiente virtuale già esistente."
fi

# Attiva l'ambiente
echo "⚙️  Attivazione ambiente virtuale..."
source venv/bin/activate

# Installa i pacchetti necessari
echo "📦 Installazione dipendenze..."
pip install --upgrade pip
pip install flask pyswisseph geopy gpt4all

# Verifica installazione
if [ $? -ne 0 ]; then
    echo "❌ Errore durante l'installazione dei pacchetti."
    deactivate
    exit 1
fi

# Avvia l'app
echo "🚀 Avvio dell'app Flask..."
python app.py

# Disattiva l'ambiente alla chiusura
deactivate
