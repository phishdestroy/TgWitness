# Elabore um relatório

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reports/

Forneça ao leitor um caminho claro desde a questão do caso até os registros salvos.

O “Report Studio” combina seleção de dados, históricos de alterações legíveis, gráficos e suas conclusões por escrito. Oito modelos integrados se aplicam às saídas compatíveis em HTML e PDF nativo. Relatórios em HTML, PDF e JSON possuem seus próprios selos assinados; o manifesto ZIP também agrupa os arquivos no pacote. Os arquivos em HTML e PDF são selados após a conclusão de seu layout final.

## Crie um relatório em três etapas

1. Abra **Exportações → Configurar e visualizar → Dados**. Use toda a área de trabalho ou selecione bate-papos, autores, incluindo datas de observação em UTC e tipos de registros. As datas indicam quando o TgWitness observou o registro.
2. Em **“Design e conteúdo”**, escolha uma predefinição de design e conteúdo. Selecione gráficos de atividades, rótulos dos participantes, a transcrição, as alterações salvas e o material opcional do Case Board. Adicione os detalhes do seu caso e as notas de análise.
3. Abra **a “Pré-visualização”** para revisar contagens, atividades, participantes, registros amostrados e intervalos de ID ausentes. Salve as configurações e, em seguida, baixe o formato de que você precisa.

### Organize o mesmo material salvo de forma acessível para o leitor

Exemplo sintético · layout esquemático, não é um relatório gerado

1. **Selecionar.** Escolha dois chats e o período de observação para o caso.
2. **Redija o texto.** Escolha um layout e as seções que respondam à pergunta.
3. **Pré-visualização.** Revise as contagens selecionadas e o texto “antes e depois” salvo.
4. **Verifique.** Gere o arquivo final e compare sua assinatura com a impressão digital do espaço de trabalho confiável.

#### Observações selecionadas

2 conversas · 1 dia de observação

Mensagens, edições e avisos de exclusão

#### Estrutura do relatório

##### Destino de pagamento alterado

Questão do caso → escopo → conclusões → referências dos registros

**Contexto da mensagem**

Observação nº 142: “Use o novo link de pagamento.”

**Alterações salvas**

Antes: old.example.invalid → Depois: new.example.invalid

#### Revisar a seleção

18 observações · 2 edições salvas

Os horários de envio, edição e observação possuem rótulos distintos.

#### Entrega final

PDF assinado + JSON assinado, ou um ZIP assinado com seu relatório legível

O destinatário verifica o arquivo e a assinatura digital confiável.

## Escolha um estilo de leitura

**As seções “Clássico”, “Editorial”, “Briefing”, “Análise”, “Técnico”, “Visão Geral”, “Série de Leituras” e “Livro-razão e margem”** apresentam os mesmos registros subjacentes em diferentes composições. A alteração do design mantém a seleção de dados e as notas escritas. O idioma do relatório pode ser escolhido entre os 25 idiomas suportados.

A série de leitura agrupa o caso, o escopo, as conclusões e as alterações em torno de uma barra lateral. O Ledger & Margin utiliza capítulos numerados e uma margem ampla. Ambos também oferecem suporte a visões gerais em HTML das contas e ao compartilhamento de cópias. PDFs nativos são gerados com fontes incluídas; o computador do usuário não precisa de navegador nem da instalação do Node para a criação de PDFs. PDFs em chinês, japonês e coreano exigem, além disso, uma fonte adequada no servidor, como a Noto Sans CJK, instalada em todo o sistema ou colocada no diretório `TGWITNESS_FONT_DIR`. Na ausência dela, o arquivo ZIP mantém os relatórios em HTML e JSON.

## Interprete uma alteração dentro de seu contexto

As edições salvas mostram o antes e o depois. Um aviso de exclusão pode ser acompanhado pela última versão capturada. Respostas, citações, encaminhamentos, reações, botões e metadados de anexos mantêm suas referências disponíveis. Os hashes SHA-256 dos arquivos e dos registros do diário são identificados separadamente.

A visualização do design mostra componentes de capa, análise e gráficos utilizando registros correspondentes entre os primeiros 50.000 registros de origem. A visualização separada dos dados examina o instantâneo completo e estável do diário para obter contagens exatas de seleção, com os limites da amostra exibidos e identificados. Gere um PDF para verificar a paginação final. A exportação completa da conta inclui uma visão geral em HTML; seus PDFs individuais de bate-papo utilizam o design escolhido.

## Escolha cuidadosamente a versão destinada ao destinatário

Os filtros de relatório moldam o relatório legível. O arquivo ZIP completo com as evidências mantém o diário original e os anexos. Use uma [transferência minimizada](https://phishdestroy.github.io/TgWitness/pt/docs/handover/) quando o destinatário precisar receber apenas dados selecionados. Veja [o conteúdo do relatório e a verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/) ou [verifique a exportação concluída](https://phishdestroy.github.io/TgWitness/pt/docs/exports/).
