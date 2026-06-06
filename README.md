# 🎵 CCB - Sistema de Presença

Sistema de contagem e registro de presença de **músicos**, **organistas** e **irmandade** nos serviços da Congregação Cristã no Brasil.

## Stack
- **Frontend/App:** Streamlit (Python)
- **Banco de Dados:** Supabase (PostgreSQL)
- **Versionamento:** GitHub

## Estrutura
```
ccb-presenca-musicos/
├── app.py                  # App principal
├── pages/
│   ├── 1_Registrar.py      # Registro de presença
│   ├── 2_Relatorios.py     # Relatórios e gráficos
│   └── 3_Gerenciar.py      # Gerenciar registros
├── utils/
│   └── supabase_client.py  # Conexão Supabase
├── database/
│   └── schema.sql          # Script SQL para criar as tabelas
├── .streamlit/
│   └── secrets_example.toml
└── requirements.txt
```

## Como usar

### 1. Configurar o Supabase
Execute o arquivo `database/schema.sql` no SQL Editor do Supabase.

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar credenciais
Crie o arquivo `.streamlit/secrets.toml` com:
```toml
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "sua_anon_key"
```

### 4. Rodar localmente
```bash
streamlit run app.py
```

### 5. Deploy no Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte este repositório
3. Adicione as secrets nas configurações
4. Clique em Deploy

## Funcionalidades
- ✅ Registrar presença por função (Músico, Organista, Irmandade)
- ✅ Criar e selecionar serviços por data e tipo
- ✅ Contadores em tempo real na tela
- ✅ Relatórios com gráficos (Plotly)
- ✅ Exportar lista em CSV
- ✅ Gerenciar e excluir registros incorretos
