# 🎵 CCB - Sistema de Presença de Músicos

Sistema para registrar e contabilizar a presença de **Músicos**, **Organistas** e **Irmandade** nos serviços da Congregação Cristã no Brasil.

## 🛠️ Stack

- **Frontend:** Streamlit (Python)
- **Banco de dados:** Supabase (PostgreSQL)
- **Hospedagem do código:** GitHub
- **Deploy:** Streamlit Cloud

## 🗄️ Projeto Supabase

- **Nome:** `ccb-presenca-musicos`
- **URL:** `https://ovnwnzqjjjtfqjodvusi.supabase.co`
- **Região:** São Paulo, Brasil (`sa-east-1`)
- **Painel:** https://supabase.com/dashboard/project/ovnwnzqjjjtfqjodvusi

## 📁 Estrutura do Projeto

```
ccb-presenca-musicos/
├── app.py                   # Tela inicial com navegação
├── pages/
│   ├── 1_Registrar.py       # Registro de presença + contadores
│   ├── 2_Relatorios.py      # Gráficos e exportação CSV
│   └── 3_Gerenciar.py       # Exclusão de registros
├── utils/
│   └── supabase_client.py   # Funções de banco de dados
├── database/
│   └── schema.sql           # SQL para criar as tabelas
├── .streamlit/
│   └── secrets.example.toml # Modelo de configuração
├── requirements.txt
└── README.md
```

## 🚀 Como Rodar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/Duarte321/ccb-presenca-musicos
cd ccb-presenca-musicos
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais
Copie o arquivo de exemplo e preencha com sua Anon Key do Supabase:
```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

Edite `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://ovnwnzqjjjtfqjodvusi.supabase.co"
SUPABASE_KEY = "sua_anon_key_aqui"
```

> 🔑 Pegue sua Anon Key em:
> https://supabase.com/dashboard/project/ovnwnzqjjjtfqjodvusi/settings/api

### 4. Rode o app
```bash
streamlit run app.py
```

## ☁️ Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte ao repositório `Duarte321/ccb-presenca-musicos`
3. Arquivo principal: `app.py`
4. Em **Advanced settings → Secrets**, adicione:
```toml
SUPABASE_URL = "https://ovnwnzqjjjtfqjodvusi.supabase.co"
SUPABASE_KEY = "sua_anon_key_aqui"
```
5. Clique em **Deploy!**

## 🗃️ Tabelas no Banco

### `servicos`
| Coluna | Tipo | Descrição |
|--------|------|----------|
| `id` | UUID | Chave primária |
| `data` | DATE | Data do serviço |
| `tipo` | TEXT | Ex: Culto de Semana, Reunião de Oração |
| `local` | TEXT | Local do serviço |
| `observacao` | TEXT | Observações extras |
| `criado_em` | TIMESTAMPTZ | Data de criação |

### `presenca`
| Coluna | Tipo | Descrição |
|--------|------|----------|
| `id` | UUID | Chave primária |
| `servico_id` | UUID | FK para `servicos` |
| `nome` | TEXT | Nome do participante |
| `funcao` | TEXT | Músico / Organista / Irmandade |
| `genero` | TEXT | Irmão / Irmã |
| `observacao` | TEXT | Observações |
| `registrado_em` | TIMESTAMPTZ | Data do registro |
