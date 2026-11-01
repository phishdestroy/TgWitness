# OCR e transcrição locais

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/media-analysis/

Reconheça imagens e áudios capturados com um worker local; mantenha o texto derivado vinculado ao seu arquivo de origem.

[Guia de fluxo de trabalho](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Abra um registro do diário `media.saved`, escolha **“Reconhecer anexo**” e, em seguida, selecione “OCR” ou “transcrição” na seção **“Solicitar ao arquivo**”. O processamento é manual e local. Não há modo de mídia na nuvem nem upload automático. Os bytes originais do anexo e o `media_sha256` permanecem inalterados; o texto reconhecido é explicitamente marcado como reconhecimento automático e armazenado separadamente com o hash de origem, a versão do mecanismo/modelo, o idioma, os parâmetros e o tempo de conclusão. As transcrições mantêm os carimbos de data e hora retornados.

Pesquise esses resultados usando a **opção “Pesquisar texto reconhecido”** e o filtro OCR/transcrição. Trata-se de uma pesquisa separada de dados derivados; ela não converte automaticamente o reconhecimento automático em texto original do Telegram nem o adiciona a eventos assinados.

## Configure o worker opcional

A versão 1 requer um servidor Linux com um daemon Docker local. Instalações no Windows podem executar o TgWitness dentro de um ambiente de VM Linux/WSL com seu próprio daemon local. O painel nunca decodifica por conta própria um anexo não confiável.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Defina essas variáveis no ambiente de serviço do TgWitness e reinicie-o. O soquete do daemon é, por padrão, `/var/run/docker.sock`; implantações sem privilégios de root podem definir `TGWITNESS_DOCKER_SOCKET`. O worker usa explicitamente esse soquete Unix em vez de um contexto remoto do Docker. Não exponha uma API do Docker aos usuários do painel nem monte seu soquete dentro do contêiner de reconhecimento.

Para transcrição, instale separadamente um modelo do Whisper compatível com o CTranslate2 e, em seguida, defina `TGWITNESS_WHISPER_MODEL_DIR` como seu diretório. O worker o carrega com `local_files_only=True`; o modelo selecionado e a entrada são montados como somente leitura. Consulte a [documentação do mecanismo sobre carregamento de modelos](https://github.com/SYSTRAN/faster-whisper). A imagem de OCR fornecida inclui dados de treinamento em inglês e russo. Incorpore outro idioma à sua imagem quando necessário; os códigos de idioma seguem [a CLI do Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Nenhum modelo é buscado durante o processamento. A compilação/download da configuração pode utilizar a rede; cada contêiner de reconhecimento propriamente dito tem a conexão de rede desativada. Instale a imagem antes de ativá-la; o ambiente de execução utiliza o `--pull=never`.

## Limites e recuperação

O contêiner é executado como um usuário sem privilégios, com um root somente leitura, capacidades reduzidas, `no-new-privileges` , um CPU, 2 GiB de memória, um limite de PID e um sistema de arquivos temporário restrito. Apenas uma cópia verificada do arquivo selecionado e um diretório de modelos opcional são montados. O banco de dados, o cofre e a sessão do coletor não são montados. Os [sinalizadores do tempo de execução do Docker](https://docs.docker.com/reference/cli/docker/container/run/) impõem esses limites; isso permanece como um limite do contêiner, não um enclave de hardware.

Os arquivos são limitados a 50 MiB, as imagens a 20 milhões de pixels, os áudios a 30 minutos com duração conhecida e o processamento a cinco minutos. Apenas um trabalhador é executado por vez, com no máximo 20 tarefas na fila/em execução e 100 tarefas retidas por espaço de trabalho. O comando “Cancelar” interrompe o contêiner; “Repetir” cria uma nova tarefa vinculada à tentativa anterior. Tarefas interrompidas são marcadas após a reinicialização. O processamento pode falhar quando um modelo não se encaixa nos limites configurados; ele não é executado silenciosamente sem isolamento.
