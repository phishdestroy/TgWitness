# Como funciona a evidência

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/how-it-works/

Cadeia de hash, assinaturas, pontos de verificação e testemunhas explicados com as fórmulas exatas utilizadas pelo verificador.

O TgWitness preserva o que uma conta coletora observou, vincula essas observações a um registro assinado e permite que outra pessoa verifique uma exportação por meio de uma chave confiável e de um ponto de verificação retido anteriormente.

O [site de documentação local](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) inclui exemplos interativos em `/docs/concepts/` e um explorador de decisões de pontos de verificação em `/docs/witness/`. Todas as mensagens de exemplo, contagens e atrasos são fictícios. Os hashes na sandbox da cadeia são calculados com SHA-256 no navegador. Nada é enviado ao Telegram.

## Uma mensagem é alterada; as observações se acumulam

Diagrama de sequência · Telegram → Coletor: Nova mensagem: Encontro às 10h; Coletor → Registro assinado: Adicionar mensagem.nova; Telegram → Coletor: Atualização: Encontro às 11h; Coletor → Registro assinado: Adicionar mensagem.editada; Telegram → Coletor: Aviso de exclusão; Coletor → Registro assinado: Anexar mensagem.excluída; Nota sobre Registro assinado: As observações relativas ao original, às edições e às exclusões permanecem · Telegram · Coletor · Registro assinado · Nova mensagem: Encontro às 10h · Adicionar mensagem.nova · Atualização: Encontro às 11h · Adicionar mensagem.editada · Aviso de exclusão · Anexar mensagem.excluída · As observações relativas ao original, às edições eàs exclusões permanecem

**Diagrama em formato de texto**

1. Telegram → Coletor: Nova mensagem: Encontro às 10h
2. Coletor → Registro assinado: Adicionar mensagem.nova
3. Telegram → Coletor: Atualização: Encontro às 11h
4. Coletor → Registro assinado: Adicionar mensagem.editada
5. Telegram → Coletor: Aviso de exclusão
6. Coletor → Registro assinado: Anexar mensagem.excluída
7. Nota sobre Registro assinado: As observações relativas ao original, às edições e às exclusões permanecem

Esta sequência simplificada pressupõe que o Telegram entregou cada atualização e que a conta selecionada pôde visualizá-la. Eventos operacionais também são registrados no diário. Um aviso de exclusão não indica quem efetuou a exclusão nem a hora exata da exclusão. Entregas repetidas são observações distintas; não há supressão de duplicatas em todo o diário.

## O que um hash abrange

