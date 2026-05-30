---
name: copy-pagina-vendas
description: >
  Gera a copy completa de uma página de vendas no padrão Light Copy,
  estruturada em 15 blocos atômicos (Hero, Dor, Prova Social, CTA
  intermediário, Método, Para Quem É, Entregáveis, Bônus, Stack de Valor,
  Depoimentos, Suporte, Garantia, Autoridade, FAQ, Oferta Final). Foco apenas
  em texto. Não gera HTML, não gera design, não usa templates visuais.
  Entrega final em um documento Markdown único e completo apresentado no
  chat, pronto para o usuário copiar ou baixar. Não salva em pasta de projeto.
---

# Copy de Página de Vendas. Só Texto. Padrão Light Copy

Skill autocontida para gerar a copy completa de uma página de vendas no estilo Light Copy, estruturada em 15 blocos. **Não produz HTML, não produz design, não usa templates visuais. Não salva em pasta de projeto nenhuma.** Ao final, entrega um documento Markdown único, completo e formatado, com os 15 títulos `## Bloco NN — Nome`, pronto para o usuário copiar, baixar ou colar em qualquer template HTML, ferramenta de página, email ou exportador de PDF.

---

## O Que Esta Skill Faz

1. Coleta os dados mínimos sobre o produto, o público, o preço, o ângulo e os bônus via entrevista de 10 perguntas.
2. Gera a copy completa nos 15 blocos atômicos da estrutura de página de vendas.
3. Aplica o Manual da Copy (15 princípios + 20 vícios proibidos) antes de entregar cada bloco.
4. Apresenta no chat, ao final, o documento Markdown consolidado com toda a copy, em formato pronto pra ser copiado ou baixado pelo usuário.

## O Que Esta Skill NÃO Faz

- Não gera HTML, CSS ou JavaScript.
- Não escolhe paleta de cores, fontes, layout ou componentes visuais.
- Não monta página em ferramenta nenhuma.
- Não salva arquivos em estrutura de projeto, não cria pastas, não toca em manifest ou painel de entregas.
- Não cria depoimentos de pessoas reais (cria modelos sinalizados para substituição).
- Não encaminha pra outras skills externas. O fluxo termina dentro desta skill, com o documento entregue no chat.

---

## Fluxo (7 Passos)

### Passo 1. Coleta de Contexto

Antes de gerar, pergunte uma de cada vez:

1. **Nome do produto.** Como ele se chama no mercado?
2. **Em uma frase, qual transformação o produto entrega?** (o resultado final, não o processo)
3. **Quem é o cliente ideal?** (perfil demográfico, profissão, faixa, momento da vida)
4. **Qual a dor real desse cliente?** (o que ele sente, fala, evita falar)
5. **Qual o método ou estrutura do produto?** (etapas, módulos, fases, formato de entrega)
6. **Preço cheio e parcelamento.**
7. **Tem garantia?** Se sim, prazo e tipo.
8. **Tem bônus já definidos?** Se sim, nome e valor de cada um. Se não, posso criar 3 coerentes.
9. **Tem depoimentos reais com resultado concreto?** Se sim, nome e resultado. Se não, vou criar modelos marcados para substituição.
10. **Ângulo de entrada da copy.** Escolha um:
    - Inadequação. A pessoa está desatualizada ou fazendo do jeito errado.
    - Identificação. A pessoa se reconhece na dor descrita.
    - Plug & Play. A pessoa quer algo pronto pra usar agora.
    - Promessa Boa Demais. Existe história real com números verificáveis.

Faça **uma pergunta por vez**, não despeje todas juntas. Se o usuário já passou parte das informações no contexto, pule essas perguntas.

### Passo 2. Confirmação Antes de Gerar

Mostre um resumo:

