# Meu Portal de Notícias

Portal pessoal com manchetes RSS de **the news** e **Estadão Analisa com Carlos Andreazza**, além de links diretos para Boris Casoy, Felipe Moura Brasil e Malu Gaspar. Inclui aba **Futebol** com ESPN Brasil, sportv, Palmeiras e Seleção Brasileira.

## Publicação no GitHub Pages

1. Crie um repositório **público** no GitHub, por exemplo `meu-portal`.
2. Envie **todos os arquivos e pastas deste projeto** para a raiz do repositório (inclusive `.github/workflows/atualizar.yml`). Se enviar pelo navegador, preserve a pasta `.github/workflows`.
3. Em **Settings → Pages**, selecione **Deploy from a branch**, branch **main**, pasta **/(root)**, e salve.
4. Em **Actions**, execute manualmente **Atualizar notícias** (Run workflow) para gerar `noticias.json`. A atualização programada ocorre aproximadamente a cada duas horas; o GitHub pode atrasar ou suspender tarefas agendadas em repositórios inativos.
5. Abra `https://SEU-USUARIO.github.io/meu-portal/` (substitua pelo nome real do repositório).
6. No Google Sites, use **Inserir → Incorporar → URL** e cole o endereço do GitHub Pages. Ajuste a altura da incorporação.

## Observações

- O HTML não busca RSS diretamente do navegador. O GitHub Actions executa `atualizar.py`, que transforma os feeds em `noticias.json`.
- Se um feed falhar, o coletor conserva os últimos dados salvos daquela fonte.
- As imagens dependem do que os feeds publicam e das permissões dos servidores de origem.
- O feed de Carlos Andreazza é um podcast; os cards mostram episódios, não artigos escritos.
- O GitHub Pages pode demorar alguns minutos para publicar. Verifique em Actions se o coletor rodou.
- As URLs de RSS são sujeitas a mudança pelos publicadores.

## Aba Futebol

- Quatro filtros: **ESPN Brasil**, **sportv**, **Palmeiras** e **Seleção Brasileira**.
- As manchetes são obtidas de pesquisas RSS do **Google Notícias** restritas às fontes ESPN Brasil e ge/sportv. Isso não é um RSS oficial da ESPN ou do sportv; resultados e imagens dependem da indexação do Google.
- O Google Notícias pode retornar links intermediários e algumas manchetes podem não ter imagem.
- Links diretos das quatro seções continuam disponíveis mesmo se a coleta falhar.
- A atualização ocorre no mesmo fluxo de duas horas das demais fontes.
