def test_raiz_informa_servico_online(client):
    # Arrange: o client vem da fixture (tests/conftest.py)
    # Act
    resposta = client.get('/')
    # Assert
    assert resposta.status_code == 200
    esperado = {'servico': 'OpsTrack API', 'status': 'online'}
    assert resposta.get_json() == esperado


def test_status_retorna_ok(client):
    resposta = client.get('/status')
    assert resposta.status_code == 200
    assert resposta.get_json()['status'] == 'ok'


def test_tickets_retorna_lista_com_id_e_titulo(client):
    resposta = client.get('/tickets')
    tickets = resposta.get_json()['tickets']
    assert resposta.status_code == 200
    assert len(tickets) >= 1
    assert 'id' in tickets[0]
    assert 'titulo' in tickets[0]


def test_usuarios_retorna_dois_usuarios(client):
    # Arrange: client pronto.
    # Act: faca um GET em /usuarios e guarde em "resposta".
    resposta = client.get('/usuarios')
    # Assert: status 200 e exatamente 2 usuarios na lista.
    assert resposta is not None, 'Complete o Act: faca o GET em /usuarios'
    assert resposta.status_code == 200
    assert len(resposta.get_json()['usuarios']) == 2


def test_rota_inexistente_retorna_404(client):
    # Act: peca uma rota que nao existe, por exemplo /nao-existe.
    resposta = client.get('/nao-existe')
    # Assert: o status deve ser 404.
    assert resposta is not None, 'Complete o Act: GET em rota inexistente'
    assert resposta.status_code == 404


def test_version_retorna_versao(client):
    resposta = client.get('/version')
    assert resposta.status_code == 200
    j = resposta.get_json()
    assert j['versao'] == '0.1.0'


def test_sobre_retorna_nome_e_versao(client):
    resposta = client.get('/sobre')
    assert resposta.status_code == 200
    j = resposta.get_json()
    assert j['nome'] == 'OpsTrack API'
    assert j['versao'] == '1.0.0'
