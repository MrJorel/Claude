# Matozo — Claude Code OS

## O que é esse workspace
Workspace principal do Matheus Jorel — CMO as a Service, especialista em webinars e infoprodutos. Centraliza os projetos ativos (LBR, Wizoom Play, marca pessoal) e serve como base de operação da Matozo.

**Estrutura de pastas:**
- `clientes/` — um diretório por cliente com briefing, estratégia e entregas
- `projetos-proprios/` — produtos digitais, canal YouTube, marca pessoal
- `_contexto/` — negócio, preferências e foco atual (lidos no início de cada conversa)
- `marca/` — guias de design por projeto
- `dados/` — arquivos brutos, exports, referências
- `templates/skills/` — templates de skills prontos pra personalizar com /mapear
- `templates/ferramentas/catalogo.md` — APIs e ferramentas disponíveis pra usar em skills

## Sobre o negócio
Matozo é uma operação de CMO as a Service focada em infoprodutos — cursos e mentorias vendidos via webinar e lançamento pago. Matheus atua como cérebro estratégico dos projetos: cuida de funil, tráfego, copy e métricas. Ao mesmo tempo, é creator e tem produtos próprios.

## O que mais fazemos aqui
- Planejamento e execução de lançamentos pagos
- Estruturação de funis (low ticket → webinar → high ticket)
- Copy: páginas, anúncios, VSLs, roteiros de webinar
- Gestão de tráfego (Meta Ads + Google Ads)
- Análise de métricas (ROAS, CPA, CAC, LTV)
- Criação de conteúdo (YouTube e Instagram)
- Estratégia e liderança de projetos como CMO

## Clientes e contexto
Atende clientes externos (advogados, médicos, experts, infoprodutores com 1M+/ano) e desenvolve projetos próprios. Modelo de entrega: CMO as a Service — Matheus assume a cadeira estratégica de marketing nos projetos.

## Tom de voz
Casual, direto e estratégico. Sem enrolação. Vai direto ao ponto, usa analogias pra explicar, não agrada sem critério. Respostas curtas quando possível, longas só quando necessário.

## Ferramentas conectadas
Meta Ads, Google Ads, WordPress + Elementor, HubSpot, ActiveCampaign, ManyChat, Sellflux, Zouti, Memberkit, Devzapp, Google Sheets, WhatsApp, YouTube, Instagram

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (se existirem e estiverem configurados):

1. `_contexto/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_contexto/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_contexto/estrategia.md` — foco atual, prioridades, o que pode esperar

Usar essas informações como base pra qualquer resposta ou decisão. Ao sugerir prioridades, formatos ou abordagens, considerar o foco atual descrito em `estrategia.md`.

Para qualquer tarefa visual (carrossel, proposta, slide, landing page), consultar `marca/design-guide.md` como referência de estilo — e perguntar de qual projeto/cliente é o contexto antes de criar.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe uma skill relevante em `.claude/skills/` ou `.claude/commands/`.
Se encontrar, seguir as instruções da skill.
Se não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma instrução que parece permanente (frases como "na verdade é assim", "não faça mais isso", "prefiro assim", "sempre que...", "evita...", "da próxima vez..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** (quem são os clientes, como funciona a empresa, serviços, mercado) → adicionar em `_contexto/empresa.md`
- **Sobre preferências e estilo** (tom de voz, formato de resposta, o que evitar, como estruturar textos) → adicionar em `_contexto/preferencias.md`
- **Sobre prioridades e foco atual** (projetos em andamento, metas do momento, prazos importantes, o que é prioridade agora) → adicionar em `_contexto/estrategia.md`
- **Regra de comportamento nessa pasta** (onde salvar arquivos, como nomear, fluxos específicos) → adicionar no próprio `CLAUDE.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro. Confirmar o que foi salvo mostrando a linha adicionada.

Não perguntar se a correção for óbvia de contexto imediato (ex: "na verdade o arquivo se chama X"). Só perguntar quando a informação tiver valor duradouro.

---

## Criação de skills

Quando o usuário pedir pra criar uma nova skill:

1. Verificar se existe um template relevante em `templates/skills/`. Se existir, usar como base e adaptar pro contexto do usuário
2. Perguntar: "Essa skill é específica pra esse projeto ou vai ser útil em qualquer projeto?"
   - Específica desse negócio → salvar em `.claude/skills/nome-da-skill/SKILL.md` (local)
   - Útil em qualquer projeto → salvar em `~/.claude/skills/nome-da-skill/SKILL.md` (global)
3. Ler `_contexto/empresa.md` e `_contexto/preferencias.md` pra calibrar o conteúdo da skill ao contexto do negócio
4. Se a skill precisar de arquivos de apoio (templates, referências, exemplos), criar dentro da pasta da skill
5. Seguir o fluxo da skill-creator nativa do Claude Code
