# Telegram · Gerenciar um grupo de contas

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/groups/

Use várias contas juntas, cada uma ainda com seus registros e sua chave.

Um grupo reúne em uma tela o status de conexão, iniciar/pausar, configurações compartilhadas e exportações. Útil quando várias contas trabalham no mesmo caso.

## Abrir a visão geral do grupo

Abra o grupo em **Contas**. Cada conta mostra estado, rota, latência e última mensagem salva. **Precisa de atenção** lista as que estão com problema e **Corrigir** leva direto até lá.

**Iniciar todas** / **Pausar todas** perguntam antes de agir. As **Configurações do grupo** são compartilhadas, mas os valores próprios de uma conta ficam até você substituí-los.

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

1. **Mudar a rota do grupo**, escolha o tipo e as configurações.
2. **Revisar seleção**: quais contas mudam e quais têm rota própria.
3. **Preparar e verificar** testa uma conexão nova com o Telegram e, quando dá, o IP de saída.
4. **Aplicar conexão verificada** e veja cada resultado. Contas rodando continuam; as paradas seguem paradas.

Latência é o tempo para estabelecer a conexão com o Telegram; o IP de saída é o que a rota mostrou na verificação. Os resultados podem variar por conta.

## Use acesso sobreposto

**Chats que várias contas veem** lista as fontes compartilhadas e sua cobertura. Canais e supergrupos podem ser exportados por várias contas ao mesmo tempo com **Exportar com … contas**. Chats privados e grupos básicos não: lá os números de mensagem são por conta.

## Exportar o grupo como um pacote

**Exportar grupo** gera um ZIP com a exportação assinada de cada conta e uma lista assinada delas. Cada uma mantém sua impressão digital para verificação. A linha do tempo unificada você ainda monta.

Próximo: [relatórios](https://phishdestroy.github.io/TgWitness/pt/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/pt/docs/case-board/), [verificar exportações](https://phishdestroy.github.io/TgWitness/pt/docs/exports/).
