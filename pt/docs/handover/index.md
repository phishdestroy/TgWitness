# Prepare uma cópia para compartilhamento

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/handover/

Compartilhe as observações relevantes, mantendo o espaço de trabalho original intacto.

Uma transferência é um extrato separado e assinado. Escolha os chats e as pessoas, reduza identidades ou texto e decida quais arquivos e notas da equipe devem constar na cópia do destinatário. Seu manifesto registra a seleção e o número de registros inalterados, minimizados e omitidos.

## Prepare o extrato do destinatário

1. Abra **Exportações → Extrato de transferência**. Descreva sua finalidade, escolha os chats e o período UTC opcional e, em seguida, selecione **“Carregar participantes dos chats escolhidos”** se precisar dos nomes dos envolvidos.
2. Escolha como lidar com os demais participantes: use pseudônimos, omita suas mensagens ou exiba-as conforme registradas. Defina o texto das mensagens e os anexos de forma independente; opcionalmente, oculte números de telefone e endereços de e-mail.
3. Decida se deseja incluir marcadores e seções do Case Board ou cartões com comentários. Os pseudônimos dos investigadores podem substituir os nomes das equipes neste texto.
4. Selecione **“Baixar extrato de transferência**”. Abra localmente o relatório gerado e os registros selecionados, verifique o arquivo e inspecione a cópia antes de enviá-la.

### Um original, uma cópia para compartilhamento deliberado

Exemplo sintético · apenas para ilustração de identidade

1. **Selecione.** Inclua o chat do caso e identifique a pessoa a quem o trecho se refere.
2. **Minimizar.** Escolha como outro participante aparece na cópia compartilhada.
3. **Verifique.** Abra o relatório e os registros do arquivo gerado antes de enviá-lo.
4. **Compartilhe.** Entregue a versão revisada e comunique sua assinatura digital de confiança separadamente.

#### Observação original

Nora · usuário 71002

“Recebi o link revisado.”

O diário de origem mantém essa observação salva.

#### Cópia para o destinatário

Mostrar conforme registrado: Nora · usuário 71002 · “Recebi o link revisado.”

Pseudônimo: P01 · “Recebi o link revisado.”

Omitir: a mensagem deste participante foi deixada de fora do texto.

#### Inspecione os arquivos reais

Leia os arquivos report.html e records.jsonl.

Verifique identidades, textos, anexos e comentários opcionais da equipe.

#### Trecho assinado

Seleção + hashes de arquivos + manifesto assinado

Um pacote separado vinculado ao limite do diário de origem

## Use os controles em conjunto

| Controle | Impacto no texto |
| --- | --- |
| Pessoas | Mantenha os sujeitos selecionados identificáveis; pseudonimize ou omita outros participantes, conforme for escolhido. |
| Texto | Inclua todo o texto, apenas o texto das pessoas selecionadas e da conta observadora, ou omita o texto da mensagem e seus campos de detalhes que contenham texto. |
| Arquivos | Escolha os arquivos das pessoas selecionadas e da conta em observação, todos os arquivos das mensagens exibidas ou nenhum arquivo. |
| Case Board | Não inclua materiais do quadro, marcadores e fatias, nem cartões com discussões da equipe. |

Revise textos em formato livre e o conteúdo dos arquivos, bem como as identidades: um pseudônimo não remove automaticamente todos os nomes escritos em uma mensagem ou anexo. Se um arquivo preservado selecionado estiver indisponível, restaure-o ou omita explicitamente os anexos antes de gerar o extrato.

## Mantenha o texto de forma que possa ser verificado de maneira independente

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Mantenha o arquivo original de evidências assinadas e os pontos de verificação separadamente. A transferência registra sua própria projeção, de modo que o destinatário possa verificar a cópia entregue sem receber todo o espaço de trabalho. [O Report Studio](https://phishdestroy.github.io/TgWitness/pt/docs/reports/) fornece seu layout de leitura; [a verificação de exportação](https://phishdestroy.github.io/TgWitness/pt/docs/exports/) explica as referências confiáveis.
