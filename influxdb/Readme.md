# Configurando o Influxdb

> Os passos a seguir foram testados no Windows 10, com o Docker Desktop instalado e o Kubernetes habilitado. 

A configuração do container do banco de dado Influxdb está no arquivo *influxdb-deployment.yaml*. Aplique o arquivo com o comando:
~~~bash
kubectl apply -f influxdb-deployment.yaml
~~~

Acessar o InfluxDB Localmente. Se você estiver em um cluster Kubernetes local (como o Minikube), faça um port-forward:
~~~bash
kubectl port-forward svc/influxdb-service 8086:8086
~~~

## Conectar e Criar Buckets

Use o script Python *starting_influxdb.py* para conectar e criar um buckets no Influxdb.

Certifique-se de instalar o cliente do InfluxDB para Python:
~~~bash
pip install influxdb-client
~~~

Verifique se o InfluxDB está acessível em http://localhost:8086.

No script altere o token de autenticação e personalize o nome do bucket (bucket_name) no script conforme necessário:

1. Verificar o pod do influxdb :
    ~~~bash
    kubectl get pods
    ~~~

2. Conecte-se ao contêiner do InfluxDB para recuperar o token:
    ~~~bash
    kubectl exec -it <nome-do-pod-influxdb> -- influx auth list
    ~~~
    Isso exibirá os tokens disponíveis, com seus respectivos valores e permissões. Copie o token que tem as permissões corretas.

3. Atualize o token no script substituindo o valor do mesmo.

Execute o script com o comando:

~~~bash
python starting_influxdb.py
~~~

## Parando o serviço

1. Liste os pods que estão rodando:
    ~~~bash
    kubectl get pods
    ~~~

2. Uma forma de parar o serviço sem removê-lo do cluster é escalá-lo para zero réplicas:
    ~~~bash
    kubectl scale deployment influxdb --replicas=0
    ~~~
Após executar este comando, o pod será encerrado.

3. Verifique se o pod foi parado com o comando do passo 1 que lista os pod ativos.

4. (OPCIONAL) Se quiser remover completamente o serviço, delete o deployment e o service:
    ~~~bash
    kubectl delete deployment influxdb
    kubectl delete service influxdb-service
    ~~~

5. Se você ainda estiver usando um port-forward, interrompa o comando que está rodando com Ctrl+C no terminal. Isso encerra o redirecionamento de porta.

## Próximos Passos
Quando quiser reiniciar o InfluxDB, basta escalá-lo novamente:
~~~bash
kubectl scale deployment influxdb --replicas=1
~~~