![Observar, codificar, gerar hash e assinar: cada novo evento inclui o hash do evento anterior.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Leia a fórmula de dentro para fora: **C** transforma os nove campos em bytes exatos; **o SHA-256** produz seu resumo; **“hex”** é a forma como esse resumo é armazenado. O hash anterior já está dentro do evento. **“unhex”** transforma o hash armazenado de volta nos 32 bytes que o Ed25519 assina.

[Diagrama estático da cadeia](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Seja C(ei) o JSON UTF-8 canônico dos nove campos de evento. O primeiro `previous_hash` consiste em 64 caracteres zero. Cada registro subsequente inclui o hash hexadecimal do registro anterior:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

A assinatura abrange os 32 bytes brutos do resumo. A entrada do hash contém exatamente `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` e `previous_hash`. As chaves dos objetos são ordenadas; espaços em branco e caracteres de escape ASCII são omitidos; NaN e infinito são rejeitados. Consulte a [codificação exata](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#event-canonicalization).

Diagrama de fluxo · 64 caracteres zero → Registro 1 / hash h1; Registro 1 / hash h1 → O Registro 2 inclui h1 / hash h2; O Registro 2 inclui h1 / hash h2 → O Registro 3 inclui h2 / hash h3; O Registro 3 inclui h2 / hash h3 → Ponto de verificação assinado: contagem 3, título h3 (manter em outro local) · 64 caracteres zero · Registro 1 / hash h1 · O Registro 2 inclui h1/ hash h2 · O Registro 3 inclui h2/ hash h3 · Ponto de verificaçãoassinado: contagem 3,título h3 · manter em outro local

**Diagrama em formato de texto**

1. 64 caracteres zero → Registro 1 / hash h1
2. Registro 1 / hash h1 → O Registro 2 inclui h1 / hash h2
3. O Registro 2 inclui h1 / hash h2 → O Registro 3 inclui h2 / hash h3
4. O Registro 3 inclui h2 / hash h3 → Ponto de verificação assinado: contagem 3, título h3 (manter em outro local)

| Alteração no registro fornecido | O que o identifica |
| --- | --- |
| Altere o registro 2, mantendo seu hash salvo | O hash do evento recalculado difere; sua assinatura não abrange mais o evento alterado |
| Reconstrua o registro alterado e todos os hashes posteriores | As assinaturas originais apresentam falhas; um ponto de verificação retido no limite afetado também apresenta discrepâncias |
| Remova a parte final, mas mantenha o prefixo restante intacto | Um ponto de verificação anterior, mantido além do prefixo fornecido, revela que a exportação está muito curta |
| Reassinar um registro substituto com outra chave | Uma impressão digital de chave confiável, mantida separadamente, rejeita a identidade substituta |

![A alteração de um campo salvo altera seu resumo; a recriação de hashes não restaura as assinaturas originais.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Experimente a lógica no registro 2:** altere `Meet at 11:00` para `Meet at 12:00` no evento salvo. Seu hash recalculado não corresponde mais. Recalcular a cadeia posterior pode reparar seus elos, mas não pode fazer com que as assinaturas originais abranjam os novos resumos. Uma edição observada no Telegram, por outro lado, torna-se um novo registro no diário.

[Diagrama de alterações estáticas](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Os links de hash, por si só, não impedem que alguém recalcule uma cadeia de substituição. A confiança decorre da verificação das assinaturas por meio de uma chave confiável e independente e da comparação com referências mantidas fora do coletor.

## O que um ponto de verificação anterior acrescenta

![Mantenha a contagem 3 e o título h3; uma exportação posterior de 4 registros é verificada na posição 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**A referência permanece inalterada enquanto o registro cresce.** Se o ponto de verificação indicar “3 registros, cabeçalho h3”, uma exportação de quatro registros pode ser aprovada ao corresponder ao h3 na posição 3. Seu cabeçalho mais recente é h4, o qual deve ser diferente. Uma exportação de apenas dois registros falhará.

[Diagrama estático de pontos de verificação](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Após verificar a assinatura do ponto de verificação, solicite:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Uma exportação pode se estender além de um ponto de verificação. Ela deve estar em conformidade no limite retido. O verificador real também verifica a sequência de cada evento, o link anterior, o hash e a assinatura. Comparar apenas o cabeçalho final armazenado deixaria de detectar um registro interno alterado cujo hash salvo não tenha sido atualizado.

## O lugar de uma testemunha

Diagrama de fluxo · Coletor / sessão da conta / chave A → Endpoint de ponto de verificação somente leitura; Witness / chave coletora fixada / chave própria B → Registro de testemunho assinado separado; Witness / chave coletora fixada / chave própria B → Endpoint de ponto de verificação somente leitura (Solicite uma verificação); Endpoint de ponto de verificação somente leitura → Witness / chave coletora fixada / chave própria B (Resposta assinada); Witness / chave coletora fixada / chave própria B → Canal com publicações assinadas do TGW1 (API do bot / token próprio) · Servidor A · Host B · Coletor / sessão da conta/ chave A · Endpoint de ponto deverificação somenteleitura · Witness / chave coletorafixada / chave própria B · Registro de testemunhoassinado separado · Canal com publicaçõesassinadas do TGW1 · Solicite uma verificação · Resposta assinada · API do bot / token próprio

**Diagrama em formato de texto**

1. Coletor / sessão da conta / chave A → Endpoint de ponto de verificação somente leitura
2. Witness / chave coletora fixada / chave própria B → Registro de testemunho assinado separado
3. Witness / chave coletora fixada / chave própria B → Endpoint de ponto de verificação somente leitura (Solicite uma verificação)
4. Endpoint de ponto de verificação somente leitura → Witness / chave coletora fixada / chave própria B (Resposta assinada)
5. Witness / chave coletora fixada / chave própria B → Canal com publicações assinadas do TGW1 (API do bot / token próprio)

A testemunha registra reversões, um cabeçalho diferente com a mesma contagem, chaves alteradas, respostas inválidas e respostas ausentes. Uma contagem maior, por si só, não comprova que todos os registros anteriores permaneçam inalterados; compare a exportação com os pontos de verificação retidos. Uma testemunha em outro servidor evita o risco de ficar sem acesso devido a uma interrupção no servidor do coletor; um operador independente proporciona maior independência.

A testemunha atesta o estado do diário relatado pelo coletor. Ela não observa de forma independente todas as mensagens do Telegram. Consulte [a configuração da testemunha](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/).

## Teste de entrega em relação a ações conhecidas

Utilize um grupo controlado, contas de coleta distintas e um marcador novo. Envie, edite e exclua deliberadamente, verificando a captura entre as etapas. Defina as ações esperadas e um limite antes de inspecionar os resultados.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Apenas as ações esperadas correspondentes são contabilizadas; recibos duplicados não aumentam o numerador. O denominador deve ser diferente de zero. Um recibo ausente não apresenta atraso medido. Documente a incerteza do relógio; utilize seu próprio tempo de ação de exclusão controlado, pois o Telegram não fornece a hora exata da exclusão. Um resultado como 5/6 (83,3%) descreve as ações de teste, não a integridade de todo o tráfego do Telegram.

## Escolha um fluxo de trabalho

[O passo a passo completo da investigação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/investigation/) acompanha um incidente que ocorre em um canal, grupo, bot e conversa privada:

1. Ative o modo de investigação de toda a conta e faça um inventário de todos os chats acessíveis.
2. Obtenha instantâneos do registro, histórico completo por conversa e anexos preservados.
3. Mantenha as alterações em tempo real e quaisquer interações deliberadas no painel com seus registros.
4. Acompanhe IDs numéricos de remetentes, relações de respostas, destinos repetidos e hashes de arquivos por meio de registros citados e perfis de pessoas.
5. Reconstrua uma linha do tempo entre conversas com registros de data e hora e lacunas explícitas.
6. Compare os espaços de trabalho de outras contas, mantendo suas origens e chaves separadas.
7. Reúna e verifique os registros assinados, perfis e exportações de histórico com notas do caso.

O guia `/docs/cases/` do site inclui um mapa interativo de casos e variantes para disputas envolvendo bots, mensagens removidas e participantes que alteram seus nomes. As anotações de caso e a análise entre espaços de trabalho são externas; o aplicativo não gera automaticamente um gráfico global de investigação nem um arquivo de casos consolidado.

[Validação concluída e trabalho pendente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/) · [Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#investigation-handoff) · [Comece com uma conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/)
