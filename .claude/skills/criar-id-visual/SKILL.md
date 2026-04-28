---
name: criar-id-visual
description: >
  Cria a identidade visual de um negócio ou projeto do zero.
  Faz um briefing estruturado, gera paleta de cores, tipografia e personalidade visual,
  e salva tudo em um design-guide.md pronto pra usar em qualquer outra skill.
  Use quando o usuário pedir "cria uma identidade visual", "quero uma ID visual", "define as cores do projeto",
  "cria um design guide", "quero uma paleta pra marca", ou chamar /criar-id-visual.
---

# /criar-id-visual — Criação de Identidade Visual

Cria a identidade visual completa de um negócio ou projeto.
O output é um `design-guide.md` com paleta, tipografia e personalidade visual documentados,
pronto pra alimentar outras skills (slide, copy, landing page, etc).

---

## Fluxo

### Passo 1 — Coletar contexto existente

Antes de perguntar qualquer coisa, verificar se já existe:
- `marca/design-guide.md` → se existir e estiver preenchido, perguntar: "Já existe um design guide aqui. Quer atualizar o que existe ou criar um novo projeto?"
- `_contexto/empresa.md` → ler se existir pra aproveitar o que já sabe sobre o negócio

Se o usuário não tiver especificado o projeto, perguntar: "Isso é pra qual projeto ou cliente?" antes de continuar.

---

### Passo 2 — Briefing em blocos

Fazer as perguntas em **3 blocos**, um bloco por vez. Aguardar resposta antes de avançar.
Não fazer todas as perguntas de uma vez. Não pular blocos.
Pular perguntas cujas respostas já foram dadas ou estão no contexto.

---

**Bloco 1 — O negócio**

> "Vou fazer algumas perguntas pra entender o projeto antes de criar qualquer coisa. Pode responder como quiser, sem formato específico."

Perguntar:
1. Qual é o nome do negócio ou projeto?
2. O que ele vende ou entrega? (produto, serviço, infoproduto, marca pessoal...)
3. Pra quem? Descreva o público em uma frase.
4. Qual é o grande diferencial ou posicionamento? O que torna esse negócio único?

---

**Bloco 2 — Personalidade e referências**

> "Agora sobre a personalidade da marca:"

Perguntar:
1. Se essa marca fosse uma pessoa, como ela seria? Escolha 3 a 5 adjetivos.
2. Quais marcas ou negócios ela admira visualmente — e por quê? (podem ser de qualquer setor)
3. Quais marcas ou estilos ela definitivamente NÃO quer parecer? O que quer evitar?
4. Tem alguma cor, fonte ou elemento visual que já está definido ou que você gosta muito?

---

**Bloco 3 — Uso e contexto**

> "Última parte: onde essa identidade vai aparecer?"

Perguntar:
1. Quais são os principais canais? (Instagram, YouTube, site, apresentações, WhatsApp, impresso...)
2. Tem logo? Se sim, como ele é — e tem versão clara e escura?
3. Tem algum prazo ou urgência pra ter isso pronto?

---

### Passo 3 — Proposta visual

Com o briefing completo, gerar a proposta visual em texto.
**Não salvar ainda.** Apresentar pra validação antes.

Estrutura da proposta:

---

**Essência da marca**
Uma frase que resume a identidade: personalidade + posicionamento visual.
Exemplo: "Autoridade acessível — séria sem ser fria, próxima sem ser genérica."

**Paleta de cores**
- Cor primária: `#HEX` — Nome e racional (o que ela transmite, quando usar)
- Cor secundária: `#HEX` — Nome e racional
- Cor de destaque/acento: `#HEX` — Nome e racional
- Neutro claro: `#HEX` — para fundos e espaço
- Neutro escuro: `#HEX` — para texto e contraste

Incluir: modo claro e modo escuro se relevante. Indicar qual cor domina em qual contexto.

**Tipografia**
- Display (títulos, destaques): [Nome da fonte] — racional em uma frase. Fonte do Google Fonts.
- Corpo (texto corrido, legendas): [Nome da fonte] — racional em uma frase. Fonte do Google Fonts.
- Hierarquia de uso: quando usar cada uma e em que tamanhos relativos.

**Personalidade visual**
- 3 atributos visuais principais (ex: "limpa", "contrastante", "geométrica")
- O que a marca usa: formas, espaçamento, elementos gráficos
- O que a marca evita: estilos, cores, recursos proibidos

**Regras rápidas**
Uma lista curta de do's and don'ts práticos pra quem for aplicar a identidade.

---

Ao apresentar, perguntar:
> "O que você quer ajustar antes de eu salvar?"

Só avançar pro Passo 4 após confirmação explícita ("pode salvar", "aprovado", "tá bom").

---

### Passo 4 — Salvar o design guide

Salvar em `marca/[nome-do-projeto]/design-guide.md`.
Se a pasta não existir, criar.

Formato do arquivo:

```markdown
# Design Guide — [Nome do Projeto]

*Criado em: [data]*

---

## Essência
[frase de essência]

---

## Paleta de Cores

| Papel | Hex | Nome | Uso |
|---|---|---|---|
| Primária | #HEX | Nome | quando usar |
| Secundária | #HEX | Nome | quando usar |
| Acento | #HEX | Nome | quando usar |
| Neutro claro | #HEX | Nome | quando usar |
| Neutro escuro | #HEX | Nome | quando usar |

---

## Tipografia

**Display:** [Fonte] — [racional]
**Corpo:** [Fonte] — [racional]

Hierarquia:
- Título principal: Display, grande
- Subtítulo: Display ou Corpo, médio
- Texto corrido: Corpo, regular
- Legenda/label: Corpo, pequeno

---

## Personalidade Visual

**Atributos:** [atributo 1], [atributo 2], [atributo 3]

**Usa:** [elementos, formas, espaçamentos, recursos]
**Evita:** [estilos, cores, recursos proibidos]

---

## Regras Rápidas

✓ [do 1]
✓ [do 2]
✓ [do 3]
✗ [don't 1]
✗ [don't 2]
✗ [don't 3]

---

## Logo

[Preencher quando disponível]
- Versão clara: `marca/[projeto]/logo-claro.png`
- Versão escura: `marca/[projeto]/logo-escuro.png`
- Área de proteção: [instrução]
- Uso incorreto: [o que evitar]
```

Confirmar ao final:
> "Design guide salvo em `marca/[projeto]/design-guide.md`. Quer já criar alguma coisa com essa identidade?"

---

## Regras

- Nunca gerar a proposta sem ter passado pelos 3 blocos de briefing
- Nunca salvar sem confirmação explícita do usuário
- Sempre usar Google Fonts — sem fontes pagas ou que precisem de instalação
- Paleta com no mínimo 5 cores: primária, secundária, acento, neutro claro, neutro escuro
- Fontes do Google Fonts que funcionam bem por personalidade:
  - Autoridade/premium: Playfair Display, Cormorant Garamond, DM Serif Display
  - Moderno/tech: Inter, Geist, Space Grotesk, Plus Jakarta Sans
  - Humano/próximo: Nunito, Lato, Poppins, Outfit
  - Criativo/diferente: Bricolage Grotesque, Cabinet Grotesk, Syne
  - Serif clássico: Lora, Merriweather, EB Garamond
- Se o usuário não tiver logo, registrar no design guide que ainda está pendente
- Se o projeto for do próprio negócio do usuário, ler `_contexto/empresa.md` e `_contexto/preferencias.md` pra calibrar o tom
