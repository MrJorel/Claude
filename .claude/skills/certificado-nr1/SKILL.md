# Skill: Certificado NR1

Gera o certificado de conclusão do Método NR1 Trabalhista para um aluno.

## Quando usar
Quando o usuário pedir para gerar, emitir ou criar um certificado do NR1 (ou chamar /certificado-nr1).

## Passos

1. Perguntar: "Qual o nome completo do aluno?"
2. Capturar a data atual no formato DD/MM/AAAA (usar a data real do sistema)
3. Ler o template em: `clientes/LBR/certificado-nr1.html`
4. Criar uma cópia com o nome do aluno e a data preenchidos:
   - Substituir `[Nome do Aluno]` pelo nome informado
   - Substituir `[data de conclusão]` pela data atual
   - Salvar o arquivo como: `clientes/LBR/certificados/NR1 - [Nome do Aluno].html`
     (criar a pasta `certificados/` se não existir)
5. Abrir o arquivo gerado no navegador com o comando `open`
6. Confirmar: "Certificado gerado para [nome] em [data]."

## Observações
- O template usa a logo real em `clientes/LBR/Logo NR1/Prancheta 4 (2).png`
- A cidade é sempre Curitiba (já fixada no template)
- Não alterar o template original — sempre criar uma cópia
- Não pedir confirmação antes de gerar, apenas o nome do aluno
