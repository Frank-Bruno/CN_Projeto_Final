import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
#import matplotlib.pyplot as plt
import datetime
#from collect_db_data import  get_campus_data
from influxdb_client import InfluxDBClient
import pandas as pd


def get_nearest_tide_level(date_hour, tide_data):
    # Converter a coluna de data e hora do mapa das marés para datetime
    tide_data['DateTime'] = pd.to_datetime(tide_data['Date'] + ' ' + tide_data['Hour'], format='%d %H:%M:%S')
    # Converter a data e hora de entrada para datetime
    input_datetime = pd.to_datetime(date_hour, format='%d %H:%M')
    # Encontrar a data e hora mais próxima
    nearest_datetime = min(tide_data['DateTime'], key=lambda x: abs(x - input_datetime))
    # Retornar o nível da maré correspondente
    return tide_data[tide_data['DateTime'] == nearest_datetime]['Tide_Level'].values[0]

def fuzzy_algorithm(values): 
    # Definindo as variáveis fuzzy de entrada
    temperatura = ctrl.Antecedent(np.arange(-10, 45, 1), 'temperatura')
    umidade = ctrl.Antecedent(np.arange(0, 100, 1), 'umidade')
    #nivel_mare_previsto = ctrl.Antecedent(np.arange(0, 5, 0.1), 'nivel_mare_previsto')
    nivel_mare_previsto = ctrl.Antecedent(np.arange(0, 5, 0.1), 'nivel_mare_previsto')

    # Definindo a variável fuzzy de saída
    #nivel_rio = ctrl.Consequent(np.arange(0, 10, 0.1), 'nivel_rio')
    probabilidade_alagamento = ctrl.Consequent(np.arange(0, 101, 1), 'probabilidade_alagamento')


    # Definindo os conjuntos fuzzy para cada variável
    # Entradas
    temperatura['baixa'] = fuzz.trimf(temperatura.universe, [-10, 0, 23])
    temperatura['media'] = fuzz.trimf(temperatura.universe, [20, 25, 35])
    temperatura['alta'] = fuzz.trimf(temperatura.universe, [30, 40, 45])

    umidade['baixa'] = fuzz.trimf(umidade.universe, [0, 20, 35])
    umidade['moderada'] = fuzz.trimf(umidade.universe, [30, 50, 60])
    umidade['alta'] = fuzz.trimf(umidade.universe, [55, 70, 100])

    #nivel_mare_previsto['baixa'] = fuzz.trimf(nivel_mare_previsto.universe, [0, 0, 1.5])
    #nivel_mare_previsto['media'] = fuzz.trimf(nivel_mare_previsto.universe, [1, 2.5, 4])
    #nivel_mare_previsto['alta'] = fuzz.trimf(nivel_mare_previsto.universe, [3.5, 5, 5])

    nivel_mare_previsto['baixa'] = fuzz.trimf(nivel_mare_previsto.universe, [0, 0, 1.5])
    nivel_mare_previsto['media'] = fuzz.trimf(nivel_mare_previsto.universe, [1, 2.5, 4])
    nivel_mare_previsto['alta'] = fuzz.trimf(nivel_mare_previsto.universe, [3.5, 5, 5])

    # Saída
    probabilidade_alagamento['baixo'] = fuzz.trimf(probabilidade_alagamento.universe, [0, 0, 35])
    probabilidade_alagamento['moderado'] = fuzz.trimf(probabilidade_alagamento.universe, [30, 50, 65])
    probabilidade_alagamento['alto'] = fuzz.trimf(probabilidade_alagamento.universe, [60, 80, 100])

    # Regras Fuzzy
    rule1 = ctrl.Rule(temperatura['baixa'] & umidade['baixa'], probabilidade_alagamento['baixo'])
    rule2 = ctrl.Rule(temperatura['media'] & umidade['alta'], probabilidade_alagamento['alto'])
    rule3 = ctrl.Rule(temperatura['alta'] & umidade['moderada'], probabilidade_alagamento['moderado'])
    rule4 = ctrl.Rule(umidade['alta'] | nivel_mare_previsto['alta'], probabilidade_alagamento['alto'])
    rule5 = ctrl.Rule(umidade['moderada'] | nivel_mare_previsto['baixa'], probabilidade_alagamento['baixo'])
    rule6 = ctrl.Rule(umidade['baixa'] | nivel_mare_previsto['baixa'], probabilidade_alagamento['baixo'])
    
    # Sistema de controle
    nivel_rio_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
    nivel_rio_simulador = ctrl.ControlSystemSimulation(nivel_rio_ctrl)

    # Converter o timestamp para um objeto datetime
    data = datetime.datetime.fromtimestamp(values["timestamp"])
    mes = 11 #data.month
    dia = data.day
    hora = data.hour
    minuto = data.minute
    dia_hora = str(dia) + ' ' + str(hora) +':'+ str(minuto)

    # Carregar o mapa das marés
    tide_data = pd.read_csv('./scripts/Mapa_das_Mares.csv')
    coluna_mes = tide_data.iloc[:,int(mes)-1].dropna()

    # Separar os dados em colunas individuais
    separated_data = coluna_mes.str.extract(r'(?P<Date>\d{2}), (?P<Hour>\d{4}), (?P<Tide_Level>[\d.]+)')

    # Converter a coluna 'Hour' para o formato correto
    separated_data['Hour'] = pd.to_datetime(separated_data['Hour'], format='%H%M').dt.strftime('%H:%M:%S')

    # Obter o nível da maré mais próximo do horário da última linha
    nivel_mare_previsto_proximo = get_nearest_tide_level(dia_hora, separated_data)

    # Passar os valores como input para o simulador
    nivel_rio_simulador.input['temperatura'] = values["data"]["temperature"]
    nivel_rio_simulador.input['umidade'] = values["data"]["humidity"]
    nivel_rio_simulador.input['nivel_mare_previsto'] = nivel_mare_previsto_proximo

    # Computar a saída
    nivel_rio_simulador.compute()
    print("Probabilidade de alagamento:", nivel_rio_simulador.output['probabilidade_alagamento'])
    
    # Classificação da probabilidade de alagamento
    probabilidade = float(nivel_rio_simulador.output['probabilidade_alagamento'])
    
    if probabilidade < 30:
        classificacao = 'Baixa'
    elif 30 <= probabilidade <= 60:
        classificacao = 'Média'
    else:
        classificacao = 'Alta'
    
    return  nivel_rio_simulador.output['probabilidade_alagamento'], classificacao
