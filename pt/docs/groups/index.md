# Gerenciar um grupo de contas

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/groups/

Gerencie várias contas de coleta simultaneamente, mantendo distintos os registros e a identidade de assinatura de cada conta.

Um grupo de contas reúne o status da conexão, controles de observação, configurações compartilhadas e exportações em uma única visualização de trabalho. Isso é útil quando várias contas abrangem a mesma investigação ou precisam de uma configuração operacional consistente.

## Abrir a visão geral do grupo

Em **“Contas”**, abra o grupo. Cada conta exibe seu status de observação, rota de conexão, a latência mais recente da rota medida quando uma verificação atual foi bem-sucedida e a última mensagem salva. Os links **“Precisa de atenção”** indicam as contas que requerem ação; **“Corrigir”** abre o espaço de trabalho e o controle relevantes.

**As opções “Iniciar tudo”** e **“Pausar tudo”** são aplicadas às contas elegíveis após a confirmação. **As configurações de grupo** compartilham as configurações selecionadas; as contas com valores próprios os mantêm até que você opte por substituí-los.

### Revisar uma alteração de rota em um grupo

Exemplo sintético · verificações ilustrativas e resultados

1. **Selecionar.** Escolha o grupo e verifique quais contas serão alteradas.
2. **Prepare.** Mantenha a rota específica de uma conta quando for necessário mantê-la separada.
3. **Verifique.** Teste a conexão proposta e analise os resultados medidos.
4. **Aplique as alterações.** Verifique novamente antes de salvar e analise o resultado para cada conta.

#### Equipe do caso

Coletor de canais · Coletor de grupos · Conta de referência

3 espaços de trabalho separados

#### Seleção revisada

Duas contas seguem a abordagem proposta.

A conta de referência mantém seu próprio caminho.

#### Verificações de preparação

Coletor de canais: tempo de transmissão do Telegram: 84 ms

Coletor de grupo: tempo de transmissão do Telegram: 91 ms

Esses números são valores fictícios para fins de exemplo.

#### Resultados da aplicação

Coletor de canais: roteamento salvo, observação retomada.

Coletor de grupo: nova verificação falhou, configurações anteriores restauradas.

Conta de referência: rota própria mantida.

## Altere o fluxo incluindo uma etapa de revisão

1. Selecione **“Alterar a rota do grupo**” e, em seguida, escolha o tipo de conexão e as configurações.
2. Selecione **a opção “Revisar**”. Revise as contas listadas e suas substituições de rota individuais.
3. Selecione **“Preparar e verificar**”. A verificação utiliza um transporte novo do Telegram; as rotas HTTP compatíveis também relatam sua verificação de saída HTTPS.
4. Selecione **“Aplicar conexão marcada”** e verifique o resultado de cada conta. A observação em andamento é retomada onde o aplicativo for bem-sucedido; contas inativas permanecem inativas.

A latência descreve o tempo medido para o estabelecimento da conexão do Telegram. Uma verificação do IP de saída descreve essa rota no momento da verificação registrada. A autorização da conta e o estado da observação possuem seus próprios indicadores; uma alteração no grupo pode resultar em desfechos diferentes para cada conta.

## Use acesso sobreposto

**A opção “Bate-papos em várias contas”** exibe as fontes compartilhadas e a cobertura de observação disponível na área de trabalho. Canais e supergrupos elegíveis podem usar **a opção “Exportar com … contas”** para dividir a aquisição do histórico de um bate-papo. Bate-papos privados e grupos comuns permanecem na conta inicial, pois os números das mensagens pertencem ao histórico dessa conta.

## Exportar o grupo como um pacote

**O “Export Group”** cria um arquivo ZIP contendo a exportação assinada de cada conta e uma lista assinada desses arquivos. As identidades e impressões digitais originais do espaço de trabalho permanecem disponíveis para verificação. Elabore uma narrativa entre contas utilizando essas referências; uma única linha do tempo combinada ainda é montada separadamente.

Continue com [o design do relatório](https://phishdestroy.github.io/TgWitness/pt/docs/reports/), [um Case Board dentro de um espaço de trabalho](https://phishdestroy.github.io/TgWitness/pt/docs/case-board/) ou [a verificação de exportação](https://phishdestroy.github.io/TgWitness/pt/docs/exports/).
