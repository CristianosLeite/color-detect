// Cria uma nova conexão websocket para o status da câmera
var socketCamera = new WebSocket("ws://localhost:8765");

// Atualiza o elemento HTML apropriado quando uma mensagem é recebida do servidor
socketCamera.onmessage = function (event) {
    if (event.data === 'True') {
        document.querySelector("#status-camera").value = 'Câmera Conectada';
        document.querySelector("#status-camera").style.backgroundColor = 'green';
    } else {
        document.querySelector("#status-camera").value = 'Câmera Desconectada';
        document.querySelector("#status-camera").style.backgroundColor = 'red';
    }
};

// Cria uma nova conexão websocket para o status do PLC
var socketPlc = new WebSocket("ws://localhost:8766");

// Atualiza o elemento HTML apropriado quando uma mensagem é recebida do servidor
socketPlc.onmessage = function (event) {
    if (event.data === 'True') {
        document.querySelector("#status-plc").value = 'Plc conectado';
        document.querySelector("#status-plc").style.backgroundColor = 'green';
    } else {
        document.querySelector("#status-plc").value = 'Plc desconectado';
        document.querySelector("#status-plc").style.backgroundColor = 'red';
    }
};

// Cria uma nova conexão websocket para o status da API
var socketApi = new WebSocket("ws://localhost:8767");

// Atualiza o elemento HTML apropriado quando uma mensagem é recebida do servidor
socketApi.onmessage = function (event) {
    const regex = /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/;
    if (regex.test(event.data)) { 
        document.querySelector("#ip").value = event.data;
        document.querySelector("#ip").style.backgroundColor = 'green';
    } else {
        document.querySelector("#ip").value = event.data;
        document.querySelector("#ip").style.backgroundColor = 'red';
    }
};

// Pega os botões pelo ID
var restartButton = document.querySelector("#restart");
var shutdownButton = document.querySelector("#shutdown");

// Adiciona um evento de clique para o botão de reiniciar
restartButton.addEventListener('click', function() {
    // Faz uma requisição POST para o servidor para reiniciar o sistema
    fetch('/restart', {method: 'POST'})
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
});

// Adiciona um evento de clique para o botão de desligar
shutdownButton.addEventListener('click', function() {
    // Faz uma requisição POST para o servidor para desligar o sistema
    fetch('/shutdown', {method: 'POST'})
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
});
