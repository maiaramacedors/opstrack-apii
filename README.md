# OpsTrack API

A OpsTrack API é uma API em Python com Flask para acompanhamento de chamados (tickets) de suporte técnico. Ela informa se o serviço está online e lista os chamados e os usuários cadastrados. Projeto da disciplina de Integração e Entrega Contínua (ISW-032 — Fatec).

O projeto usa **flake8** para análise estática de código, **pre-commit** para barrar automaticamente commits com erros de lint e **pytest** com **pytest-cov** para os testes automatizados e a cobertura de código.

---

## 1. Pré-requisitos

Antes de começar, tenha instalado na sua máquina:

- **Python 3.12** ou superior — confira com `python --version`
- **Git** — confira com `git --version`
- Acesso à internet (o pre-commit baixa o flake8 no primeiro commit)

---

## 2. Configurando o ambiente

Siga os passos **na ordem**. Os comandos são executados no terminal.

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/maiaramacedors/opstrack-apii.git
cd opstrack-apii
```

### Passo 2 — Criar o ambiente virtual

```bash
python -m venv venv
```

> **Windows:** se aparecer "Python não foi encontrado", use `py` no lugar de `python`: `py -m venv venv`

### Passo 3 — Ativar o ambiente virtual

Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

Windows (Prompt de Comando / cmd):

```cmd
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

O prompt do terminal passa a mostrar `(venv)`. **Todos os passos seguintes precisam ser feitos com o venv ativo.**

> Se o PowerShell bloquear a ativação com um erro de "execução de scripts", rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo.

> **Moveu a pasta do projeto de lugar?** O venv guarda o caminho da pasta onde foi criado e para de funcionar se ela for movida (aparece "'flake8' não é reconhecido"). Nesse caso, apague a pasta `venv` e refaça os passos 2 a 5.

### Passo 4 — Instalar as dependências

```bash
pip install -r requirements-dev.txt
```

Esse arquivo inclui as dependências da aplicação (`requirements.txt`) e as ferramentas de desenvolvimento (flake8, pre-commit, pytest e pytest-cov).

### Passo 5 — Ativar o hook do pre-commit

```bash
pre-commit install
```

Você deve ver:

```
pre-commit installed at .git/hooks/pre-commit
```

> **Atenção:** este passo é obrigatório em **cada clone**, em cada máquina. O arquivo `.pre-commit-config.yaml` vem junto com o repositório, mas o hook ativo fica na pasta `.git/hooks/`, que não é versionada. Sem o `pre-commit install`, commits com erro passam sem aviso.

### Passo 6 — Conferir se está tudo certo

```bash
pre-commit run --all-files
pytest
```

Resultado esperado:

```
flake8...................................................................Passed
```

```
Required test coverage of 85% reached.
7 passed
```

Na primeira execução do pre-commit aparecem linhas `[INFO]` enquanto o flake8 é baixado. Isso é normal e pode levar alguns minutos.

---

## 3. Executando a aplicação

Com o venv ativo, na raiz do projeto:

```bash
flask --app app run
```

O terminal mostra `Running on http://127.0.0.1:5000`. Abra no navegador:

| Endereço                       | O que retorna                                     |
| ------------------------------ | ------------------------------------------------- |
| http://127.0.0.1:5000/         | `{"servico": "OpsTrack API", "status": "online"}` |
| http://127.0.0.1:5000/status   | `{"status": "ok"}`                                |
| http://127.0.0.1:5000/version  | `{"versao": "0.1.0"}`                             |
| http://127.0.0.1:5000/tickets  | `{"tickets": [...]}` com 2 chamados               |
| http://127.0.0.1:5000/usuarios | `{"usuarios": [...]}` com 2 usuários              |
| http://127.0.0.1:5000/sobre    | `{"nome": "OpsTrack API", "versao": "1.0.0"}`     |
| qualquer outra rota            | erro 404 (Not Found)                              |

Para parar a API, pressione `Ctrl+C` no terminal.

---

## 4. Rodando os testes

Os testes ficam na pasta `tests/` e usam o **pytest**. A configuração fica no arquivo `pytest.ini`, na raiz do projeto.

```
opstrack-apii/
    app.py
    pytest.ini
    tests/
        conftest.py      -> cria o client de teste (fixture)
        test_api.py      -> os testes de cada rota
```

### Rodando todos os testes

Com o venv ativo, na raiz do projeto:

```bash
pytest
```

O `pytest.ini` já faz o pytest medir a cobertura de código do `app.py` e mostrar as linhas não testadas. Resultado esperado:

```
Name     Stmts   Miss  Cover   Missing
--------------------------------------
app.py      22      1    95%   50
--------------------------------------
TOTAL       22      1    95%
Required test coverage of 85% reached. Total coverage: 95.45%
7 passed
```

- Cada `.` na linha `tests\test_api.py .......` é um teste que passou. Um `F` é um teste que falhou.
- A coluna **Missing** mostra as linhas do `app.py` que nenhum teste executa.

### O que é testado

