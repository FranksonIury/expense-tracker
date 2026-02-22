import argparse
import json
import os
import csv

parser = argparse.ArgumentParser (prog="Expense Tracker", description= "A CLI for manage and track your expenses ")

subparsers = parser.add_subparsers(dest="command", required=True)
#-----ADD-----
parser_add = subparsers.add_parser("add", help="Add the expense ")
parser_add.add_argument("name", help="Write the name of expense ")
parser_add.add_argument("-d", "--description", help="Write the description of the expense ")
parser_add.add_argument("value", type=int, help="Add the value of the expense ")
parser_add.add_argument("month", type=int, help="Add the month of the the expense ")
#-----UPDATE-----
parser_up = subparsers.add_parser("up", help="Update the expense ")
parser_up.add_argument("id", help="Choose the expense id for update ")
parser_up.add_argument("to_up", help="Choose wich part of expense you want to update ")
parser_up.add_argument("new_value", help="Choose the new value ")
#-----LIST-----
parser_view = subparsers.add_parser("list", help="List all expenses ")
#-----AMOUNT-----
parser_amount = subparsers.add_parser("amount", help="Shows the total or especific amount expenses ")
parser_amount.add_argument("-m", "--month", type=int, help="Shows the amount of an especific month expenses ")
parser_amount.add_argument("-t", "--total", action="store_true", help="Shows the total amount of expenses ")
#-----DELETE-----
parser_delete = subparsers.add_parser("delete", help="Delete the expense ")
parser_delete.add_argument("delnumber", type=int, help= "Choose the number of expense ")
parser_delete.add_argument("--yes", action="store_true", help="Agree ")
#-----EXPORT-----
parser_export = subparsers.add_parser("export", help="Export to a CSV file ")

args = parser.parse_args()
def estrutura_padrao():
    return {"last_id": 0,
            "despesas": {}}

def ler_dados():
    if os.path.exists("dados.json"):
        try:
            with open ("dados.json", "r",encoding="UTF-8") as arquivo:
                dados = json.load(arquivo)
                if "last_id" not in dados or "despesas" not in dados:
                    print("Invald structure in JSON. Reseting file ")
                    dados = estrutura_padrao()
                    escrever_dados(dados)
                    return dados
            return dados
        except json.JSONDecodeError:
            print("JSON file corrupted. Reseting file")
            dados = estrutura_padrao()
            escrever_dados(dados)
            return dados
        except Exception as e:
            print (f"Unexpected error: {e}")
            exit()
    else:
        with open("dados.json", "w", encoding="UTF-8") as arquivo:
            estrutura_inicial = {"last_id": 0,
                                 "despesas": {}}
            json.dump((estrutura_inicial), arquivo, indent=4)
            return {"last_id": 0,
                    "despesas": {}}

def escrever_dados(dados):
    with open("dados.json", "w", encoding="UTF-8")as arquivo:
        json.dump(dados, arquivo, indent=4)

#Adiciona uma despesa com nome, valor, mês e descrição
if args.command == "add":
    dados = ler_dados()
    valid_months = [1,2,3,4,5,6,7,8,9,10,11,12]
    if args.month not in valid_months:
        print ("Just can add months in range 1-12")
    elif args.month in valid_months:
        novo_id = dados["last_id"]+1
        nova_despesa = {"name": args.name,
                        "value": args.value,
                        "description": args.description,
                        "month": args.month}
        dados["despesas"][str(novo_id)] = (nova_despesa)
        dados["last_id"] = novo_id
        escrever_dados(dados)
        print(f"Despesa {novo_id} adicionada com sucesso! ")
#Atualiza uma despesa
if args.command == "up":
    dados = ler_dados()
    if args.id in dados["despesas"]:
        if args.to_up in ["name", "value", "description", "month"]:
            if args.to_up=="month":
                valid_months = [1,2,3,4,5,6,7,8,9,10,11,12]
                if int(args.new_value) not in valid_months:
                    print ("Just can add months in range 1-12")
                    exit()
                else:
                    dados["despesas"][args.id][args.to_up] = int(args.new_value)
            elif args.to_up=="value":
                try:
                    args.new_value = int(args.new_value)
                except ValueError:
                    print("Value must be an integer. ")
                    exit()
                dados["despesas"][args.id]["value"]= (args.new_value)
            else:
                dados["despesas"][args.id][args.to_up] = (args.new_value)
            escrever_dados(dados)
        else:
            print("Invalid field. Choose: name, value, description or month ")
    else:
        print("This id not exists. Verify the expenses list ")
#Lista as despesas
if args.command=="list":
    dados = ler_dados()
    for i in dados["despesas"]:
        print (f"id {i}: {dados['despesas'][i]['name']}, valor: {dados['despesas'][i]['value']}, mês: {dados['despesas'][i]['month']}, description: {dados['despesas'][i]['description']}\n")
#Mostra o montante das despesas
if args.command=="amount":
    dados = ler_dados()
    amount = 0
    if args.total:                  #Se a flag total for escolhida, todos os valores vão ser passados
        for i in dados["despesas"]:
            amount = amount+dados["despesas"][i]["value"]
        print(f"The total amount is {amount}")
    elif args.month:                #Se a flag month for escolhida, apenas o mês selecionado vai ser contado
        for i in dados["despesas"]:
            if dados["despesas"][i]["month"]==args.month:
                amount = amount+dados["despesas"][i]["value"]
        print(f"The amount of month {args.month} is {amount}")
#Deleta a despesa 
if args.command=="delete":
    dados = ler_dados()
    if str(args.delnumber) not in dados["despesas"]:
        print("ID not found. Use the command 'list' for see the ID's ")
    elif args.yes:
        del dados["despesas"][str(args.delnumber)]
        escrever_dados(dados)
        print(f"Delete the expense {args.delnumber} succesfully ")
    else:
        print(f"The task {args.delnumber} was not deleted. Please confirm with --yes")

def exportar_csv():
    dados = ler_dados()
    with open("despesas.csv", "w",newline="", encoding="UTF-8") as arquivo:
        writer = csv.writer(arquivo, delimiter=";")
        #cabecalho
        writer.writerow(["id", "name", "value", "month", "description"])
        #linhas
        for id, despesa in dados["despesas"].items():
            writer.writerow([
            id,
            despesa["name"],
            despesa["value"],
            despesa["month"],
            despesa["description"]
            ])
if args.command=="export":
    exportar_csv()
    