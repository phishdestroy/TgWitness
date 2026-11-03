# Veja como funciona o registro de evidências

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/concepts/

Uma mensagem pode ser alterada. O registro do que o senhor observou deve permanecer verificável.

Explore dois pequenos experimentos a seguir. Eles utilizam mensagens fictícias, permanecem no seu navegador e nunca se conectam ao Telegram.

## De uma exportação de bate-papo a um registro verificável

[As exportações do Telegram Desktop](https://telegram.org/blog/export-and-more) salvam o histórico de bate-papo e as mídias disponíveis como HTML ou JSON para uso offline. O TgWitness adiciona um registro contínuo das alterações recebidas, assinaturas nas observações e exportações, além de pontos de verificação que os destinatários podem comparar de forma independente.

| Tarefa | Exportação do Telegram Desktop | TgWitness |
| --- | --- | --- |
| Ler conversas salvas | HTML ou JSON com mídia selecionada | Bate-papos salvos, diário pesquisável e relatórios offline |
| Acompanhe as mudanças ao longo do tempo | O histórico disponível ao ser exportado | Versões capturadas anteriormente, edições posteriores e observações de exclusão são mantidas juntas |
| Verifique os arquivos após a entrega | Os arquivos de exportação padrão em HTML/JSON não são assinados | Manifesto assinado, assinaturas por registro e relatórios HTML/PDF/JSON selados, verificados em relação a uma chave de coletor confiável |
| Compare com um estado anterior mantido | Mantenha uma cópia de referência separada ou um hash | Pontos de verificação assinados, uma testemunha separada e carimbos de data/hora externos opcionais |

A comparação de assinatura de arquivos baseia-se nos [geradores de exportação](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) do [Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) revisados em 2 de novembro de 2026. O TgWitness assina com a chave do coletor; as verificações abaixo mostram como um destinatário a utiliza.

## Uma mensagem, três observações

Quando o Telegram entrega uma nova mensagem, uma edição ou um aviso de exclusão, o coletor acrescenta três observações distintas. A edição não substitui o registro original. Um aviso de exclusão não o apaga.

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

Uma notificação de exclusão não fornece nem a hora confiável da exclusão nem a identidade da pessoa que excluiu a mensagem. Manter esses valores desconhecidos preserva a distinção entre uma observação e uma suposição.

## Altere um registro. Siga o hash.

Cada registro contém o hash do registro anterior. Seu próprio hash abrange os campos do evento, incluindo esse link. Um ponto de verificação mantido externamente fixa um comprimento específico do diário e o hash inicial.

02 / HASH-CHAIN SANDBOXSHA-256 real · registros de amostra

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

**C** serializa os nove campos do evento como JSON em UTF-8: chaves ordenadas, sem espaços em branco extras, sem escape ASCII e sem NaN/infinito. O `previous_hash` do evento é hi−1. O h0 exibido significa 64 caracteres zero; as assinaturas abrangem os 32 bytes brutos do resumo.

Os nove campos são `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` e `previous_hash`. Esta é [a codificação JSON documentada](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#event-canonicalization) do TgWitness; o hash e a assinatura em si não são campos de entrada de hash.

PONTO DE VERIFICAÇÃO RETIDO

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Verifique a assinatura do ponto de verificação sob a chave do coletor fixada e, em seguida, compare seus limites com os do registro verificado. Uma exportação posterior pode conter mais registros; mesmo assim, deve estar em conformidade com o ponto de verificação anterior.

## Três perguntas, três verificações diferentes

[01 / INTEGRIDADE**Este registro sofreu alguma alteração?** Verifique os hashes e as assinaturas em relação a uma chave confiável separada.](https://phishdestroy.github.io/TgWitness/pt/docs/exports/)[02 / CONTINUIDADE**O que foi mantido anteriormente?** Compare uma exportação assinada com os pontos de verificação mantidos por uma testemunha independente.](https://phishdestroy.github.io/TgWitness/pt/docs/witness/)[03 / ENTREGA**Esses eventos de teste chegaram?** Compare as ações controladas de envio, edição e exclusão com o registro de cada conta.](https://phishdestroy.github.io/TgWitness/pt/docs/cases/)

Use assinaturas para verificar os registros retidos, pontos de verificação para comparar um limite anterior e testes de entrega controlada para avaliar a coleta. Cada um responde a uma pergunta específica. [Leia o escopo da verificação e as premissas de confiança.](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope)

Acompanhe toda a [investigação da conta,](https://phishdestroy.github.io/TgWitness/pt/docs/cases/) desde a aquisição até o pacote do caso.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