| Teste                                        | O que confere                                      |
| -------------------------------------------- | -------------------------------------------------- |
| `test_raiz_informa_servico_online`           | `/` devolve o nome do serviço e o status online    |
| `test_status_retorna_ok`                     | `/status` devolve `"ok"`                           |
| `test_tickets_retorna_lista_com_id_e_titulo` | `/tickets` devolve os chamados com `id` e `titulo` |
| `test_usuarios_retorna_dois_usuarios`        | `/usuarios` devolve exatamente 2 usuários          |
| `test_rota_inexistente_retorna_404`          | uma rota que não existe devolve 404                |
| `test_version_retorna_versao`                | `/version` devolve a versão `0.1.0`                |
| `test_sobre_retorna_nome_e_versao`           | `/sobre` devolve o nome e a versão da API          |

### Meta de cobertura: 85%

O pytest está configurado com `--cov-fail-under=85`: se a cobertura do `app.py` ficar **abaixo de 85%**, o comando `pytest` termina com erro, mesmo que todos os testes passem.

**Por que 85%:** é uma meta alta o bastante para garantir que todas as rotas da API tenham teste, mas deixa margem para linhas que não fazem sentido testar. Hoje a cobertura é de 95%, então a meta também protege contra regressões: se alguém criar uma rota nova sem teste, a cobertura cai e o problema aparece.

**A linha que fica sem teste:** a linha 50 (`app.run(debug=True)`) só é executada quando o app é iniciado direto com `python app.py`. Os testes usam o `client` do Flask e não sobem o servidor, então essa linha não é coberta. Testá-la não traria ganho, por isso a equipe optou por não usar `# pragma: no cover` e manter a meta com essa margem.

### Quando um teste falha

Leia a linha que começa com **`E`** no bloco `FAILURES`: ela mostra o valor esperado e o valor obtido. Por exemplo:

```
E       assert 'oks' == 'ok'
```

Significa que o teste esperava `"ok"`, mas a rota devolveu `"oks"`. O rodapé (`tests\test_api.py:31`) indica o arquivo e a linha do teste.

---

## 5. Qualidade de código

### Rodando o flake8 manualmente

```bash
flake8 .
```

Se o comando terminar **sem exibir nenhuma linha**, o código está dentro do padrão. Cada apontamento segue o formato:

```
arquivo:linha:coluna: CÓDIGO mensagem
```

Exemplo: `utils.py:3:5: F841 local variable 'sobra' is assigned to but never used`

- Códigos **E** e **W**: estilo (PEP 8), como linhas em branco ou linhas longas.
- Códigos **F**: erros lógicos prováveis, como imports ou variáveis não usados.

A configuração fica no arquivo `.flake8`, que ignora pastas que não são código da equipe (`venv`, `__pycache__`, `.git`).

### O que o hook faz a cada commit

Ao rodar `git commit`, o pre-commit executa o flake8 nos arquivos `.py` que estão na área de staging:

- **Sem apontamentos** → `Passed` e o commit é criado.
- **Com apontamentos** → `Failed`, o commit é **bloqueado** e os erros aparecem no terminal.

Para corrigir um commit bloqueado:

1. Abra o arquivo na linha indicada e corrija o problema.
2. Salve o arquivo (`Ctrl+S`).
3. Rode `git add <arquivo>` de novo (o hook analisa a versão que está no staging).
4. Rode o `git commit` novamente.

### Testando se o hook está funcionando

Crie um arquivo `teste_hook.py` com uma variável não usada:

```python
def teste():
    sobra = 42
    return 1
```

```bash
git add teste_hook.py
git commit -m "teste: hook deve barrar"
```

O resultado deve ser `Failed` com o código `F841`. Depois desfaça o teste:

```bash
git restore --staged teste_hook.py
```

E apague o arquivo `teste_hook.py`.

> Se o commit passar mesmo com o erro, o hook não está ativo: volte ao **Passo 5** com o venv ativo.

---

## 6. Como contribuir

Nenhuma alteração vai direto para a `main`. O fluxo é:

1. Atualize a `main` local:

```bash
   git checkout main
   git pull
```

2. Crie uma branch para a sua tarefa:

```bash
   git checkout -b feature/nome-da-tarefa
```

3. Faça as alterações e rode os testes antes de commitar:

```bash
   pytest
```

4. Commite (o hook roda o flake8 automaticamente):

```bash
   git add .
   git commit -m "feat: descreve a alteração"
```

Use prefixos nas mensagens: `feat:` (nova funcionalidade), `fix:` (correção), `chore:` (configuração/manutenção), `docs:` (documentação), `test:` (testes).

5. Envie a branch para o GitHub:

```bash
   git push -u origin feature/nome-da-tarefa
```

6. No GitHub, abra um **Pull Request** para a `main`, peça revisão e faça o merge após a aprovação.

### Observações

- Não use `git commit --no-verify` para pular o hook, exceto em emergência.
- Não gere o `requirements.txt` com `pip freeze`: ele passaria a incluir o flake8, o pre-commit, o pytest e as dependências deles. Ferramentas de desenvolvimento vão no `requirements-dev.txt`.
- Toda rota nova deve vir com pelo menos um teste em `tests/test_api.py`, para a cobertura não cair abaixo da meta.
