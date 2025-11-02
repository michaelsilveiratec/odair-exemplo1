📊 SHEIN Sales Dashboard
<div align="center">
https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python
https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly
https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker

</div>
🎯 Visão Geral
O SHEIN Sales Dashboard é uma aplicação web interativa construída com Streamlit que fornece visualizações em tempo real dos dados de vendas e produtos.

✨ Funcionalidades do Dashboard
📈 Visualização de Dados
Métricas em tempo real: Vendas totais, produtos cadastrados, ticket médio, estoque

Gráficos interativos: Vendas por categoria e por marca

Tabela de produtos: Lista completa com todos os detalhes

Estatísticas rápidas: Produto mais vendido, categoria líder, marca líder

🔧 Gerenciamento de Produtos
Adicionar novos produtos através de formulário intuitivo

Monitorar estoque em tempo real

Acompanhar performance de vendas por produto

🎮 Interface Interativa
Atualização manual com botão de refresh

Atualização automática configurável

Design responsivo para desktop e mobile

Visualizações interativas com Plotly

🚀 Início Rápido
🐳 Via Docker (Recomendado)
bash
# Execute o dashboard
docker-compose up --build dashboard

# Ou apenas
docker-compose up dashboard
💻 Via Python Local
bash
# Navegue até a pasta do dashboard
cd dashboard

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
🌐 Acesso
text
📊 Dashboard: http://localhost:8501
🏗️ Estrutura do Projeto
text
dashboard/
├── 🐳 Dockerfile                 # Configuração do container
├── 🐍 app.py                    # Aplicação principal Streamlit
└── 📋 requirements.txt          # Dependências Python
🎮 Como Usar
📊 Visualizando Dados
Acesse http://localhost:8501

Veja as métricas principais no topo da página

Explore os gráficos interativos de vendas

Analise a tabela de produtos cadastrados

➕ Adicionando Produtos
Expanda o formulário na barra lateral

Preencha os dados do produto:

Nome e categoria

Marca e preço

Estoque e vendas iniciais

Clique em "Adicionar Produto"

🔄 Atualização de Dados
Automática: Configure para atualizar a cada 30 segundos

Manual: Clique no botão "🔄 Atualizar Dados"

Em tempo real: Novos produtos aparecem instantaneamente

📊 Componentes do Dashboard
🎯 Métricas Principais
Vendas Totais 📊 - Unidades vendidas

Total de Produtos 🏷️ - Produtos cadastrados

Ticket Médio 💰 - Preço médio dos produtos

Estoque Total 📦 - Unidades em estoque

📈 Gráficos Interativos
Vendas por Categoria - Gráfico de barras

Vendas por Marca - Gráfico de barras

🎛️ Controles
Botão de Atualização 🔄

Formulário de Produtos ✅

Atualização automática ⚙️

🔧 Configuração
⚙️ Configurações Personalizáveis
No arquivo app.py, você pode modificar:

🎨 Cores do tema

⏰ Intervalo de atualização

📐 Layout dos componentes

📊 Tipos de gráficos

🛠️ Desenvolvimento
💻 Instalação para Desenvolvimento
bash
cd dashboard
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
📦 Dependências Principais
txt
streamlit==1.28.0
pandas==2.1.0
plotly==5.15.0
requests==2.31.0
🐳 Docker
🏗️ Comandos Úteis
bash
# Build da imagem
docker build -t shein-dashboard .

# Executar container
docker run -p 8501:8501 shein-dashboard

# Ver logs
docker logs <container_id>

# Parar container
docker stop <container_id>
💡 Características Técnicas
Framework: Streamlit

Visualizações: Plotly

Processamento de dados: Pandas

Containerização: Docker

Interface: Responsiva e intuitiva

<div align="center">
Desenvolvido com 💻 e ☕

</div>