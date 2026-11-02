# Primeira configuração e ajustes

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/settings/

O assistente de configuração, as metas, os níveis de interface, as rotas de conexão e as configurações compartilhadas por um grupo de contas.

[Contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/) · [Conexão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) · [Acesso](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/)

Um novo espaço de trabalho é aberto `/first-run`: idioma e fuso horário, nível de interface, objetivo, conexão, Telegram e chats. Cada resposta é salva no servidor assim que sofre alteração, de modo que uma atualização da página continua na mesma etapa. A última tela lista as respostas e permite que você retorne a qualquer uma delas.

O idioma, o fuso horário da IANA, o tema e o nível são armazenados por operador e por espaço de trabalho. Os padrões são o idioma do navegador, o fuso horário do dispositivo, o tema do sistema e a interface simples. A alteração do idioma mantém a sessão do painel. Os horários no diário assinado nunca mudam.

`/settings` edita os mesmos registros que o assistente. A pesquisa abrange os campos principais, parâmetros e os formulários estendidos; um campo oculto pode ser aberto sem alterar o nível. Os níveis alteram apenas o que é exibido: o servidor verifica as permissões por conta própria. As configurações da coleção e a primeira conexão pertencem ao administrador do espaço de trabalho.

| Nível | Campos | Barra lateral |
| --- | --- | --- |
| Simples | Apenas o essencial | Página inicial, Conversas, Alterações, Arquivos, Configurações |
| Padrão | Configurações comuns com explicações | Adiciona Case Board, Contas e Acesso |
| Especialista | Todos os campos, limites e detalhes técnicos | Adiciona Fontes, Extras, Pergunte ao arquivo, Parâmetros, Conta, Log do sistema e Integrações |

[O guia do painel](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/) descreve cada seção.

## Objetivos

| Objetivo | Coleção | Arquivos | Serviços externos | Endereço do servidor |
| --- | --- | --- | --- | --- |
| Cópia de arquivo | Desativado; **“Iniciar”** executa uma exportação | Fotos de até 20 MB | Desativado | Automático |
| Acompanhar conversas | Contínuo | Fotos e vídeos de até 60 segundos / 20 MB | Registros de data e hora e notificações de problemas | Automático |
| Evidências | Contínuo | Todos os arquivos de até 1 GB | Carimbos de data/hora, drand, notificações | Não, ocultar |

Recomenda-se a cópia externa, o bot testemunha e a verificação de código como evidências. Os endereços de armazenamento e notificação precisam primeiro de um destino. Um recurso que se comunica com um serviço externo solicita permissão para enviar solicitações fora do Telegram; desativá-lo oferece a opção de desativar, junto com ele, os carimbos de data e hora, as notificações e a cópia externa.

Alterar a meta mostra a diferença em primeiro lugar, e as alterações manuais podem ser mantidas. Um campo que difere da meta é marcado **como “Alterado por você”** e pode ser restaurado. A revisão das configurações impede que uma diferença revisada seja aplicada sobre uma alteração feita em outra aba.

## Conexão

**O Automatic** tenta servidores públicos MTProxy, depois o WARP e, por fim, uma conexão direta, sendo que esta última só é utilizada quando o endereço do servidor pode ser exibido. O Automatic e o WARP podem instalar componentes com verificação de hash e registrar o servidor no Cloudflare. O WARP utiliza o gerenciador wgcf/wireproxy existente e uma porta SOCKS5 local; a tabela de roteamento do sistema não é alterada. Quando serviços externos são necessários, o Automatic prefere o WARP ao MTProxy.

Seu próprio proxy aceita `tg://proxy`, `socks5://`, `http://` e `https://`. O certificado de um proxy HTTPS é verificado antes que as credenciais sejam enviadas a ele.

Uma verificação de conexão é válida por cinco minutos e está vinculada à rota, à política e às respostas do assistente; alterar qualquer um desses itens exige uma nova verificação. A **opção “Continuar sem verificar”** está disponível e não substitui o login no Telegram. A rota escolhida é verificada novamente em segundo plano, e o recurso “Automático” executa sua cadeia novamente após uma perda de conexão. Quando nenhum proxy público responde, a contagem fica em vermelho com as ações WARP e reverificação.

## Grupos de contas

As contas de um grupo compartilham suas configurações. Abra **Contas → Grupos e configurações compartilhadas → Configurações compartilhadas** ou **Configurações do grupo** na página de configurações de uma conta.

O grupo compartilha a meta, arquivos salvos, registros de data e hora, drand, notificações de problemas, cópia externa, solicitações fora do Telegram, modo IP, o que registrar, a programação de reverificação, regras de notificação, configurações de relatório, parâmetros e a rota de conexão. Os destinos de notificação, as credenciais de proxy e o login permanecem por conta, assim como o início e a pausa da coleta.

- Todos os membros seguem o grupo. Em “Configurações”, marque um valor 🔗 **do grupo** ou ✏️ **um valor próprio**; a opção **“Retornar ao valor do grupo”** o restabelece.
- Uma alteração lista as contas afetadas (**aplica-se a 2 das 3 contas**) e solicita confirmação por conta antes de substituir um valor próprio. As contas desmarcadas mantêm seus valores.
- Um parâmetro que o grupo não compartilha permanece como **“Não compartilhado”: cada conta mantém seu próprio valor** até que você pressione **“Compartilhar este valor**”.
- **Ao copiar as configurações de uma conta,** os valores da conta escolhida passam a ser os do grupo.
- Quando uma conta é movida para um grupo, é perguntado: **“Adotar os valores do grupo?**”. Caso contrário, ela mantém seus próprios valores, marcados com ✏️. As contas adicionadas posteriormente começam com os valores do grupo.
- Uma conta de observação mantém seu modo de IP até ser pausada.

Cada alteração é registrada no diário assinado do espaço de trabalho principal e de cada membro ao qual ela chega. A exclusão de um grupo mantém suas contas e seus valores atuais.

A página do grupo `/groups/<id>` mostra os membros, o que precisa de atenção e os chats que várias contas visualizam. Veja [grupos de contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#bulk-import-and-account-groups).

## Espaços de trabalho existentes

Um espaço de trabalho com uma sessão ou uma configuração concluída anteriormente não exibe o assistente. Seus valores não são substituídos por uma meta quando a página é carregada. Ocultar um campo não desativa o recurso nem exclui seu valor.

A estimativa de tamanho e tempo considera até três conversas selecionadas e até 20 mensagens de cada uma. Trata-se de uma estimativa: ela não prevê os limites do Telegram, a velocidade de um determinado servidor nem os arquivos presentes em cada conversa.

```
python tools/test_settings_hub.py
python tools/test_group_settings.py
python tools/check_group_settings_browser.py
python tools/check_first_run.py
```