```
Resumo do que vou gerar:
- Produto: [nome]
- Transformação principal: [frase]
- Cliente ideal: [perfil]
- Dor real: [descrição]
- Método: [resumo]
- Preço: [valor + parcelamento]
- Garantia: [prazo ou "sem garantia"]
- Bônus: [lista ou "vou criar 3"]
- Depoimentos: [reais ou "vou criar modelos para substituir"]
- Ângulo: [inadequação / identificação / plug & play / promessa boa demais]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### Passo 3. Princípios de Copy. Light Copy

**Carregar antes de gerar uma linha:** `references/manual-copy.md`. É a fonte única.

Resumo operacional:

- **A melhor copy não parece copy.** Parece alguém inteligente explicando algo que o leitor nunca tinha entendido direito.
- **Você não vende no início.** Você informa, avisa ou ensina. O produto não existe nos primeiros parágrafos.
- **Argumente sempre.** Toda promessa tem mecanismo, comparação antes/depois, especificação e prova curta.
- **Nomear cria realidade.** Crie nomes próprios para o problema, a causa ou o método. "Método Exclusivo" não vale.
- **Razão E emoção em toda copy.** Engenheiro também tem coração.
- **Promessa E benefício.** Vender a transformação técnica E a consequência tangível (dinheiro, tempo, reconhecimento).
- **Dor real, não superficial.** A dor que o cliente diz primeiro quase nunca é a dor verdadeira.
- **Headline em toda seção.** Sem headline, ninguém lê o conteúdo.
- **Depoimento exige resultado.** Antes + resultado específico + prazo. Elogio sem número é descarte.
- **Autoridade com conquista concreta.** Números, clientes, prêmios, resultado de alunos.

### Passo 4. Estrutura Obrigatória. 15 Blocos

Use **exatamente** estes títulos `##` na ordem abaixo. Numeração com dois dígitos (01, 02, …, 15). Não una blocos, não pule número, não renomeie. Detalhe completo em `references/template-copy-pagina-vendas.md`.

- **Bloco 01 — Hero.** Headline (promessa, até 10 palavras, afirmação direta, sem pergunta, sem produto, sem método, sem sigla), subheadline, 3 bullets no padrão **urgência oculta + benefício**, indicação de vídeo placeholder, texto do botão. **Proibido** mencionar nome do produto, método, curso ou sigla aqui.
- **Bloco 02 — Dor.** Dor amplificada com cenas do cotidiano. Não descreva o sintoma, descreva a **causa** ("Você procrastina porque seu cérebro foi programado para ação imediata", não só "você procrastina").
- **Bloco 03 — Prova social (primeiro bloco).** 2 a 3 depoimentos curtos com nome + resultado específico. Se não houver reais, marque com `[DEPOIMENTO MODELO. SUBSTITUIR]`.
- **Bloco 04 — CTA intermediário.** Frase curta de virada + texto do botão (ancorar pra oferta final).
- **Bloco 05 — Método.** Primeira vez que o nome do método ou do produto aparece com destaque. Apresentação das macroetapas. Mínimo 3 parágrafos de argumentação explicando por que esse método funciona, como era antes e como é agora.
- **Bloco 06 — Para quem é / Para quem não é.** Listas claras para os dois lados. "Não é para" filtra leitor errado.
- **Bloco 07 — Entregáveis.** Lista completa com nome + valor de mercado individual de cada item.
- **Bloco 08 — Bônus.** 3 bônus com nome, descrição e R$ individual. Cada bônus ancorado em preço de mercado.
- **Bloco 09 — Stack de valor.** Itens com valor, total ancorado, preço real, parcelamento. Total maior que o preço.
- **Bloco 10 — Prova social (segundo bloco) ou Depoimentos.** 3 a 5 depoimentos completos com situação antes + resultado depois + prazo. Palavras-chave em **negrito**. Modelos sinalizados se necessário.
- **Bloco 11 — Suporte.** Como o aluno é acompanhado (canais, frequência, prazo de resposta).
- **Bloco 12 — Garantia.** Tipo (incondicional, satisfação), prazo (7, 15 ou 30 dias), texto de risco zero.
- **Bloco 13 — Autoridade do criador.** Quem é, credenciais, prova de resultado concreta (faturamento, maior cliente, prêmios, alunos formados). Sem "sou apaixonada pelo que faço".
- **Bloco 14 — FAQ.** 5 a 8 perguntas e respostas das objeções reais do público.
- **Bloco 15 — Oferta final.** Reprise de valor, preço, último CTA, urgência se houver, menção a termos/privacidade em uma linha se quiser rodapé.

### Passo 5. Modo de Geração

Pergunte:

