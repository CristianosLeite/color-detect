# COLOR DETECT

## Sistema para detecção de cores industrial

Este sistema foi projetado pensando em uma solução para detecção de cores em um processo industrial. O sistema é capaz de detectar cores em tempo real e informar ao usuário se a cor detectada está dentro dos padrões definidos pelo próprio usuário.
O sistema conta com uma interface web para configuração dos parâmetros de detecção e e visualização dos resultados em tempo real e uma interface desktop que pode ser carregada em um Raspberry Pi para ser utilizada em um processo industrial como um controlador e visualizador de status do sistema.

## Installation

1. Clone the repository.

```bash
git clone https://github.com/CristianosLeite/color-detect.git
```

2. Install the dependencies.

```bash
cd color-detect/color-detect-back
pip install -r requirements.txt
```
Este projeto foi desenvolvido utilizando o PostgreSQL como banco de dados. Após instalar e configurar o PostgreSQL, creie um arquivo com o nome `credentials.py`:

```bash
touch credentials.py
```

No Windows utilize o comando `type nul > credentials.py` para criar o arquivo.

Declare uma variavel db_credentials no arquivo `credentials.py` com as credenciais do banco de dados:

Exemplo:

```bash
    db_credentials = {
    'DB_NAME': 'postgres',
    'DB_USER': 'postgres',
    'DB_PASSWORD': 'postgres',
    'DB_HOST': 'localhost',
    'DB_PORT': '5432'
    }
```

Ou se preferir utilize variáveis de ambiente para armazenar as credenciais do banco de dados.
Obs: Caso opte por utilizar variáveis de ambiente, é necessário alterar o arquivo `database.py` para que o mesmo utilize as variáveis de ambiente.

3. Run the application.

```bash
python api.py
```

```bash	
python class_interface.py
```

Ao executar o comando a interface desktop e a API serão iniciadas.
Obs: Pode ser necessário executar o comando `python3` ao invés de `python` dependendo da configuração do seu sistema.

## Installation (Frontend)

Para instalar o frontend do projeto, siga os seguintes passos:

1. Go to the `color-detect-front` directory.

```bash
cd ../color-detect-front
```

2. Run `npm install` to install the dependencies.

```bash
npm install
```

3. Run `npm start` to start the application.

```bash
npm start
```

## Usage

A interface web pode ser acessada através do endereço `http://localhost:3000/`.

Após acessar a interface web, é necessário que já tenha um plc conectado à mesma rede para que seja possível a comunicação entre o plc e a interface web.

Alternativamente você pode utilizar um serviço como o [pm2](https://github.com/Unitech/pm2) para iniciar a aplicação em background.

## Contributing

Contributions are welcome! Please follow the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the [GPL-3.0 License](LICENSE).

## Authors

Douglas Venâncio - [@douglasvenancio](https://github.com/faraddouglas)
Cristiano Leite - [@cristianosleite](https://github.com/CristianosLeite)
