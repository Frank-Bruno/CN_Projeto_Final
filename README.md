# CN_Projeto_Final

A arquitetura proposta visa fornecer uma infraestrutura escalável e resiliente para aplicações IoT, com foco na coleta, processamento e armazenamento de dados de sensores. No cenário descrito, temos uma rede de sensores que publicam dados em um broker AMQP (RabbitMQ) utilizando uma exchange e duas filas (queues). Duas aplicações consomem dados de suas respectivas filas para processá-los e armazená-los em um banco de dados InfluxDB. Além disso, a arquitetura contempla a escalabilidade dinâmica das aplicações de processamento de dados por meio do Horizontal Pod Autoscaler (HPA) e o monitoramento completo da infraestrutura utilizando o Prometheus.

![Arquitetura](/imgs/arquitetura_kubernetes.png)
### Componentes da Arquitetura:
1. Simulador de Tráfego: Um serviço que simula a geração de dados de sensores, publicando periodicamente as mensagens no broker AMQP. A carga gerada pode ser ajustada para simular diferentes volumes de dados, escalando o número de nós sensores conforme necessário.
2. Broker AMQP (RabbitMQ): Responsável pela troca de mensagens entre os dispositivos IoT e as aplicações consumidoras. Ele é configurado com uma exchange e duas filas para garantir uma comunicação eficiente e escalável entre os produtores e consumidores de dados.
3. Banco de Dados InfluxDB: Utilizado para armazenar os dados de sensores, com alta capacidade de leitura e escrita para grandes volumes de dados temporais.
4. Aplicação 1 (Processamento de Dados): Responsável por processar os dados recebidos da fila 1 e armazená-los no InfluxDB.
5. Aplicação 2 (Algoritmo de Previsão): Consome os dados da fila 2, realiza cálculos ou algoritmos de previsão e retorna os resultados para a aplicação ou sistemas subsequentes.

### Escalabilidade e Monitoramento:
- As aplicações 1 e 2 são configuradas para escalar automaticamente com base na carga de trabalho, utilizando o Horizontal Pod Autoscaler (HPA). O HPA ajusta dinamicamente o número de réplicas de pods com base em métricas como uso de CPU ou memória.
- O Prometheus é utilizado para monitorar a saúde e o desempenho dos pods, incluindo as métricas de escalabilidade, tempo de resposta e disponibilidade dos serviços.

## Construindo a Arquitetura

### Pré-requisitos
-  [Docker Desktop](https://www.docker.com/products/docker-desktop/) (com Kubernetes habilitado, caso esteja no Windows/macOS)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) (Kubernetes in Docker)
- [Kubectl](https://kubernetes.io/pt-br/docs/tasks/tools/install-kubectl-linux/) (CLI para gerenciar o cluster Kubernetes)
- [Helm](https://helm.sh/pt/docs/intro/install/) (gerenciador de pacotes do Kubernetes)

Acesse os liks para obter as instruções detalhadas para instalação. Para verificar, use os seguintes comandos:
~~~bash
kind version
kubectl version --client
helm version
~~~

### Criando o Cluster Kubernetes com Kind

Use o arquivo de configuração *cluster-config.yaml* para configurar um cluster com 1 control plane e 5 nós workers. Execute o comando:

~~~bash
kind create cluster --name iot-cluster --config cluster-config.yaml
~~~

Verifique se o cluster foi criado corretamente:
~~~bash
kind get clusters
~~~
Após a criação do cluster, verifique os nós:
~~~bash
kubectl get nodes
~~~
![Saida esperada](/imgs/verificando_criacao_clusteres.png)

Para garantir que os pods (simulador, aplicação 1, aplicação 2, RabbitMQ e InfluxDB) sejam distribuídos em nós distintos, você pode usar Pod Anti-Affinity no arquivo YAML de cada deployment/statefulset.

### Configuração do RabbitMQ com Helm
Adicione o repositório do RabbitMQ ao Helm:
~~~bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
~~~ 
Use o Helm para instalar o RabbitMQ no cluster:
~~~bash
helm install rabbitmq bitnami/rabbitmq -f rabbitmq-values.yaml
~~~
Entre as informações de saida será indicado como expor o serviço:
![Saida esperada](/imgs/acesso_rabbitmq_1.png)
Caso precise recuperar a senha use:
~~~bash
echo "Password      : $(kubectl get secret --namespace default rabbitmq -o jsonpath="{.data.rabbitmq-password}" | base64 -d)"
~~~
Verifique o serviço:
~~~bash
kubectl get all | grep rabbitmq
~~~
![Saida esperada](/imgs/verificando_servico_rabbitmq.png)
O RabbitMQ será exposto internamente via ClusterIP.

### Configurando o InfluxDB com Helm
Adicione o repositório do Influxdb ao Helm:
~~~bash
helm repo add influxdata https://helm.influxdata.com/
helm repo update
~~~ 
Use o Helm para instalar o Influxdb no cluster:
~~~bash
helm install influxdb influxdata/influxdb2 -f influxdb-values.yaml
~~~
Entre as informações de saida será indicado como expor o serviço:
![Saida esperada](/imgs/acesso_influxdb_1.png)

Verifique o serviço:
~~~bash
kubectl get all | grep influxdb
~~~
![Saida esperada](/imgs/verificando_servico_influxdb.png)

Caso precise recuperar o toke, conecte-se ao contêiner do InfluxDB assim:
~~~bash
kubectl exec -it <nome-do-pod-influxdb> -- influx auth list
~~~

### Configurar o Simulador de Tráfego
Use o arquivo *simulator-deployment.yaml* para configurar o pod para simular o trafego gerado por uma rede de sensores. Execute o comando:
~~~bash
kubectl apply -f simulator-deployment.yaml
~~~

Caso precise fazer alguma alteração na simulação, acessar o scripts *sensor_simulator.py* e edite. Depois execute os seguintes comandos para construir uma nova imagem:
~~~bash
docker build -t mercydiniz/node-sensor:latest .
docker login
docker push mercydiniz/node-sensor:latest
~~~

### Configurar as Aplicações
Pendente ...

### Verfique a Arquitetura
Distribuição dos pods:
~~~bash
kubectl get pods -o wide
~~~
![Saida esperada](/imgs/verificando_distribuicao_pods_p1.png)

Os StatefulSet que gerenciam os pod:
~~~bash
kubectl get statefulsets
~~~

Serviços e as portas configuradas
~~~bash
kubectl get services
~~~
![Saida esperada](/imgs/verificando_servicos_p1.png)



### Configurar o Horizontal Pod Autoscaler (HPA)

### Configurar o Prometheus e Grafana com Helm


## Referências
- [Minicurso Kubernetes - LASSE](https://www.youtube.com/playlist?list=PL6t5HAc1KOf6TS4y0AgEsMriVlcX7QMzO)

- [Conhecendo os recursos e conceitos do Kubernetes](https://aurimrv.gitbook.io/pratica-devops-com-docker/7-deploy-na-nuvem/7.3-conhecendo-os-recursos-e-conceitos-do-kubernetes)

- [Documentação do Kubernetes - Instale as ferramentas](https://kubernetes.io/pt-br/docs/tasks/tools/)
