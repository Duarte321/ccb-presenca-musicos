-- ============================================
-- CCB - Sistema de Presença de Músicos
-- Projeto: ccb-presenca-musicos
-- Supabase URL: https://ovnwnzqjjjtfqjodvusi.supabase.co
-- ============================================

-- Tabela de serviços (cultos)
CREATE TABLE IF NOT EXISTS servicos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  data DATE NOT NULL,
  tipo TEXT NOT NULL,
  local TEXT,
  observacao TEXT,
  criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de presença
CREATE TABLE IF NOT EXISTS presenca (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  servico_id UUID REFERENCES servicos(id) ON DELETE CASCADE,
  nome TEXT NOT NULL,
  funcao TEXT NOT NULL CHECK (funcao IN ('Músico', 'Organista', 'Irmandade')),
  genero TEXT CHECK (genero IN ('Irmão', 'Irmã', NULL)),
  observacao TEXT,
  registrado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_presenca_servico_id ON presenca(servico_id);
CREATE INDEX IF NOT EXISTS idx_presenca_funcao ON presenca(funcao);
CREATE INDEX IF NOT EXISTS idx_servicos_data ON servicos(data);

-- Habilitar RLS
ALTER TABLE servicos ENABLE ROW LEVEL SECURITY;
ALTER TABLE presenca ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso
CREATE POLICY "Leitura publica de servicos" ON servicos FOR SELECT USING (true);
CREATE POLICY "Insercao publica de servicos" ON servicos FOR INSERT WITH CHECK (true);
CREATE POLICY "Delecao publica de servicos" ON servicos FOR DELETE USING (true);
CREATE POLICY "Atualizacao publica de servicos" ON servicos FOR UPDATE USING (true);

CREATE POLICY "Leitura publica de presenca" ON presenca FOR SELECT USING (true);
CREATE POLICY "Insercao publica de presenca" ON presenca FOR INSERT WITH CHECK (true);
CREATE POLICY "Delecao publica de presenca" ON presenca FOR DELETE USING (true);
CREATE POLICY "Atualizacao publica de presenca" ON presenca FOR UPDATE USING (true);
