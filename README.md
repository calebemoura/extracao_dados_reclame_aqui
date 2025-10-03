# Extracao de dados site do Reclame Aqui

Para título de estudo a aprimoramento de técnica de web scraping, relalização upload e arquivo para um volume do databricks por meio de API, porque hoje quando se fala de enriquecimento de bases de dados, umas das formas é por meio de web scraping, que nada mais é uma raspagem de dados que estão púplicos na web. Pontos importantes quando se fala de web scraping:
- A forma mais correta de fazer essa busca de dados é por meio de API, porque é forma de comunicação e integração dos sistema. Porque é de uma forma semi-estruturada e sugura e realizar esse tráfego de dados.
- O web scraping é uma forma alternativa, mas pode gerar muita manutenção, porque se mudar alguma coisa no site o processo não é concluído corretamente, e dependendo de algums site é muito inviável realizar um raspagem.
- Um ponto muito importante é estar atento ao [robots.txt](https://www.reclameaqui.com.br/robots.txt), ele é um orientação para os que desenvolvem robôs para raspagem de dados, orientando o que é permitido e o que não é permitido acessar dentro do site

#### Objetivo
Esse projeto é somente para título de estudo e aprimoramento de técnicas, e buscar navegar por situação de mundo real. O reclame aqui tem uma para a busca das informações, mas essa API é restrita para empresas. Então essa forma que desenvolvi é um paliativo ou MVP para mostrar o grande valor de ouvir os cliente e resolver a dor, e assim justifica o investimento para aderir a API.

#### O projeto
O projeto consiste em extrair as reclamações dos cliente de uma determinada empresa, verificar o status da reclamação. E assim que extrair armazenar um um local apropriado, aqui neste projeto estou armazenando na databricks, criei um volume, onde desegnei como `landing` onde armazeno os dados brutos e depois evoluir em camadas tranformando e deixando de um modo apropriado para relizar análises ou até mesmo treinar modelos.