```
Como você quer que eu gere a copy?

1. Bloco a bloco (recomendado). Eu gero um bloco, mostro, você valida e só então passo para o próximo. Mais lento, qualidade maior, você corrige o rumo antes de acumular erro.
2. Em 2 partes. Gero Blocos 01 a 08 de uma vez, depois 09 a 15, e só então você revisa tudo. Mais rápido, exige revisão maior no fim.
3. Tudo de uma vez. Gero os 15 blocos em sequência sem pausa. Só revise no fim.

Digite o número:
```

**Modo 1. Bloco a bloco.** Para cada NN de 01 a 15:
1. Gere o bloco com o título exato `## Bloco NN — Nome`.
2. Aplique a revisão (Passo 6) só nesse bloco.
3. **Acumule internamente** o bloco aprovado em memória (não salvar arquivo nenhum no disco. esta skill não salva). Mantenha a lista de blocos aprovados pra montar o documento final no Passo 7.
4. Mostre o bloco no chat e pergunte:
   ```
   Bloco NN/15 pronto.
   1. Aprovar e ir para o próximo
   2. Ajustar este bloco (diga o que mudar)
   3. Pausar aqui (posso retomar depois)
   ```

**Modo 2. Duas partes.** Gere Blocos 01 a 08 em sequência, mostre no chat, peça aprovação. Gere Blocos 09 a 15, mostre, peça aprovação final. Não salvar arquivo durante o processo. acumular em memória pra entregar tudo junto no Passo 7.

**Modo 3. Tudo de uma vez.** Gere os 15 em sequência sem pausa. Acumule em memória. Mostre tudo no chat na hora da entrega final (Passo 7).

### Passo 6. Revisão Obrigatória Antes de Mostrar

**Carregar:** `references/manual-copy.md` (Parte 4. Checklist de entrega).

Para todo bloco gerado, aplicar **Bloco A (vícios absolutos)** + **Bloco B (argumento e especificidade)** + **Bloco C (estrutura)** + **Bloco D (seções de página)**. Se qualquer item falhar, **reescrever o trecho** antes de mostrar ao usuário.

Critérios mínimos que tudo precisa passar:

**Bloco A. Vícios absolutos (zero tolerância):**
- Zero travessões (— ou –)
- Zero pontos de exclamação (!)
- Zero estrutura "Não é X. É Y."
- Zero perguntas no gancho ou primeira linha
- Zero "mesmo que" ou "sem precisar" como muleta
- Zero emojis
- Nome do produto, método, curso ou sigla ausente das primeiras linhas (até o Bloco 05)

**Bloco B. Argumento e especificidade:**
- Toda promessa tem dado concreto (número, prazo, cenário)
- A copy tem tese (explica **por que** o problema existe, não só descreve)
- Zero lero-lero (palavras genéricas de nicho que não dizem nada. ex: "padrão interno", "caminhos terapêuticos", "processos emocionais")
- Zero siglas ou técnicas sem explicação no mesmo parágrafo
- Especificidade presente (números, situações reais, detalhes verificáveis)

**Bloco C. Estrutura:**
- Copy ensina ou avisa em vez de vender
- Pelo menos um conceito com nome próprio criado
- Inimigo concreto identificado (ou cenário inevitável)
- Razão **e** emoção presentes
- Promessa **e** benefício defendidos (transformação técnica + consequência tangível)
- Dor real, não a superficial que o cliente diz primeiro

**Bloco D. Seções de página:**
- Toda seção começa com headline curiosa (não rótulo. "Como funciona o método" é rótulo. "Por que a maneira que você aprendeu na faculdade está custando pelo menos R$ 20 mil por projeto" é headline.)
- Depoimentos têm antes + resultado + prazo (palavras-chave em **negrito**)
- Autoridade com números/conquistas concretas
- Bônus ancorados com preço de mercado
- Método com mecanismo + comparação antes/depois + especificação + prova curta

Após aplicar correções, informe ao usuário em uma linha:
```
Revisão concluída. [N] ajuste(s) aplicado(s) antes de mostrar.
```

---

## Regras de Promessa (Bloco 01. Headline)

A promessa é o headline principal da hero. É o argumento que leva o leitor à Big Idea sem parecer promessa direta.

