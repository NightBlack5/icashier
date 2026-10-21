# CashSave

Aplicativo de organização financeira feito com Reflex. A interface roda localmente e usa o grupo de APIs Xano configurado no ambiente para autenticação e persistência.

## Executar localmente no Windows

1. Crie ou ative um ambiente virtual e instale as dependências:

   ```powershell
   py -m venv .venv-cashsave
   .\.venv-cashsave\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Copie `.env.example` para `.env` e configure `CASH_SAVE_API_URL` com a URL do grupo CashSave no Xano. Não versione `.env`.

3. Inicie o app:

   ```powershell
   $env:PYTHONIOENCODING = "utf-8"
   reflex run --env prod --single-port
   ```

4. Abra o endereço local informado pelo Reflex (por padrão, `http://localhost:3000`).

O modo `prod` aqui só altera como o app é servido localmente; não publica o site. Para desenvolvimento com recarga automática, use `--env dev`.
No Windows, mantenha `PYTHONIOENCODING=utf-8` durante o comando de produção
para que o progresso Unicode do build não falhe no console com a codificação
legada `cp1252`.

## Verificações

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m unittest discover -s tests -v
reflex compile --dry
```

O app depende de endpoints publicados no Xano e de uma conta válida para testar fluxos autenticados. Os arquivos em `xano/` são a definição versionada das APIs e tabelas, não uma confirmação de que foram publicados no workspace remoto.

### Smoke test das rotas

Com o servidor em produção rodando, verifique no navegador as rotas abaixo:

| Rota | Resultado esperado sem sessão |
|---|---|
| `/` | Landing page pública |
| `/login` | Formulário de login |
| `/cadastro` | Formulário de cadastro |
| `/sobre` | Página institucional |
| `/suporte` | FAQ e suporte |
| `/apoiar` | Página de apoio |
| `/app` | Estado não autenticado, sem erro de servidor |
| `/assistente` | Estado não autenticado, sem erro de servidor |
| `/financas` | Estado não autenticado, sem erro de servidor |
| `/calendario` | Estado não autenticado, sem erro de servidor |
| `/perfil` | Estado não autenticado, sem erro de servidor |

As seis primeiras rotas são públicas e não devem depender do Xano para
renderizar. As cinco últimas usam carregamento protegido e devem ser abertas
sem sessão apenas para confirmar o estado de autenticação. O conjunto offline
de testes valida o registro das rotas e impede chamadas Xano no componente da
landing page:

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m unittest discover -s tests -v
```

Esse smoke test não confirma cadastro, login, persistência, isolamento entre
usuários, upload ou CRUD no Xano. Esses fluxos exigem uma conta de demonstração
isolada e um workspace Xano publicado com as definições versionadas.

## Assistente financeira local com Ollama

A página `/assistente` pode usar um modelo Ollama local para responder perguntas
somente de análise. O backend monta o contexto a partir dos dados financeiros
já carregados para o usuário autenticado; o navegador não acessa o Ollama e a
IA não cria, edita ou exclui registros.

O Ollama é opcional. Sem ele, o CashSave continua iniciando e a tela informa
explicitamente que o serviço local está indisponível.

### Instalação manual

1. Instale o Ollama pelo site oficial ou pelo gerenciador apropriado ao seu
   sistema operacional.
2. Inicie o serviço local e confirme que ele está escutando em
   `http://127.0.0.1:11434`.
3. Baixe manualmente um modelo compatível com a memória da máquina. Um ponto de
   partida é `llama3.2:3b`; modelos maiores exigem mais RAM/VRAM. O projeto não
   baixa modelos automaticamente.
4. Copie as variáveis `CASHSAVE_OLLAMA_*` de `.env.example` para `.env` e ajuste
   o nome do modelo, se necessário.
5. Reinicie o CashSave após alterar o `.env`.

O ambiente auditado desta máquina não possui o comando `ollama`, portanto a
integração real com um modelo não foi executada nesta etapa. Os testes usam
respostas mockadas e não são prova do comportamento de um modelo real.

### Limites da primeira versão

- A pergunta tem limite de 1200 caracteres por padrão.
- O contexto, histórico e resposta possuem limites configuráveis.
- A projeção usa a média simples dos últimos meses disponíveis e é apresentada
  como estimativa, nunca como certeza.
- Com menos de dois meses de transações, a projeção é marcada como insuficiente.
- A assistente não executa SQL, código, ferramentas ou operações financeiras.