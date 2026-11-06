# Telegram · Prepare uma cópia para compartilhamento

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/handover/

Compartilhe só o necessário; o original fica intacto.

Uma entrega é um extrato assinado à parte: escolha chats e pessoas, oculte identidades ou texto e decida quais arquivos e notas da equipe entram. O manifesto registra o que foi mantido, reduzido e deixado de fora.

## Prepare o extrato do destinatário

1. **Exportações → Extrato de entrega**: escreva o propósito, escolha chats e um período e use **Carregar pessoas dos chats escolhidos** se precisar de pessoas nomeadas.
2. Os demais: pseudônimos, fora ou como registrado. Texto e arquivos são chaves separadas; telefones e e-mails podem ser mascarados.
3. Case Board: nada, favoritos e recortes, ou cartões com comentários. Os nomes da equipe podem virar apelidos.
4. **Baixar extrato de entrega**, abra, verifique e revise antes de enviar.

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
| Pessoas | As pessoas selecionadas continuam nomeadas; as demais recebem pseudônimos ou ficam de fora. |
| Texto | Todo o texto, só o das pessoas selecionadas e da sua conta, ou nenhum. |
| Arquivos | Arquivos das pessoas selecionadas e da sua conta, todos os arquivos mostrados ou nenhum. |
| Painel de Casos | Nada, favoritos e recortes, ou cartões com discussão. |

Leia também o texto e os arquivos: um pseudônimo não remove nomes escritos dentro de uma mensagem ou anexo. Se faltar um arquivo selecionado, restaure-o ou deixe os anexos de fora.

## Mantenha o texto de forma que possa ser verificado de maneira independente

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Guarde você mesmo o arquivo original e os pontos de verificação. O destinatário pode verificar a cópia dele sem receber o espaço inteiro. Design: [Report studio](https://phishdestroy.github.io/TgWitness/pt/docs/reports/). Referências confiáveis: [verificação da exportação](https://phishdestroy.github.io/TgWitness/pt/docs/exports/).
