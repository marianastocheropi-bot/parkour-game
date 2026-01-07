import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Configuração do Servidor
app = Flask(__name__)
app.config['SECRET_KEY'] = 'robo_arabe_v3_secret'

# SocketIO configurado para alta performance (essencial para o Robô Árabe)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Banco de dados temporário dos jogadores online
players = {}

@app.route('/')
def index():
    # Isso vai procurar o arquivo dentro da pasta /templates
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("⚓ Um novo Agente tentou conexão, senhor!")

@socketio.on('join')
def handle_join(data):
    user = data.get('user', 'Agente_Desconhecido')
    players[user] = {'x': 0, 'y': 0, 'z': 0, 'ry': 0}
    emit('update_list', list(players.keys()), broadcast=True)
    print(f"⚓ Senhor, o Agente {user} entrou no Parkour-Game!")

@socketio.on('move')
def handle_move(data):
    user = data.get('user')
    if user:
        players[user] = data
        # Envia a posição para todos, menos para quem enviou (economiza dados)
        emit('update_positions', players, broadcast=True, include_self=False)

if __name__ == '__main__':
    # O Render/Railway vai injetar a porta automaticamente aqui
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
