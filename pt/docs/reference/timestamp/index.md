# Registros de data e hora

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/

Carimbos de data e hora RFC 3161 para pontos de verificação assinados: o que é enviado à autoridade e como a resposta é verificada.

O TgWitness prepara solicitações RFC 3161 e verifica as respostas da autoridade de carimbo de data/hora (TSA). Este procedimento manual não seleciona uma TSA nem envia dados; o modo de evidência realiza ambas as ações de acordo com uma programação ([formato de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Uma solicitação preparada **ainda não** constitui **uma prova de carimbo de data/hora**.

## O que a prova comprova

Diagrama de fluxo · Observações sobre a conta → Cadeia SHA-256 e assinaturas Ed25519; Cadeia SHA-256 e assinaturas Ed25519 → Ponto de verificação assinado; Ponto de verificação assinado → Hash exato em bytes e nonce aleatório; Hash exato em bytes e nonce aleatório → Solicitação RFC 3161; Solicitação RFC 3161 → TSA independente; TSA independente → Resposta assinada da TSA; Ponto de verificação assinado → Verifique os dados, o nonce e a confiança explícita na CA; Resposta assinada da TSA → Verifique os dados, o nonce e a confiança explícita na CA · Observações sobre aconta · Cadeia SHA-256 eassinaturas Ed25519 · Ponto de verificaçãoassinado · Hash exato em bytes enonce aleatório · Solicitação RFC 3161 · TSA independente · Resposta assinada daTSA · Verifique os dados, ononce e a confiançaexplícita na CA

**Diagrama em formato de texto**

1. Observações sobre a conta → Cadeia SHA-256 e assinaturas Ed25519
2. Cadeia SHA-256 e assinaturas Ed25519 → Ponto de verificação assinado
3. Ponto de verificação assinado → Hash exato em bytes e nonce aleatório
4. Hash exato em bytes e nonce aleatório → Solicitação RFC 3161
5. Solicitação RFC 3161 → TSA independente
6. TSA independente → Resposta assinada da TSA
7. Ponto de verificação assinado → Verifique os dados, o nonce e a confiança explícita na CA
8. Resposta assinada da TSA → Verifique os dados, o nonce e a confiança explícita na CA

A assinatura do coletor vincula os registros à sua chave. Uma resposta confiável da TSA pode comprovar que um determinado ponto de controle existia na hora declarada pela TSA. O ponto de controle pode, então, vincular o prefixo do registro. Isso não determina a hora de cada ação no Telegram nem a veracidade do conteúdo capturado.

## Procedimento

1. Conserve a impressão digital da chave do coletor por meio de um canal confiável separado. Uma chave fornecida apenas pelo arquivo ZIP examinado é insuficiente para identificar o coletor.
2. Em **Exportações → Preparar solicitação de carimbo de data/hora**, baixe o arquivo ZIP da solicitação do espaço de trabalho selecionado. Extraia `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` e `README.txt`. Não altere os bytes de verificação.
3. Escolha um TSA adequado à investigação. Envie `timestamp.tsq` utilizando o método documentado, com `application/timestamp-query` para um serviço HTTP. Salve a resposta binária original como `timestamp.tsr`, o endpoint, a hora da recuperação e o resultado da solicitação. A solicitação contém um hash e um nonce, em vez de mensagens; os metadados de rede ainda revelam a solicitação.
4. Obtenha o certificado raiz confiável independentemente da resposta, além de quaisquer certificados intermediários necessários. Um certificado presente na resposta não se torna confiável simplesmente por estar incluído nela.
5. A partir de uma instalação confiável do TgWitness, verifique:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Adicione `--intermediates tsa-intermediates.pem` ou `--openssl /path/to/openssl`, se necessário. O OpenSSL deve oferecer suporte a `ts`. No Windows, o verificador também procura na instalação padrão do Git. O OpenSSL 3.5.9 foi testado localmente com uma CA/TSA sintética.

1. Exporte um arquivo ZIP do registro assinado após o ponto de verificação, de modo que ele inclua esse prefixo. Verifique utilizando a impressão digital reconhecida de forma independente:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Preserve o arquivo ZIP, o ponto de verificação, a solicitação, a resposta, a cadeia de certificados, os resultados da verificação e o registro de transferência fora do coletor. Repita a verificação no momento do recebimento.

Para preparar uma solicitação a partir de um ponto de verificação salvo:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

A preparação canoniza o JSON e inclui o ponto de verificação correspondente no arquivo. Utilize os **bytes do ponto de verificação desse arquivo** para a verificação TSA, mesmo que o arquivo de entrada apresentasse espaços em branco diferentes.

## Limites da verificação

| Verificar | Comportamento atual |
| --- | --- |
| Dados | O SHA-256 dos bytes exatos do ponto de verificação deve corresponder à resposta |
| Solicitação | Com o `--request`, a consulta original e o nonce são verificados |
| Assinatura da TSA | O OpenSSL verifica a assinatura e a cadeia de certificação até a CA explicitada |
| Assinatura do coletor | Verificado separadamente pelo verificador de registros com uma chave fixada |
| Revogação | Sem recuperação automática de OCSP/CRL |
| Validade a longo prazo | Não há validação do arquivo após o vencimento do certificado |
| Envio programado | Modo de evidência, desativado por padrão |

O `--request` é tecnicamente opcional, mas sua omissão impede a verificação do nonce original. Para este procedimento completo, o resultado `request_checked` deve ser verdadeiro. A verificação do certificado segue as regras e o tempo de verificação do OpenSSL instalado. A preservação de longo prazo requer uma política separada de certificados e evidências de revogação.

Uma assinatura criptográfica válida não constitui automaticamente um carimbo de data/hora qualificado nem uma determinação de admissibilidade jurídica. Caso um operador tenha falsificado observações antes da aplicação do carimbo de data/hora, o TSA fixa esses bytes; isso não comprova sua veracidade.

## Registro de transferência

Registre o identificador do caso, o remetente e o destinatário, a hora da transferência em UTC e sua fonte, finalidade, nomes de arquivos/valores SHA-256, impressão digital do coletor, intervalo de sequência, lacunas conhecidas, versão do verificador e resultado da verificação. Assine e mantenha esse registro de forma independente por meio do processo da sua organização. Um sistema de registro de custódia para múltiplos usuários não está implementado no TgWitness.

Nenhuma TSA independente em tempo real foi contatada durante o desenvolvimento. Testes locais criam uma CA/TSA sintética para verificar a compatibilidade e a rejeição de dados alterados, nonce ou CA.
