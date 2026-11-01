# Evidências e confiança

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence-trust/

O que as exportações, vídeos, arquivos da web e registros assinados podem comprovar, e como o dispositivo de coleta afeta sua confiabilidade.

Uma exportação, captura de tela ou gravação pode ser uma evidência útil. Sua confiabilidade depende de como foi coletada, preservada e corroborada. **Um hash ou assinatura válida verifica o material salvo; ela não comprova, de forma independente, que o dispositivo de coleta recebeu conteúdo de fonte autêntico.** Esse limite também se aplica ao TgWitness.

Este guia separa a verificação técnica da avaliação jurídica. A documentação do produto e as disposições legais abaixo foram revisadas em 1º de novembro de 2026; a comparação da Hunchly descreve sua documentação publicada, não uma nova auditoria do produto.

## Quando a confiança entra na captura

Diagrama de fluxo · Conta e serviço do Telegram → Cliente, navegador e sistema operacional; Cliente, navegador e sistema operacional → Exportação, captura de vídeo ou de página; Exportação, captura de vídeo ou de página → Hashes e assinaturas do coletor; Hashes e assinaturas do coletor → Hash mantido por uma parte independente · Conta e serviço doTelegram · Cliente, navegador esistema operacional · Exportação, captura devídeo ou de página · Hashes e assinaturasdo coletor · Hash mantido por umaparte independente

**Diagrama em formato de texto**

1. Conta e serviço do Telegram → Cliente, navegador e sistema operacional
2. Cliente, navegador e sistema operacional → Exportação, captura de vídeo ou de página
3. Exportação, captura de vídeo ou de página → Hashes e assinaturas do coletor
4. Hashes e assinaturas do coletor → Hash mantido por uma parte independente

O modelo de ameaça aqui pressupõe que um invasor ou operador possa alterar o ambiente de coleta antes que as evidências sejam confirmadas. Trata-se de uma análise condicional, não de uma alegação de que um determinado dispositivo ou produto tenha sido comprometido.

Um cliente oficial e uma conexão criptografada ajudam a proteger o uso normal. Eles não tornam o sistema operacional, o navegador ou a tela ao redor, por si só, confiáveis. Se o conteúdo for substituído após a descriptografia, mas antes da captura, o exportador poderá salvá-lo com precisão e o signatário poderá assiná-lo corretamente. Nenhuma das operações requer um algoritmo de hash comprometido ou uma assinatura falsificada.

Um vídeo gravado no mesmo dispositivo pode registrar a mesma apresentação substituída. Uma câmera separada pode confirmar o que a tela exibia, mas a tela por si só não autentica o que o Telegram forneceu. Da mesma forma, HTML, JSON, capturas de tela e registros do navegador correspondentes de um único ambiente controlado podem compartilhar a mesma falha. A concordância entre eles é um contexto útil; não constitui automaticamente uma corroboração independente.

## O que cada tipo de evidência contribui

| Material | Contribuição útil | Questão pendente |
| --- | --- | --- |
| Exportação do Telegram Desktop | Conversas legíveis ou legíveis por máquina e mídias selecionadas | Quem controlava os arquivos do cliente e de exportação, e o que estava disponível ou foi excluído? |
| Captura de tela ou gravação de tela | Contexto visível, sequência de ações e apresentação | A apresentação reflete fielmente a fonte e o que aconteceu fora da gravação? |
| Arquivo local da web, incluindo MHTML | Conteúdo da página e recursos associados para análise posterior | O que o navegador forneceu ao arquivador, e quem controlava esse navegador? |
| Arquivo assinado pelo coletor | Alterações nos bytes assinados podem ser detectadas em relação a uma chave confiável e a uma referência mantida | Quem controlava a chave de assinatura e os dados de entrada antes da assinatura? |
| Ponto de verificação mantido de forma independente ou carimbo de data/hora verificado | Um hash ou ponto de verificação mantido para comparação com um envio posterior | Quais bytes e limites são abrangidos, e o que a parte independente realmente atesta? |

