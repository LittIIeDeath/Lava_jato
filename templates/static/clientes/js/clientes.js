function add_carro(){

    container = document.getElementById("form-carro")

    html = "<br><div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro'></div> <div class='col-md'> <input type='text' placeholder='Placa' class='form-control' name='placa'></div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'></div></div>"

    container.innerHTML += html
}

function exibir_form(tipo){
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if (tipo == 1){
        add_cliente.style.display = 'block'
        att_cliente.style.display = 'none'
    }
    if (tipo == 2){
        add_cliente.style.display = 'none'
        att_cliente.style.display = 'block'
    }
}

function dados_cliente(){
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result){
        return result.json()
    }).then(function(data){
        document.getElementById('form-att-cliente').style.display = 'block'

        document.getElementById('cliente_id').value = data['cliente_id']
        document.getElementById('nome').value = data['cliente']['nome']
        document.getElementById('sobrenome').value = data['cliente']['sobrenome']
        document.getElementById('cpf').value = data['cliente']['cpf']
        document.getElementById('email').value = data['cliente']['email']

        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ''

        for(i=0; i<data['carros'].length; i++){
            div_carros.innerHTML += "<form action='/clientes/update_carro/" + data['carros'][i]['id'] + "' method='POST'>\
            <div class='row'>\
            <div class='col-md'>\
                <input type='text' class='form-control' name='carro' value='" + data['carros'][i]['fields']['carro'] + "'>\
            </div>\
            <div class='col-md'>\
                <input type='text' class='form-control' name='placa' value='" + data['carros'][i]['fields']['placa'] + "'>\
            </div>\
            <div class='col-md'>\
                <input type='text' class='form-control' name='ano' value='" + data['carros'][i]['fields']['ano'] + "'>\
            </div>\
            <div class='col-md'>\
                <input type='submit' class='btn btn-success' value='Salvar'>\
            </div>\
            </form>\
            <div class='col-md'>\
                <a class='btn btn-danger' href='/clientes/excluir_carro/" + data['carros'][i]['id'] + "'>Excluir</a>\
            </div>\
        </div><br>"
        }
    })
}

function update_cliente(){
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    id = document.getElementById('cliente_id').value

    fetch('/clientes/update_cliente/' + id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf
        })
    }).then(function(result){
        return result.json()
    }).then(function(data){
        if(data['status'] == '200'){
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            console.log('Dados alterados com sucesso')
        }else if(data['status'] == '201'){
            console.log('cpf ja cadastrado')
        }else if(data['status'] == '202'){
            console.log('email ja cadastrado')
        }else if(data['status'] == '203'){
            console.log('email invalido')
        }
        else{
            console.log('Ocorreu algum erro')
        }
    })
}
