## Configurando o pod dos nós sensores

Com o Dockerfile pronto, você pode construir a imagem Docker localmente. No diretório onde o seu Dockerfile está localizado, execute:
~~~bash
docker build -t seu-usuario/no-sensor:latest .
~~~
Antes de enviar a imagem para o Docker Hub, você precisa fazer login na sua conta Docker:
~~~bash
docker login
~~~
Após construir a imagem, você pode enviá-la para o Docker Hub com o comando:
~~~bash
docker push seu-usuario/no-sensor:latest
~~~

> Os passos a seguir foram testados no Windows 10, com o Docker Desktop instalado e o Kubernetes habilitado. 

Com o arquivo YAML configurado para usar a imagem do Docker Hub, você pode aplicar a configuração para criar o Pod no Kubernetes:
~~~bash
kubectl apply -f starting_node_sensor.yaml
~~~
Confirme que o Pod foi criado e está rodando:
~~~bash
kubectl get pods
~~~
Visualize os logs do Pod para garantir que o script está executando corretamente:
~~~bash
kubectl logs node-sensor-pod
~~~
Caso o pod ainda esteja em criação ou com problemas, você também pode executar o comando describe para ver eventos mais detalhados que podem indicar o que está acontecendo:
~~~bash
kubectl describe pod node-sensor-pod
~~~
Para excluir o pod e parar o processo de criação, execute o seguinte comando:
~~~bash
kubectl delete pod node-sensor-pod
~~~
Para excluir um Deployment:
~~~bash
kubectl delete deployment <nome-do-deployment>
~~~