**Critérios obrigatórios:**
- Até 10 palavras
- Foco em um único resultado (sem conjunção aditiva "e")
- Gera curiosidade e desejo de saber mais
- Memorável e específica para o nicho
- Afirmação direta, não revela todos os detalhes

**O que a promessa NÃO é:**
- Slogan ou frase motivacional
- Explicação longa sobre o produto
- Promessa vaga ou abstrata
- Começa com verbo no imperativo
- Contém interrogação ou exclamação
- Usa "através de" ou "com" para sugerir o caminho
- Usa conjunção aditiva ("e") para transmitir mais de um resultado

**Exemplos validados:**
- Tem gente cobrando R$ 800 por uma página feita com IA em 3 horas.
- O segredo das finanças não é quanto você ganha, mas quanto você consegue manter.
- Guardar dinheiro é bom, mas fazer o dinheiro trabalhar por você é melhor.
- Quem vende barato vende menos.
- Ansiedade não é normal.
- Todo paciente tem cura.
- Pessoas bonitas usam maquiagem.
- Não precisa abrir uma empresa para ficar rico.
- A melhor receita de sobremesa não exige forno nem açúcar.
- Economizar pode ser o maior erro financeiro que você pode cometer.
- O método certo pode transformar uma rotina exaustiva em um negócio que roda sozinho.
- Você pode criar um estilo de vida saudável com 15 minutos por dia.

**Padrões de estrutura que funcionam:**
- "O melhor jeito de [conseguir X] é [fazer Y]."
- "Todo mundo pode [alcançar X] se souber [fazer Y]."
- "Afirmação contra-intuitiva que inverte a crença mais comum do nicho."
- "Dado ou fato específico que o público não esperava ver."

---

## Passo 7. Entrega Final. Documento Consolidado no Chat

> Esta skill **não salva arquivos** em pasta de projeto, não cria diretório, não toca em estrutura externa nenhuma. A entrega final é um documento Markdown único apresentado no chat, que o usuário copia ou baixa pela própria interface (botão de copiar, exportar markdown, ou simplesmente selecionar e colar).

Quando todos os 15 blocos estiverem aprovados (ou gerados, dependendo do modo escolhido no Passo 5), monte **um único bloco de código Markdown** com a copy completa e apresente no chat. Antes do bloco de código, escreva uma linha curta de entrega:

```
Documento final. Copia o bloco abaixo (ou usa o botão de copiar) e cola onde quiser (Notion, Google Docs, template HTML, ferramenta de página, email).
```

Em seguida o documento completo, dentro de um único fence ```` ```markdown ````:

````markdown
# Copy. {Nome do Produto}

> Produto: {nome}
> Preço: {preço + parcelamento}
> Ângulo: {ângulo escolhido}
> Data: {data atual no formato DD/MM/AAAA}

---

## Bloco 01 — Hero

[conteúdo aprovado do bloco]

---

## Bloco 02 — Dor

[conteúdo aprovado do bloco]

---

[... seguir os 15 blocos na ordem ...]

---

## Bloco 15 — Oferta final

[conteúdo aprovado do bloco]
````

Os títulos `## Bloco NN — Nome` são **obrigatórios** e devem permanecer exatamente assim, para que a copy possa ser preenchida depois em qualquer template HTML, sem perder fidelidade entre texto aprovado e página final.

Depois do documento, encerre com uma linha curta:

```
Copy completa entregue. 15 blocos no padrão Light Copy, prontos pra colar onde precisar.
```

**Nada além disso.** Não oferecer próxima skill, não encaminhar pra HTML, não sugerir salvar em pasta, não criar artefato no disco.

---

## Quando o usuário pedir ajuste depois de aprovar um bloco

Edite **apenas o bloco solicitado**. Não reescreva blocos vizinhos. Não corrija o que não foi pedido. Se notar outro problema, mencione depois da entrega, separado, como sugestão opcional. Nunca corrija sem autorização.

---

## Referências

- `references/template-copy-pagina-vendas.md`. Estrutura obrigatória dos 15 blocos.
- `references/manual-copy.md`. 15 princípios fundamentais, 20 vícios proibidos e checklist de entrega (Blocos A, B, C, D).
- `references/checklist-light-copy.md`. Lista resumida das 12 proibições absolutas para verificação rápida.
