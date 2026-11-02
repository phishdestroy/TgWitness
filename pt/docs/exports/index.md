# Exportar e verificar

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/exports/

Forneça aos destinatários arquivos que possam ser comparados com o espaço de trabalho de coleta e seu histórico salvo.

Manter uma referênciaExportar ZIP assinadoO destinatário verifica

Não tem familiaridade com assinaturas e pontos de verificação? [Altere um registro de exemplo](https://phishdestroy.github.io/TgWitness/pt/docs/concepts/#chain) e veja quais verificações o detectam.

Deseja manter uma cópia fora do controle do coletor? Acesse [a configuração do S3](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3), [o Object Lock](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3-retention) ou [a recuperação verificada](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3-restore).

## Mantenha uma referência confiável

Salve a impressão digital da chave pública do espaço de trabalho fora do coletor. Durante a coleta, mantenha pontos de verificação assinados em outro local ou utilize uma [testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/witness/). Essas referências permitem que um destinatário verifique a chave e o limite de um diário anterior.

## Baixe o arquivo ZIP assinado

Abra **o “Exports”** e crie um arquivo ZIP de evidências assinado. Ele inclui o diário completo da área de trabalho e um manifesto de arquivos assinado. Use [o “Report Studio”](https://phishdestroy.github.io/TgWitness/pt/docs/reports/) para elaborar um relatório legível ou um [extrato de transferência](https://phishdestroy.github.io/TgWitness/pt/docs/handover/) para entregar apenas dados selecionados e minimizados.

Os relatórios em HTML, PDF e JSON possuem seus próprios selos assinados e podem ser verificados separadamente. O CSV é uma cópia prática para análise; use o CSV exato contido no ZIP verificado para verificar sua integridade. Mantenha o ZIP assinado quando o destinatário também precisar dos registros de origem e dos anexos.

## Verifique com uma cópia confiável do TgWitness

No ambiente do projeto instalado, substitua a impressão digital de exemplo e os caminhos dos arquivos:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Quando ambas as referências forem aprovadas, o resultado indicará `key_pinned: true` e `checkpoint_checked: true`. Mantenha o resultado da verificação junto com o arquivo original. O ponto de verificação retido deve estar no limite da exportação ou antes dele.

## Utilize o resultado da verificação

- **Verifique os arquivos entregues:** o manifesto vincula seus hashes, e as assinaturas dos registros vinculam o diário salvo. Qualquer arquivo alterado ou cadeia de registros quebrada será detectada.
- **Verifique a identidade do espaço de trabalho:** a impressão digital mantida de forma independente identifica a chave de assinatura esperada.
- **Compare um limite anterior:** um ponto de verificação retido compara a exportação com um prefixo de diário salvo antes da transferência.
- **Analise a cobertura da coleta:** lacunas, resultados da aquisição e um teste controlado de envio → edição → exclusão descrevem os eventos capturados por essa configuração.

Mantenha esses resultados na cópia do destinatário. Verifique [o que a verificação estabelece](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) quanto ao escopo das verificações e à avaliação separada das alegações das fontes e da cobertura da coleta.

## Configure a cópia externa no S3

Em sua área de trabalho ativa, abra **Exportações → Cópia externa**. Esse recurso opcional funciona com o AWS S3 e outros serviços compatíveis com S3. Ele copia segmentos do registro, fotos e arquivos preservados, pontos de verificação com suas respostas de carimbo de data/hora e exportações concluídas de bate-papos. Cada objeto é criptografado no coletor com o algoritmo `AES-256-GCM` antes do upload.

A demonstração online mostra os mesmos controles com os envios desativados. Insira as credenciais de armazenamento apenas em seu próprio ambiente de trabalho em execução.

[![Painel completo de cópia externa: endpoint, região, bucket, chaves de acesso, programação, controles de Object Lock e chave de recuperação](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

O painel completo com opções avançadas está expandido. Nenhuma credencial de armazenamento é exibida.

| Campo | O que inserir |
| --- | --- |
| Endpoint | A URL do serviço de armazenamento, sem caminho de bucket nem credenciais. Exemplo fictício: `https://s3.example.invalid`. |
| Região | A região exigida pelo seu provedor. O padrão do aplicativo é `us-east-1`. |
| Bucket | Um bucket existente ao qual o senhor pode acessar. Exemplo fictício: `example-case-backup`. |
| Pasta no bucket | O prefixo do objeto; padrão `tgwitness`. O aplicativo acrescenta um prefixo derivado da impressão digital da chave de assinatura deste espaço de trabalho. |
| ID da chave de acesso / Chave secreta de acesso | Insira ambas as credenciais de armazenamento ao mesmo tempo. Elas serão salvas no cofre da área de trabalho. Deixe ambos os campos em branco em salvamentos posteriores para manter o par salvo. |
| Endereços no formato de caminho | Utilize `endpoint/bucket` quando ativado ou `bucket.endpoint` quando desativado, de acordo com o provedor. |
| Intervalo de cópia | De 1 a 1.440 minutos; padrão de 5 minutos. O aplicativo deve estar em execução para que as cópias programadas sejam realizadas. |
| Retenção do Object Lock | Período de retenção e modo para um bucket compatível com o Object Lock. O valor “zero dias” mantém a retenção padrão do bucket em vigor. |

1. Crie o bucket com seu provedor e, em seguida, insira o destino e as credenciais. Deixe a opção **“Manter uma cópia externa”** desmarcada durante a preparação e, depois, selecione **“Salvar cópia externa**”.
2. Selecione **“Testar conexão**”. Isso envia um objeto de teste criptografado e verifica a resposta do armazenamento.
3. Selecione **“Baixar chave de criptografia**”. Mantenha esse arquivo separado do coletor; ele é necessário para a recuperação.
4. Marque a caixa de seleção **“Manter uma cópia externa”** e salve novamente. Selecione **“Copiar agora**” para uma execução manual ou deixe a programação em execução.

## Verifique a retenção e o andamento da cópia

Em **“Mais opções”**, escolha os dias de retenção e “`GOVERNANCE`” ou “`COMPLIANCE`” quando seu bucket for compatível com o Object Lock. O TgWitness recupera o modo de retenção e o prazo de um objeto enviado. Verifique o resultado de retenção separado: confirmado, retenção ausente ou falha na verificação.

O painel informa a última passagem, a contagem de objetos, os bytes transferidos, o limite do registro copiado e quaisquer erros. Mídias locais ausentes ou alteradas são relatadas e a operação é repetida na próxima passagem. Arquivos, pontos de verificação e exportações em fila após essa mídia ainda podem ser copiados.

Os envios utilizam as rotas Direct, SOCKS5 ou HTTP do espaço de trabalho. Escolha uma dessas rotas para a cópia para o S3; uma rota exclusivamente MTProxy deixa a cópia pendente com um erro.

## Guarde a chave de recuperação em local separado

O arquivo JSON baixado contém a chave de descriptografia, as configurações de destino, o prefixo do objeto do espaço de trabalho e a impressão digital da chave de assinatura. A recuperação requer tanto esse arquivo de chave quanto credenciais de armazenamento separadas com acesso de leitura ao bucket. Inclua-as em seu plano de recuperação.

Caso altere o endpoint, o bucket ou o prefixo da pasta, baixe o arquivo de chave novamente para que as configurações de destino correspondam. O aplicativo inicia uma nova cópia do registro, dos arquivos e dos pontos de verificação mantidos localmente no novo destino. As exportações de bate-papos concluídas que já foram removidas da fila de upload local permanecem em seu destino anterior.

## Restaurar e verificar em outro computador

Utilize uma instalação confiável do TgWitness, o arquivo JSON de chave baixado, credenciais de armazenamento com acesso de leitura e um diretório de saída vazio. Substitua os placeholders fictícios de credenciais abaixo.

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

Os arquivos baixados e os objetos descriptografados permanecem em um armazenamento temporário privado enquanto todo o registro, os pontos de verificação retidos e os hashes e tamanhos das mídias preservadas são verificados. Caminhos inseguros, segmentos conflitantes do registro e um registro mais curto que seu ponto de verificação são rejeitados. Uma verificação com falha não publica nenhum arquivo restaurado.

A recuperação bem-sucedida gera `events.jsonl`, `media/`, `checkpoints/` e `exports/` para o material disponível na cópia. Guarde o resultado JSON do comando junto com o material recuperado.

Compare o material recuperado com seus pontos de verificação ou registros de testemunho mantidos de forma independente e, em seguida, analise a cobertura da coleta registrada para o período de que você precisa.
