# Veja como funciona o registro de evidências

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/concepts/

Mensagens mudam. O seu registro do que você viu não deveria, e qualquer pessoa deveria poder conferir isso.

Dois pequenos experimentos abaixo. Mensagens fictícias, tudo roda no seu navegador, nada vai para o Telegram.

## De uma exportação de bate-papo a um registro verificável

Uma [exportação do Telegram Desktop](https://telegram.org/blog/export-and-more) salva o histórico que você vê agora em HTML ou JSON. O TgWitness acrescenta um diário contínuo de mudanças, assinaturas em cada registro e pontos de verificação com os quais outros podem comparar.

| Tarefa | Exportação do Telegram Desktop | TgWitness |
| --- | --- | --- |
| Ler conversas salvas | HTML ou JSON com mídia selecionada | Bate-papos salvos, diário pesquisável e relatórios offline |
| Acompanhe as mudanças ao longo do tempo | O histórico disponível ao ser exportado | Versões antigas, edições posteriores e exclusões, tudo guardado |
| Verifique os arquivos após a entrega | Os arquivos de exportação padrão em HTML/JSON não são assinados | Manifesto assinado, registros assinados e relatórios selados, conferidos com uma chave confiável |
| Compare com um estado anterior mantido | Mantenha uma cópia de referência separada ou um hash | Pontos de verificação assinados, uma testemunha separada e carimbos de data/hora externos opcionais |

A comparação se baseia no [código de exportação do Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) em 2 de novembro de 2026.

## Uma mensagem, três observações

Uma mensagem nova, uma edição e uma exclusão viram três registros separados. A edição não sobrescreve o primeiro e a exclusão não o apaga.

01 / PERCURSO DA MENSAGEMSequência ilustrativa

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Coletor · Registro · atualização → · acrescentar →

VISUALIZAÇÃO ATUAL DO CHAT Mensagem nº 42

Mensagem excluída

A mensagem desapareceu da visualização do chat.

REGISTRO DE OBSERVAÇÕES 3 registros

1. 01

   `message.new`

   Encontro às 10h

   ✓
2. 02

   `message.edited`

   Encontro às 11h

   ✓
3. 03

   `message.deleted`

   Aviso de exclusão para o nº 42

   ✓

Todas as três observações recebidas permanecem no registro.

Caminho simplificado para uma fonte já selecionada. Os registros operacionais também compartilham o diário real. A captura depende do que a conta pode visualizar e do que o Telegram disponibiliza.

O Telegram não diz quem excluiu uma mensagem nem quando exatamente. O TgWitness deixa esses campos vazios em vez de chutar.

## Altere um registro. Siga o hash.

Cada registro contém o hash do anterior. Um ponto de verificação guardado em outro lugar fixa o tamanho do diário e o último hash.

02 / SANDBOX DA HASH-CHAINSHA-256 real · registros de amostra

REGISTRO 01**Mensagem recebida**`h₁ = SHA-256(e₁)`Links para 64 zeros

REGISTRO 02**Encontro às 11h**`h₂ = SHA-256(e₂)`Inclui h₁

REGISTRO 03**Exclusão observada**`h₃ = SHA-256(e₃)`Inclui h₂

ARQUIVADO EM OUTRO LOCAL**3 registros · cabeçalho `h₃`**Compare esse limite fixo com o registro fornecido.

A alteração de um evento modifica seu hash. A reconstrução da cadeia altera seu ponto inicial. A remoção do ponto final torna a cadeia mais curta do que o ponto de verificação retido.

**Inspecione o registro 2 e os hashes completos**

Este é exatamente o JSON em UTF-8 com hash apresentado neste exemplo. Os valores são fictícios; os nove campos e a serialização correspondem ao formato do registro.

```

```

Hash do registro 2 salvo

``

Hash do registro 2 recalculado

``

Este ambiente de teste calcula hashes, não assinaturas. O verificador real também verifica a assinatura Ed25519, a sequência e o link de cada evento. A reconstrução de hashes por si só não permite criar assinaturas válidas sob a chave confiável.

## As regras propriamente ditas, em poucas linhas

HASH + ASSINATURA

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** são os nove campos do evento como JSON UTF-8: chaves ordenadas, sem espaços extras, sem escape ASCII, sem NaN/infinito. `previous_hash` é hi−1, h0 são 64 zeros e as assinaturas cobrem os 32 bytes brutos do resumo.

Os campos: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Especificação completa: [codificação de eventos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#event-canonicalization).

PONTO DE VERIFICAÇÃO RETIDO

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Confira a assinatura do ponto de verificação com a chave fixada e depois compare com o diário. Uma exportação posterior pode ser maior, mas tem de bater no ponto de verificação.

## Três perguntas, três verificações diferentes

[01 / INTEGRIDADE**Este registro sofreu alguma alteração?** Hashes e assinaturas contra uma chave confiável.](https://phishdestroy.github.io/TgWitness/pt/docs/exports/)[02 / CONTINUIDADE**O que foi mantido anteriormente?** Compare a exportação com os pontos de verificação que uma testemunha guardou.](https://phishdestroy.github.io/TgWitness/pt/docs/witness/)[03 / ENTREGA**Esses eventos de teste chegaram?** Envie, edite e exclua mensagens de teste e veja o que cada conta capturou.](https://phishdestroy.github.io/TgWitness/pt/docs/cases/)

Assinaturas respondem "foi alterado?", pontos de verificação respondem "bate com o que havia antes?" e mensagens de teste respondem "capturamos tudo?". [O que a verificação prova e o que não prova.](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope)

Próximo: uma [investigação de conta inteira](https://phishdestroy.github.io/TgWitness/pt/docs/cases/) do começo ao pacote do caso.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
