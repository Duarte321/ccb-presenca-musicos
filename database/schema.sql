-- ============================================
-- CCB - Sistema de Presença
-- Script de criação do banco de dados
-- Execute no SQL Editor do Supabase
-- ============================================

-- Tabela de serviços (cultos)
CREATE TABLE IF NOT EXISTS servicos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  data DATE NOT NULL,
  tipo TEXT NOT NULL,  -- 'Culto de Semana', 'Culto de Sábado', 'Reunião de Oração', etc.
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

-- Índices para melhorar a performance das consultas
CREATE INDEX IF NOT EXISTS idx_presenca_servico_id ON presenca(servico_id);
CREATE INDEX IF NOT EXISTS idx_presenca_funcao ON presenca(funcao);
CREATE INDEX IF NOT EXISTS idx_servicos_data ON servicos(data);

-- Habilitar Row Level Security (RLS)
ALTER TABLE servicos ENABLE ROW LEVEL SECURITY;
ALTER TABLE presenca ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso público (ajuste conforme necessidade)
CREATE POLICY "Leitura pública de serviços"
  ON servicos FOR SELECT USING (true);

CREATE POLICY "Inserção pública de serviços"
  ON servicos FOR INSERT WITH CHECK (true);

CREATE POLICY "Deleção pública de serviços"
  ON servicos FOR DELETE USING (true);

CREATE POLICY "Leitura pública de presença"
  ON presenca FOR SELECT USING (true);

CREATE POLICY "Inserção pública de presença"
  ON presenca FOR INSERT WITH CHECK (true);

CREATE POLICY "Deleção pública de presença"
  ON presenca FOR DELETE USING (true);