O Telegram documenta sua exportação do Desktop como uma cópia offline em HTML/JSON e sua API Takeout como uma forma de recuperar dados selecionados da conta. Essas descrições não fornecem uma assinatura do Telegram no arquivo final exportado para que o destinatário possa verificá-lo. Nossa conclusão se limita a esses mecanismos de exportação documentados; não se trata de uma afirmação de que as evidências do Telegram não tenham valor jurídico.[Exportação do Telegram Desktop](https://telegram.org/blog/export-and-more),[API Takeout](https://core.telegram.org/api/takeout).

A mesma distinção se aplica a solicitações em segundo plano, entradas de cache e registros de rede. Eles podem revelar inconsistências e ajudar a corroborar uma coleta. Sua complexidade, por si só, não determina quem os produziu. Um arquivo operado de forma independente ou um registro de serviço obtido separadamente introduz uma fonte diferente para comparação, sujeita às suas próprias limitações de coleta e custódia.

## O Hunchly ilustra o mesmo limite

A documentação do Hunchly descreve o hash SHA-256 de capturas MHTML, fotos e anexos, com verificação independente do hash. Ela também explica por que um arquivo alterado acompanhado de um hash recém-calculado pode passar nessa comparação e aponta para assinaturas e corroboração da fonte como verificações adicionais.[Hunchly: hash de conteúdo, fotos e anexos](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

Seu *Guia de Provas* publicado, revisão 1.0 de 17 de outubro de 2018, descreve chaves GPG e assinaturas geradas localmente para capturas MHTML. Ele identifica explicitamente o acesso à chave privada local como uma forma de assinar novamente o material modificado. Trata-se de uma limitação de confiança documentada, não de evidência de uma vulnerabilidade atual não divulgada. O guia também afirma que o Chrome realiza a captura MHTML. Descrever o Hunchly como baseando-se apenas na reputação de um investigador omitiria esses controles técnicos.[Guia de Evidências do Hunchly, seções 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

A admissibilidade de material coletado com um determinado produto em um processo depende da decisão e das circunstâncias relevantes. Não fazemos aqui nenhuma afirmação sobre a frequência com que os tribunais aceitam o Hunchly ou o TgWitness, nem sobre qualquer um dos produtos ter aprovação geral dos tribunais.

## O que o TgWitness acrescenta e até onde vai sua proteção

O TgWitness regista observações num diário assinado e vinculado e fornece exportações que o destinatário pode verificar. Pontos de verificação retidos, carimbos de data/hora e uma testemunha separada fornecem aos revisores referências além dos arquivos atuais do coletor. Eles ajudam a revelar alterações em registros previamente confirmados. Registros de cobertura e resultados explícitos da coleta ajudam a explicar o que foi e o que não foi capturado.[Formato e transferência de evidências](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/), [escopo da coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/).

O momento de uma possível substituição é importante:

1. **Após a assinatura, sem acesso à chave de assinatura:** a alteração de um registro assinado ou de um arquivo vinculado ao manifesto falhará na verificação com um verificador confiável e a chave correspondente.
2. **Com a chave do coletor, após um ponto de verificação independente ter sido mantido:** um diário de substituição pode ter novas assinaturas válidas, mas um prefixo alterado falha na comparação com aquele ponto de verificação anterior. Um ponto de verificação mantido apenas no mesmo dispositivo controlado pode ser substituído juntamente com o diário. Registros além do limite mantido precisam de cobertura própria.
3. **Antes que um ponto de verificação que abranja uma observação seja mantido de forma independente:**dados falsos podem ser assinados e ancorados com sucesso, incluindo novos registros anexados após um ponto de verificação anterior. O ponto de verificação ou carimbo de data/hora resultante ainda abrange esses registros falsos; ele não atesta sua veracidade.

Uma testemunha TgWitness recebe os pontos de verificação assinados pelo coletor; ela não lê de forma independente a conversa subjacente no Telegram. Sua chave e seus registros mantidos devem ser considerados confiáveis separadamente. Quando todo o diário enviado precisar ser testemunhado, use o[procedimento de transferência que exige o limite final de exportação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#require-a-witnessed-export-boundary). Uma verificação de integridade comum ainda pode relatar uma parte final não testemunhada.

Uma resposta RFC 3161 verificada pode comprovar que um ponto de verificação existia na hora declarada pela autoridade. Ela não comprova quando uma mensagem do Telegram foi enviada nem se seu conteúdo era verdadeiro. Uma solicitação preparada ou um arquivo de resposta incluído por si só é insuficiente. Ao verificar uma exportação com `tgwitness.verify`, a verificação das assinaturas TSA incluídas requer uma CA explicitamente confiável por meio de `--tsa-ca`. Os recibos do OpenTimestamps precisam de `ots verify` independente, com atualizações de prova quando necessário. [Procedimento de carimbo de data/hora](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

[Na captura do GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), um executador hospedado temporariamente coleta as mensagens. O atestado vincula o arquivo a um fluxo de trabalho aprovado. Esse modo ainda confia no GitHub, no software e nas dependências aprovadas, no auxiliar/navegador e no túnel. Não se trata de hardware confidencial, de uma assinatura do Telegram ou de prova de que ninguém acessou o host. Um recibo de execução assinado localmente também é uma medição auto-relatada, não um atestado de hardware.

## O peso jurídico depende da base

Quatro questões devem permanecer distintas: se o item é o que se afirma que seja, se os bytes enviados correspondem ao registro mantido, se o conteúdo corrobora os fatos alegados e se as regras aplicáveis permitem seu uso. Uma verificação criptográfica aborda apenas parte dessa base.

Em processos federais dos EUA, a Regra 901 prevê formas de autenticar provas, incluindo depoimentos de testemunhas com conhecimento de causa e provas sobre um processo ou sistema. As Regras 902(13) e 902(14) estabelecem vias de certificação para determinados registros e cópias eletrônicas, com requisitos processuais. As notas da comissão distinguem a autenticação de questões como boatos, relevância e atribuição. Uma assinatura de software, por si só, não constitui a certificação da pessoa qualificada descrita nessas regras.[Regra Federal de Provas 901](https://www.law.cornell.edu/rules/fre/rule_901),[Regra Federal de Provas 902](https://www.law.cornell.edu/rules/fre/rule_902).

Nos casos em que se aplica a Lei de Provas do Canadá, a seção 31.1 trata da autenticação de documentos eletrônicos. A seção 31.2 vincula a regra da melhor prova à integridade do sistema ou a uma presunção aplicável; a seção 31.3 especifica as circunstâncias para uma presunção de integridade. Trata-se de condições probatórias definidas, e não de uma presunção geral de que qualquer investigador licenciado ou produto comercial seja infalível. [Lei de Provas do Canadá, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Esses exemplos não determinam a admissibilidade em outra jurisdição ou em um caso específico. As verificações técnicas devem ser aplicadas de forma consistente ao material que apoie ou conteste uma alegação. Este guia não afirma que as provas da acusação sejam, em geral, mais fáceis de serem admitidas do que as provas da defesa.

## Prepare um registro que outra pessoa possa avaliar

- Descreva a conta, o dispositivo de coleta, o operador, a versão do software, os direitos de acesso, o escopo selecionado e o período de coleta. Registre interrupções e possíveis comprometimentos, em vez de tratar uma verificação de assinatura bem-sucedida como um teste de dispositivo limpo.
- Mantenha os pacotes originais e registre as transferências, os hashes e a fonte da data e hora. Mantenha a impressão digital da chave e os pontos de verificação por meio de um canal confiável separado. Verifique a cobertura real das testemunhas ou dos carimbos de data e hora antes de descrevê-la em um relatório.
- Busque corroboração independente adequada à alegação: registros de outro participante, uma captura independente ou registros de serviço obtidos legalmente. Explique sua independência e limitações; a concordância entre cópias, por si só, não é suficiente.
- Preserve o contexto relevante. Identifique arquivos omitidos, histórico indisponível e redações. Prepare uma [divulgação minimizada separada](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)quando necessário e descreva suas transformações sem apresentá-la como o original completo.
- Forneça ao destinatário instruções de verificação e o material necessário para essas verificações. Mantenha as observações, as constatações técnicas e as conclusões do analista claramente diferenciadas.

Para uma transferência específica, indique o hash do arquivo, a chave confiável, o resultado da verificação e o limite exato coberto externamente. Descreva a autenticidade da fonte, a atribuição da conta, a integridade e as conclusões jurídicas separadamente. Isso fornece ao próximo revisor alegações específicas para examinar.
