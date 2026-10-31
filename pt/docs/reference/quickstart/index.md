# Introdução rápida

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/

Todas as formas de instalar e executar o TgWitness: pacote para Windows, Python, Docker e a demonstração sintética, com as primeiras verificações.

**Inglês** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ucraniano](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Espanhol](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Chinês simplificado](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

O TgWitness é um aplicativo independente para monitorar grupos e canais do Telegram aos quais suas contas têm acesso. Ele é executado localmente com seu próprio diretório de dados.

**É sua primeira visita?** [Explore a demonstração](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/#explore-the-interface) antes de conectar uma conta. [Escolha um guia](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) sobre proxies, testemunhas, exportações ou configuração do servidor.

## Instale e inicie

[Captura com GitHub Actions (prévia)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Escolha um método. Os downloads portáteis ficam disponíveis após a publicação de uma versão de lançamento:

| Hospedagem | Nada instalado | Fonte: Python 3.11+ | Docker: Engine/Desktop com Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | Extraia o `TgWitness-<version>-windows-amd64-portable.zip` das versões do GitHub e clique duas vezes no `TgWitness.cmd` | Clique duas vezes em `Start.cmd` | Clique duas vezes em `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Para os métodos a partir do código-fonte, [baixe e extraia a branch `main` atual](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) ou clone o repositório:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

O código-fonte atual inclui importação de contas em lote, o painel MTProxy e carregamento de histórico retomável. A prévia portátil 0.7.0 e o arquivo de código-fonte do seu lançamento são anteriores a essas adições. Veja [o changelog](https://phishdestroy.github.io/TgWitness/pt/docs/reference/changelog/) para entender o limite entre as versões.

O `Start.cmd` oferece a instalação do Python 3.12 para o seu usuário do Windows caso nenhuma versão adequada do Python seja encontrada (via winget ou pelo instalador assinado do python.org). O `start.sh` exibe o comando exato de instalação para a sua distribuição Linux ou macOS se o Python estiver ausente. A primeira execução a partir do código-fonte cria o `.venv` e instala as dependências automaticamente.

O Docker compila o aplicativo e o inicia em segundo plano; não é necessário um host Python. `scripts\Docker.cmd` e `scripts/docker-start.sh` exibem o endereço do painel e o token quando o contêiner está em bom estado. Os comandos equivalentes do Docker em todos os hosts compatíveis são:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Acesse **http://127.0.0.1:8787**. Utilize o token gerado pelo auxiliar do Docker ou pelo segundo comando do Docker, ou consulte **o arquivo data/live/panel-token.txt** para uma instalação portátil ou de código-fonte. Continue na seção **“Conectar o Telegram”** abaixo. As instalações nativas e via Docker utilizam armazenamento separado; iniciar o Docker não importa um diário nativo existente.

No que diz respeito ao servidor, [a implantação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/) abrange HTTPS automático, reinicialização, imagens publicadas, atualizações e backups.

## Explore a interface

1. Execute **o arquivo `TgWitness-Demo.cmd`** no pacote portátil, **o `scripts\Demo.cmd`** na pasta de origem do Windows ou o ``sh start.sh --demo` ` no Linux/macOS. Ao executar o arquivo de origem, o sistema cria primeiro o ``.venv` ` e instala as dependências.
2. Acesse **http://127.0.0.1:8787**.
3. A demonstração local abre automaticamente o diário de amostra. Não é necessária nenhuma cópia do token para acesso local direto.

As mensagens de demonstração são fictícias. O modo de demonstração não permite conectar uma conta real do Telegram.

## Conectar-se ao Telegram

> [!AVISO] **Não utilize nada que não possa se dar ao luxo de perder.** Recomendamos enfaticamente que não conecte contas pessoais ou valiosas e que não crie um ID de API/hash em uma conta que seja importante para você. O Telegram bane contas de forma imprevisível e, muitas vezes, permanentemente, independentemente do cliente utilizado. O bom funcionamento do teste depende do Telegram, não do TgWitness, e não oferece nenhuma garantia para o futuro.

1. Caso a demonstração nativa esteja em execução, interrompa-a e execute **o Start.cmd** ou o `sh start.sh`. Caso contrário, mantenha em execução a instalação ao vivo iniciada acima.
2. Utilize o token do painel correspondente ao seu método de instalação para abrir o painel.
3. Caso necessite de um proxy, salve-o em **Conta → Configurações → Configurações de conexão → Alterar rota de conexão**.
4. Em **“Conta**”, insira seu número de telefone e pressione **“Continuar”**, escolha **“Código QR” → “Mostrar código QR**” ou selecione arquivos e pressione **“Conectar conta**”. **O “ID da API + Hash”** é opcional: o espaço de trabalho utiliza o par salvo ou importado, ou um par válido do conjunto integrado. Para utilizar seu próprio aplicativo, cole um par `API ID:API Hash` no campo “ID da API”. Para obter uma chave de autorização completa, selecione **“Chave de autenticação”**, cole todos os 512 caracteres hexadecimais e selecione o ID DC fornecido. O ID do usuário é opcional e será marcado caso seja inserido.
5. Conclua o método de login selecionado: telefone/código/2FA, confirmação a partir de um aplicativo do Telegram com login ativo para QR ou importação de uma sessão autorizada compatível.
6. Verifique o ID da conta exibido. **Fontes** abertas: seus chats são carregados automaticamente; adicione seus grupos.
7. Em **“Escolha quais alterações preservar”**, selecione categorias de eventos ou a predefinição **“Mensagens, edições e exclusões**” e, em seguida, salve as configurações de monitoramento.
8. Selecione as configurações de anexos separadamente e, em seguida, clique em **“Iniciar observação**”.

As credenciais da API identificam seu aplicativo; elas não autorizam uma conta por si só. Grupos privados não exigem nome de usuário público, mas sua conta deve ter acesso.

Para contas existentes, veja [contas e formatos de sessão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/): o painel aceita StringSession do Telethon, SQLite do Telethon/Pyrogram, ZIP de TData de conta única e JSON de conta compatível. Selecione uma sessão e seu arquivo JSON complementar juntos e pressione **Conectar conta**. O login por QR também está disponível com as mesmas configurações opcionais de API. TDLib, sessões de bots e inventários de contas em CSV/JSON não são suportados.

Para várias contas, use **Contas → Importar contas** e selecione os arquivos de sessão compatíveis. Os arquivos JSON complementares são pareados pelo nome-base; cada conta importada recebe seu próprio espaço de trabalho. Veja [importação em massa e grupos de contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#bulk-import-and-account-groups).

Para adicionar outra conta, pressione **+** ao lado do seletor de contas ou acesse **Conta → Configurações → Configurações de conexão → Espaços de trabalho**, ou utilize **a opção Contas**. Os espaços de trabalho possuem sessões, registros, chaves, fontes e filas separadas. A troca de visualizações mantém os demais coletores em execução. A mesma conta do Telegram não pode ser atribuída a dois espaços de trabalho nesta instalação. Não há um número fixo de espaços de trabalho; eles compartilham um único processo, portanto, a capacidade depende do computador.

O token do painel ao vivo protege o acesso às suas autorizações do Telegram e ao material salvo; ele é independente das credenciais da API do Telegram. Apenas uma demonstração local iniciada explicitamente e acessada diretamente recebe acesso automático. Uma demonstração remota ou via proxy continua utilizando o `data/demo/panel-token.txt`.

## Revisão e exportação

- **Registro:** pesquise e filtre observações por fonte e tipo de evento.
- Selecione um evento para examinar seu registro original, atribuição e versões salvas.
- Os detalhes da edição mostram o conteúdo disponível antes e depois. Os detalhes da exclusão mostram o último conteúdo capturado, se houver; um agente desconhecido permanece desconhecido.
- **Formatos de exportação:** ZIP assinado, JSONL, CSV e HTML offline.
- **Exportação completa do chat** (Fontes → Exportação completa do chat): baixe todo o histórico visível de um chat como um pacote assinado com `chat.json` (estilo de exportação do Telegram) e um `chat.html` legível. Os chats privados funcionam quando a conta é membro. Trata-se de um instantâneo atual, não de uma reconstrução de mensagens excluídas ou editadas anteriormente. Verifique uma cópia com o `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Ponto de verificação:** mantenha o limite do registro assinado fora do coletor.
- **Baixe o comprovante de execução assinado:** preserve o registro do programa e da versão do coletor.
- **Prepare uma solicitação de carimbo de data e hora:** prepare uma solicitação offline para uma autoridade de carimbo de data e hora; siga as instruções do arquivo [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/) para obter e verificar uma resposta.
- **Verificar o registro:** verifique as assinaturas dos eventos e os elos da cadeia. A exportação em ZIP também verifica os arquivos de mídia.

Os navegadores compatíveis salvam exportações de grande porte diretamente em um arquivo escolhido. Outros navegadores armazenam em buffer no máximo 128 MiB. Enquanto o servidor estiver em execução, a CLI de streaming suporta downloads maiores sem armazenar toda a resposta em buffer:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Para outro espaço de trabalho, adicione `--profile ID` usando **Exportações → ID do Espaço de Trabalho**. Para um servidor remoto, adicione `--url https://your-server`. O limite padrão de transferência é de 5 GiB; o `--max-mib` altera esse valor. O conteúdo ZIP assinado possui um limite de verificação separado de 4 GiB, sem compactação, por padrão (**o “Parameters”** aumenta esse limite; verifique esses arquivos com o `verify.py --max-gib N`). Verifique o arquivo utilizando uma cópia confiável do verificador e uma impressão digital da chave/ponto de verificação mantida de forma independente.

## Verifique a instalação

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

O `--check` verifica dependências locais, suporte à assinatura, armazenamento, configuração de chaves e o endereço de escuta. Ele não instala nada nem se conecta ao Telegram. Uma porta ocupada pode significar que outra instância está em execução. Utilize um `--port` diferente ou interrompa-a primeiro.

O iniciador é instalado no `.venv`. Os comandos auxiliares `python -m tgwitness...` devem utilizar o `.venv\Scripts\python.exe` no Windows ou o `.venv/bin/python` no Linux/macOS, a menos que esse ambiente já esteja ativado.

## Sessões, proteção e operação

Um arquivo `.session` do Telethon SQLite, fechado e consistente, pode ser convertido localmente com o `python -m tgwitness.sessions account.session --out account.tgwitness-session` e, em seguida, carregado na conta. A importação direta de arquivos e o login por QR também estão disponíveis. Consulte [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) para conhecer os formatos de login, SOCKS5, HTTP CONNECT, MTProxy e chaves-mestra externas.

**A pausa na observação** interrompe a coleta. **O bloqueio** apenas interrompe o acesso pelo navegador. Fechar uma aba mantém o processo de coleta em execução. Interromper o processo interrompe a coleta; um instantâneo do histórico não pode reconstruir todas as edições ou exclusões perdidas. Veja [como funciona a coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/) em relação a políticas de eventos, filas de anexos, isolamento de contas e comportamento de reinício.

As sessões e os segredos são criptografados. O conteúdo das mensagens, as mídias e as exportações exigem um disco ou volume criptografado. As assinaturas garantem a integridade em relação a uma chave confiável; elas não comprovam a origem no Telegram nem impedem a falsificação por parte de um operador que controle o coletor e sua chave.

Leia [o arquivo OPERATIONS.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/operations/) para informações sobre backup/restauração, [o arquivo DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/) para hospedagem e [a pasta deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) para exemplos de uso do serviço. O painel instalado também inclui um guia de configuração offline em `/guide.html`.

A verificação efetiva e as limitações remanescentes estão registradas nos arquivos [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/) e [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
