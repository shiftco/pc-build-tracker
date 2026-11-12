# 🚀 PC Gamer Tracker & Monitor de Ofertas

Plataforma completa e minimalista (estilo Vercel) desenvolvida para rastrear o preço de todas as peças do PC Gamer do primo do Felipe Oliveira em tempo real nas principais lojas do Brasil:
- **KaBuM!**
- **TerabyteShop**
- **Pichau**
- **Mercado Livre**
- **Shopee**

---

## 🏗️ Arquitetura do Projeto

```
pc-tracker/
├── database/                 # Banco de Dados Supabase (PostgreSQL)
│   ├── schema.sql            # Definição das tabelas relacionais com RLS
│   ├── seed.py               # Cadastro inicial das 8 peças e ofertas reais
│   └── check.py              # Script de verificação e checagem de dados
├── scraper/                  # Motores de coleta e rastreio de preços
│   ├── test_stores.py        # Testes de conexão com e-commerces
│   └── mercadolivre.py       # Coletor de dados
├── bot/                      # Módulo de Notificação Push
│   └── telegram_bot.py       # Disparador de alertas ricos com foto e botão de compra
├── web/                      # Dashboard Web Minimalista (Estilo Vercel)
│   ├── src/
│   │   ├── components/       # Header, HeroStats, CategoryFilter, PecaCard, Sparkline
│   │   ├── lib/supabase.ts   # Conexão Supabase + fallback ultra-rápido
│   │   └── App.tsx           # Tela principal do Dashboard
│   └── package.json          # Vite + React 19 + Tailwind CSS + Lucide
└── tracker.py                # Orquestrador agendado de monitoramento
```

---

## ⚡ Como Rodar o Dashboard Web Localmente

1. Abra o terminal na pasta `pc-tracker/web`:
```bash
cd web
npm run dev
```
2. Acesse no navegador: `http://localhost:5173`

---

## 📱 Como Ativar as Mensagens no Telegram do Primo

1. Crie um bot no Telegram com o [@BotFather](https://t.me/BotFather) e pegue o `BOT_TOKEN`.
2. Pegue o `CHAT_ID` do seu primo (usando bots como `@userinfobot`).
3. Adicione no arquivo `.env` ou execute o script passando as credenciais:
```bash
python tracker.py
```
Quando o preço de qualquer peça cair ou bater a meta de compra, o bot envia uma notificação push com o link direto da loja.
