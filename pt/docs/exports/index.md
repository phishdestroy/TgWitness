# Exportar e verificar

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/exports/

Compartilhe um registro assinado que outra pessoa possa verificar.

Manter uma referênciaExportar ZIP assinadoO destinatário verifica

Não tem familiaridade com assinaturas e pontos de verificação? [Altere um registro de exemplo](https://phishdestroy.github.io/TgWitness/pt/docs/concepts/#chain) e veja quais verificações o detectam.

Deseja manter uma cópia fora do controle do coletor? Acesse [a configuração do S3](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3), [o Object Lock](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3-retention) ou [a recuperação verificada](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3-restore).

## Mantenha uma referência confiável

Salve a impressão digital da chave pública do espaço de trabalho fora do coletor. Durante a coleta, mantenha pontos de verificação assinados em outro local ou utilize uma [testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/witness/). Essas referências permitem que um destinatário verifique a chave e o limite de um diário anterior.

## Baixe o arquivo ZIP assinado

Abra **o “Exports”** e crie um arquivo ZIP de evidências assinado. Ele inclui o diário da área de trabalho e um manifesto de arquivos assinado. Os filtros do painel não limitam essa exportação do diário completo: analise o material antes de compartilhá-lo.

Os downloads independentes em HTML e CSV são úteis para leitura e análise. Mantenha o arquivo ZIP assinado como o original verificável; o arquivo HTML ou CSV separado não possui assinatura independente.

## Verifique com uma cópia confiável do TgWitness

No ambiente do projeto instalado, substitua a impressão digital de exemplo e os caminhos dos arquivos:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Quando ambas as referências forem aprovadas, o resultado indicará `key_pinned: true` e `checkpoint_checked: true`. Mantenha o resultado da verificação junto com o arquivo original. O ponto de verificação retido deve estar no limite da exportação ou antes dele.

## Compreenda o resultado

- **Integridade:** o histórico registrado e os arquivos exportados correspondem às respectivas assinaturas.
- **Observação anterior:** um ponto de verificação externo permite que o senhor compare a exportação com um prefixo de registro previamente armazenado.
- **Execução:** um teste controlado de envio → edição → exclusão verifica eventos específicos em relação ao registro capturado.

Uma assinatura válida não comprova que todos os eventos do Telegram tenham sido recebidos, que a fonte tenha dito a verdade ou que o relógio do coletor estivesse correto.

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

1. Insira o destino e as credenciais. Deixe a opção **“Manter uma cópia externa”** desmarcada durante a preparação e, em seguida, selecione **“Salvar cópia externa**”.
2. Selecione **“Testar conexão**”. Isso envia um objeto de teste criptografado e verifica a resposta do armazenamento.
3. Selecione **“Baixar chave de criptografia**”. Mantenha esse arquivo separado do coletor; ele é necessário para a recuperação.
4. Marque a caixa de seleção **“Manter uma cópia externa”** e salve novamente. Selecione **“Copiar agora**” para uma execução manual ou deixe a programação em execução.

**O que não faz** A ferramenta não cria um bucket de armazenamento. Os envios programados são interrompidos quando o aplicativo é encerrado.

## Verifique a retenção e o andamento da cópia

Em **“Mais opções”**, selecione o número de dias de retenção e “`GOVERNANCE`” ou “`COMPLIANCE`” caso seu bucket ofereça suporte ao Object Lock. O TgWitness retorna o modo de retenção e o prazo de validade de um objeto enviado. O status informa se houve confirmação, se a retenção está ausente ou se ocorreu uma falha na verificação; o simples fato de o envio ter sido bem-sucedido não constitui, por si só, confirmação da retenção.

O painel informa a última passagem, a contagem de objetos, os bytes transferidos, o limite do registro copiado e quaisquer erros. Mídias locais ausentes ou alteradas são relatadas e a operação é repetida na próxima passagem. Arquivos, pontos de verificação e exportações em fila após essa mídia ainda podem ser copiados.

Os envios utilizam a rota Direct, SOCKS5 ou HTTP do espaço de trabalho. A cópia para o S3 não está disponível via MTProxy; o aplicativo não recorre a uma conexão direta.

**O que não faz** O fato de o upload ter sido aceito não obriga o provedor a aplicar o Object Lock.

## Guarde a chave de recuperação em local separado

O arquivo JSON baixado contém a chave de descriptografia, as configurações de destino, o prefixo do objeto do espaço de trabalho e a impressão digital da chave de assinatura. Ele não contém as credenciais de acesso ao S3: a recuperação requer credenciais separadas com acesso de leitura ao bucket.

Caso altere o endpoint, o bucket ou o prefixo da pasta, baixe o arquivo de chave novamente para que as configurações de destino correspondam. O aplicativo inicia uma nova cópia do registro, dos arquivos e dos pontos de verificação mantidos localmente no novo destino. As exportações de bate-papos concluídas que já foram removidas da fila de upload local permanecem em seu destino anterior.

**O que não faz** A ferramenta não descriptografa a cópia sem a chave exportada. As credenciais de acesso ao armazenamento não podem substituir essa chave.

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

**O que não faz** Ela não reconstrói observações que nunca chegaram ao registro nem substitui um ponto de verificação ou testemunha mantidos de forma independente.
