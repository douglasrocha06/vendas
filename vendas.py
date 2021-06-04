import pymysql
from app import app3
from config import mysql3
from flask import jsonify
from flask import flash, request
from flask_httpauth import HTTPBasicAuth
import requests

auth = HTTPBasicAuth()

#GET na tabela inventário dos produtos que um cliente adquiriu
@app3.route('/compras/clientes/<int:id_cliente>', methods=['GET'])
@auth.login_required
def vendas_produ(id_cliente):
    try:
        conn = mysql3.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #Traz todas as vendas de um cliente
        cursor.execute("SELECT id_vendas, id_cliente, id_produto, date_format(data_venda, GET_FORMAT(DATE,'EUR')) as 'data_venda' from inventario where id_cliente = %s", id_cliente)
        linha = cursor.fetchall()
        
        cliente = requests.get(url = f'http://loadbalancer-djl-1817009558.us-east-1.elb.amazonaws.com/clientes/{id_cliente}', headers = {'Authorization':'Basic ZG91Z2xhczoxMjM='})

        catalogo2 = [] 
        produtos = []
        for i in (linha):
            if i not in produtos:
                id_produto = i['id_produto']
                produtos.append(id_produto)
                catalogo = requests.get(url = f'http://loadbalancer-djl-1817009558.us-east-1.elb.amazonaws.com/catalogo/{id_produto}', headers = {'Authorization':'Basic ZG91Z2xhczoxMjM='})
                catalogo2.append(catalogo.json())

        if catalogo2 and produtos:
            return jsonify(linha, cliente.json(), catalogo2), 200
        else:
            return jsonify({'status':'Não há compra cadastrada!'}), 400

    except Exception as e:
        return(e)
    finally:
        cursor.close() 
        conn.close()

#Adicionando um registro 
@app3.route('/compras/clientes', methods=['POST'])
@auth.login_required
def adicionar_venda():
    try:
        json = request.json
        id_cliente = json['id_cliente']
        id_produto = json['id_produto']
        data_venda = json['data_venda']

        if id_cliente and id_produto and data_venda and request.method == 'POST':
            sqlQuery = "INSERT INTO inventario(id_cliente, id_produto, data_venda) VALUES(%s, %s, %s)"
            dados = (id_cliente, id_produto, data_venda)
            conn = mysql3.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            #Verificação se os IDs estão nas bases
            cliente = requests.get(url = f'http://loadbalancer-djl-1817009558.us-east-1.elb.amazonaws.com/clientes/{id_cliente}', headers = {'Authorization':'Basic ZG91Z2xhczoxMjM='})
            catalogo = requests.get(url = f'http://loadbalancer-djl-1817009558.us-east-1.elb.amazonaws.com/catalogo/{id_produto}', headers = {'Authorization':'Basic ZG91Z2xhczoxMjM='})

            if cliente.status_code == 404:
                return jsonify({'status':'Cliente inexistente.'}), 400
            elif catalogo.status_code == 404:
                return jsonify({'status':'Produto inexistente.'}), 400

            cursor.execute(sqlQuery, dados)
            conn.commit()
            resposta = jsonify({'status':"Compra cadastrada com sucesso!"})
            resposta.status_code = 200
            return resposta
        else:
            return not_found
    except Exception as e:
        return jsonify({"error":f"{e}"})
    finally:
        cursor.close()
        conn.close()

#Atualizando uma venda
@app3.route('/compras/clientes', methods=['PUT'])
@auth.login_required
def atualizar_venda():
    try:
        conn = mysql3.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json = request.json
        id_vendas = json['id_vendas']
        id_cliente = json['id_cliente']
        id_produto = json['id_produto']
        data_venda = json['data_venda']

        if id_vendas and id_cliente and id_produto and data_venda and request.method == 'PUT':
            sqlQuery = "SELECT * FROM inventario where id_vendas=%s"
            cursor.execute(sqlQuery, id_vendas)
            linha = cursor.fetchone()

            if not linha:
                return jsonify({'status':'Compra não cadastrada!'})
            sqlQuery = "UPDATE inventario SET id_cliente=%s, id_produto=%s, data_venda= %s WHERE id_vendas=%s"
            dados = (id_cliente, id_produto, data_venda, id_vendas)

            #Verificação se os IDs estão nas bases
            cliente = requests.get(url = f'http://loadbalancer-djl-1817009558.us-east-1.elb.amazonaws.com/clientes/{id_cliente}', headers = {'Authorization':'Basic ZG91Z2xhczoxMjM='})
            catalogo = requests.get(url = f'http://loadbalancer-djl-1817009558.us-east-1.elb.amazonaws.com/catalogo/{id_produto}', headers = {'Authorization':'Basic ZG91Z2xhczoxMjM='})

            if cliente.status_code == 404:
                return jsonify({'status':'Cliente inexistente.'}), 400
            elif catalogo.status_code == 404:
                return jsonify({'status':'Produto inexistente.'}), 400

            cursor.execute(sqlQuery, dados)
            conn.commit()
            resposta = jsonify({'status':'Compra alterada com sucesso!'})
            resposta.status_code = 200
            return resposta
        else:
            return not_found
    except Exception as e:
        return jsonify({"error":f"{e}"})
    finally:
        cursor.close()
        conn.close()

#Método DELETE
@app3.route('/compras/clientes/<int:id_vendas>', methods=['DELETE'])
@auth.login_required
def deletar_venda(id_vendas):
	try:
		conn = mysql3.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sqlQuery = "SELECT * FROM inventario where id_vendas=%s"
		cursor.execute(sqlQuery, id_vendas)
		linha = cursor.fetchone()

		if not linha:
		    return jsonify({'status':'Registro de venda inexistente!'}), 404

		else:
			cursor.execute("DELETE FROM inventario where id_vendas=%s", (id_vendas))
			conn.commit()
			resposta = jsonify({'Status':'Registro de venda exluído com sucesso!'})
			resposta.status_code = 200
			return resposta

	except Exception as e:
		return jsonify({'error':f'{e}'})
	finally:
		cursor.close()
		conn.close()

#Caso não encontre o caminho
@app3.errorhandler(404)
def not_found(error=None):
    messagem = {
        'status': 404,
        'mensagem': 'Registro não encontrado: ' + request.url,
    }
    respone = jsonify(messagem)
    respone.status_code = 404
    return respone

#Método de verificação de senha
@auth.verify_password
def verificacao(login, senha):
	usuarios= {
			'douglas':'123',
			'cristhian':'321'
	}
	#Valida se o login existe
	if not (login, senha): #Se não for igual retorna false
		return False
	return usuarios.get(login) == senha
		
if __name__ == "__main__":
    app3.run(debug=True, host="0.0.0.0", port=80)
