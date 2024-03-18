## Coletor de Dados do Site do Fluminense
Este repositório contém um script em Python para coletar dados do site do Fluminense (https://www.fluminense.com.br/) utilizando as bibliotecas Selenium, Pandas, NumPy, PyYAML, entre outras.

## Funcionalidades
O script automatiza a navegação pelo site do Fluminense para coletar informações específicas.
Os dados coletados são organizados e armazenados em um arquivo CSV para fácil análise.
Utiliza YAML para configurar parâmetros como URL, elementos da página, etc.
Pré-requisitos
Certifique-se de ter as seguintes dependências instaladas:

- Python 3.x
- Selenium
- Pandas
- NumPy
- PyYAML
  
## Como usar
1° Clone este repositório:
```bash
git clone https://github.com/seu_usuario/nome_do_repositorio.git
```
2° Crie um Virtual Envirement:
```bash
python -m venv venv
````
3° Vá para o ambiente virtual (Em Windows): 
```bash
venv/Scripts/activate
```
4° Instale as dependências:
```bash
pip install -r requirements.txt
```
5° Configure as opções no arquivo config.yml.

6° Execute o script fluminense.py:

```bash
python coletor_fluminense.py
```

## Licença
Este projeto é licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
