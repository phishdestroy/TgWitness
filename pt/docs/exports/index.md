# Telegram · Exportar e verificar

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/exports/

Entregue arquivos que o destinatário pode conferir sozinho contra o seu espaço.

Manter uma referênciaExportar ZIP assinadoO destinatário verifica

Novo em assinaturas e pontos de verificação? [Altere um registro de exemplo](https://phishdestroy.github.io/TgWitness/pt/docs/concepts/#chain) e veja quais verificações percebem.

Deseja manter uma cópia fora do controle do coletor? Acesse [a configuração do S3](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3), [o Object Lock](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3-retention) ou [a recuperação verificada](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3-restore).

## Mantenha uma referência confiável

Anote a impressão digital da chave do espaço em algum lugar que não seja o coletor. Durante a coleta, guarde pontos de verificação assinados em outro lugar também ou use uma [testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/witness/). É com isso que o destinatário confere a chave e um estado anterior do diário.

## Baixe o arquivo ZIP assinado

**Exportações** → ZIP de evidência assinado. Ele tem o diário inteiro e um manifesto de arquivos assinado. Monte o relatório legível no [Report studio](https://phishdestroy.github.io/TgWitness/pt/docs/reports/) ou envie só dados selecionados como [extrato de entrega](https://phishdestroy.github.io/TgWitness/pt/docs/handover/).

Relatórios HTML, PDF e JSON têm selos próprios. O CSV é só uma cópia de trabalho; para integridade, use o CSV de dentro do ZIP verificado.

## Verifique com uma cópia confiável do TgWitness

No ambiente do projeto, com sua impressão digital e seus caminhos:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Se passar, aparece `key_pinned: true` e `checkpoint_checked: true`. Guarde essa saída ao lado do arquivo. O ponto de verificação tem de estar no fim da exportação ou antes.

## Utilize o resultado da verificação

- **Arquivos:** o manifesto amarra os hashes e as assinaturas amarram o diário. Qualquer mudança aparece.
- **Identidade:** a impressão digital que você guardou prova que é a chave esperada.
- **Estado anterior:** um ponto de verificação compara a exportação com um prefixo do diário salvo antes da entrega.
- **Cobertura:** lacunas, resultados de aquisição e um teste enviar → editar → excluir mostram o que esta configuração realmente capturou.

Detalhes: [o que a verificação prova e o que não prova](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope).

## Configure a cópia externa no S3

**Exportações → Cópia externa** no seu espaço. Funciona com AWS S3 e qualquer serviço compatível com S3. Copia segmentos do diário, arquivos salvos, pontos de verificação com seus carimbos de tempo e exportações de chats prontas, cada um criptografado com `AES-256-GCM` antes de sair do coletor.

A demo online mostra esses controles com o envio desligado. Só informe credenciais reais na sua própria instalação.

[![Painel completo de cópia externa: endpoint, região, bucket, chaves de acesso, programação, controles de Object Lock e chave de recuperação](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

O painel completo com opções avançadas está expandido. Nenhuma credencial de armazenamento é exibida.

| Campo | O que inserir |
| --- | --- |
| Endpoint | URL do armazenamento, sem caminho de bucket nem credenciais. Exemplo: `https://s3.example.invalid`. |
| Região | O que o seu provedor exigir. Padrão `us-east-1`. |
| Bucket | Um bucket existente onde você possa gravar. Exemplo: `example-case-backup`. |
| Pasta no bucket | Prefixo, padrão `tgwitness`. Um prefixo por espaço é acrescentado. |
| ID da chave de acesso / Chave secreta de acesso | As duas juntas, guardadas no cofre. Deixe ambas vazias depois para mantê-las. |
| Endereços no formato de caminho | Ligado: `endpoint/bucket`. Desligado: `bucket.endpoint`. Depende do provedor. |
| Intervalo de cópia | De 1 a 1.440 minutos, padrão 5. Só enquanto o app está rodando. |
| Retenção do Object Lock | Dias e modo, se o bucket suportar Object Lock. Zero mantém o padrão do bucket. |

1. Crie o bucket, preencha destino e credenciais com **Manter uma cópia externa** desmarcado e clique em **Salvar cópia externa**.
2. **Testar conexão** envia um objeto de teste criptografado.
3. **Baixar chave de criptografia** e guarde longe do coletor. Sem chave, sem recuperação.
4. Marque **Manter uma cópia externa**, salve e depois **Copiar agora** ou deixe o agendamento rodar.

## Verifique a retenção e o andamento da cópia

Em **Mais opções** escolha os dias de retenção e `GOVERNANCE` ou `COMPLIANCE`. O TgWitness lê a retenção de volta de um objeto enviado e informa: confirmada, ausente ou falha na verificação.

O painel mostra a última passada, número de objetos, bytes, limite do diário copiado e erros. Um arquivo local ausente é relatado e tentado de novo na próxima passada; o resto continua copiando.

Os envios vão direto, por SOCKS5 ou por HTTP. Com uma rota só MTProxy, a cópia espera com um erro.

## Guarde a chave de recuperação em local separado

O JSON da chave tem a chave de descriptografia, o destino, o prefixo e a impressão digital da chave. Para recuperar, você precisa dele mais credenciais de armazenamento com leitura.

Mudou endpoint, bucket ou prefixo? Baixe a chave de novo. Uma cópia nova começa no novo destino; exportações antigas ficam onde estavam.

## Restaurar e verificar em outro computador

Você precisa de uma instalação confiável do TgWitness, do JSON da chave, de credenciais só de leitura e de uma pasta vazia:

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Tudo é verificado antes numa pasta temporária privada: o diário inteiro, os pontos de verificação, hashes e tamanhos dos arquivos. Caminhos inseguros, segmentos conflitantes ou um diário menor que o ponto de verificação falham, e aí nada é gravado.

Se der certo, você recebe `events.jsonl`, `media/`, `checkpoints/` e `exports/`. Guarde junto a saída JSON do comando e compare com os pontos de verificação ou registros da testemunha que você mesmo guardou.
