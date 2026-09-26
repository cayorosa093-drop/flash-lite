# Flash-Lite

## Assistente inteligente de otimização e desempenho para PC

> **Deixe seu PC pronto para jogar sem precisar entender de otimização.**

O **Flash-Lite** é um aplicativo desktop pensado para pessoas que jogam no PC, mas não sabem identificar ou corrigir problemas de desempenho. Seu objetivo é analisar o computador, explicar o que está acontecendo em linguagem simples e recomendar ações seguras, reversíveis e baseadas em evidências.

O nome representa a proposta do produto:

- **Flash:** rapidez, resposta imediata e desempenho;
- **Lite:** leveza, simplicidade e baixo consumo de recursos.

## Objetivo do projeto

O objetivo final é permitir que alguém sem conhecimento técnico consiga descobrir o que está deixando o PC lento e melhorar o sistema com segurança.

O Flash-Lite não deve ser apenas um “FPS Booster” que fecha processos ou promete ganhos irreais. Ele deve:

- analisar o computador e identificar problemas reais;
- explicar diagnósticos e recomendações em linguagem simples;
- limpar somente itens conhecidos e revisados;
- preparar o PC temporariamente para jogos;
- medir o resultado antes e depois das mudanças;
- restaurar alterações quando necessário;
- usar IA para explicar o diagnóstico, nunca para decidir sozinha o que será apagado.

Em resumo:

> **O usuário não precisa entender de otimização para ter um PC bem configurado.**

## Público-alvo

O público principal são gamers com computadores antigos ou de entrada e usuários que:

- não sabem quais processos podem fechar;
- não distinguem cache, arquivos pessoais e arquivos do sistema;
- não conhecem conceitos como plano de energia, shader cache, prioridade ou processos em segundo plano;
- querem melhorar estabilidade e desempenho sem correr o risco de quebrar o sistema.

## Posicionamento

O produto pode ser entendido como:

> **Um assistente inteligente de desempenho para PC.**

As áreas principais são:

1. **Limpeza:** libera espaço usando regras explicáveis e seguras;
2. **Desempenho:** identifica consumo desnecessário de CPU, RAM, disco, GPU e rede;
3. **Gaming:** prepara o computador temporariamente enquanto um jogo está aberto.

Toda recomendação deve responder: **por que isso está sendo recomendado?**

## Princípios do produto

- segurança antes de ganho marginal;
- transparência, sem otimizações misteriosas;
- linguagem simples na interface principal;
- métricas reais em vez de promessas de FPS;
- mudanças reversíveis sempre que tecnicamente possível;
- nenhum arquivo pessoal tratado como lixo automaticamente;
- IA como assistente de explicação, não como autoridade destrutiva.

O programa nunca deve piorar o PC tentando otimizá-lo.

## O que já está implementado

A versão atual já possui uma fundação funcional de diagnóstico e limpeza segura:

- coleta de CPU, memória RAM e armazenamento;
- cálculo de um indicador de saúde de 0 a 100;
- listagem dos processos que mais consomem memória;
- detecção de aplicativos configurados para iniciar com o sistema;
- análise de arquivos por regras JSON;
- classificação de itens por risco;
- seleção automática apenas de itens de risco muito baixo ou baixo;
- prévia com categoria, caminho, tamanho e explicação;
- confirmação explícita antes da limpeza;
- quarentena reversível em vez de exclusão direta;
- histórico local de scans e ações em SQLite;
- interface gráfica com Início, Jogos, Limpeza, Desempenho e Assistente;
- respostas locais simples sobre CPU, RAM, disco e limpeza.

## Arquitetura atual

```text
app/
├── core/
│   ├── models.py              # Modelos de dados e níveis de risco
│   ├── service.py             # Orquestra scanners, regras e backends
│   ├── safety.py              # Validações antes de mexer em arquivos
│   ├── cleaner.py             # Quarentena e restauração
│   └── scanner/
│       ├── system.py          # CPU, RAM, disco e distribuição Linux
│       ├── processes.py       # Processos ordenados por uso de memória
│       └── cleanup.py         # Regras e geração da prévia de limpeza
├── database/
│   └── sqlite.py              # Histórico local de scans e ações
├── platforms/
│   ├── factory.py             # Escolha do backend por sistema operacional
│   ├── base.py                # Contrato dos backends
│   ├── windows/backend.py     # Itens Run do Registro do Windows
│   ├── linux/backend.py       # Arquivos XDG de autostart
│   └── generic/backend.py     # Fallback para outras plataformas
├── rules/windows/
│   └── cleanup.json           # Regras atuais de limpeza do Windows
└── ui/
    └── main_window.py         # Interface gráfica PySide6
```

### Fluxo principal

1. `FlashLiteService` coordena a aplicação.
2. `SystemScanner` coleta CPU, RAM, disco e plataforma.
3. O resultado vira um `SystemSnapshot` e pode ser gravado no SQLite.
4. `ProcessScanner` identifica os maiores consumidores de memória.
5. `CleanupRuleScanner` lê as regras aplicáveis e cria `CleanupCandidate`.
6. A interface exibe origem, risco, tamanho e explicação antes de qualquer ação.
7. Após a confirmação, `SafetyEngine` valida cada item.
8. `QuarantineCleaner` move os arquivos aprovados para a quarentena e registra um manifesto para restauração.

## Estratégia de plataformas

### Windows-first

O Windows é a prioridade máxima porque concentra o maior público gamer e oferece grande oportunidade para simplificar processos, serviços, inicialização e modo jogo.

O backend atual lê os itens `Run` do Registro por meio de `winreg` e possui regras de limpeza para temporários, miniaturas e cache de shaders.

### Linux-native

Linux deve ter suporte oficial, mas não ser tratado como uma cópia do Windows. O núcleo deve ser compartilhado e os backends devem respeitar as características de cada ambiente.

No futuro, o projeto poderá detectar distribuição, desktop environment, áudio, launcher, ferramentas de energia e integrações como GameMode, Gamescope e MangoHud. A arquitetura planejada contempla adapters para sistemas Arch-based, Debian-based, Fedora e sistemas imutáveis como Bazzite.

## Interface atual

- **Início:** score de saúde, métricas e alertas simples.
- **Jogos:** área preparada para integração com Steam e outros launchers; ainda é um placeholder.
- **Limpeza:** prévia de arquivos e envio dos itens confirmados para quarentena.
- **Desempenho:** CPU, RAM, disco e os dez maiores consumidores de memória, com atualização a cada cinco segundos.
- **Assistente:** respostas locais sobre CPU, RAM, disco e limpeza.

## Recursos planejados

### Modo jogo

Ao detectar um jogo, o Flash-Lite poderá oferecer:

- pausar processos dispensáveis;
- interromper downloads e sincronizações escolhidos pelo usuário;
- ativar modo de jogo ou GameMode;
- ajustar temporariamente o plano de energia;
- priorizar o processo do jogo dentro de limites seguros;
- silenciar notificações;
- monitorar temperaturas e recursos;
- restaurar tudo quando o jogo fechar.

### Diagnóstico de desempenho

O produto deverá identificar se o problema está relacionado a CPU, GPU, RAM, VRAM, armazenamento, temperatura, rede ou processos em segundo plano. Para jogos, o diagnóstico deve observar FPS, frametime e `1% lows`, evitando atribuir qualquer lentidão a um único componente sem medir o contexto.

### Benchmark antes e depois

Uma funcionalidade planejada é comparar uma sessão antes e depois de uma otimização:

```text
Antes:  FPS médio 47  |  1% low 29
Depois: FPS médio 51  |  1% low 36
Resultado: +8% de FPS médio e +24% no 1% low
```

Se não houver melhora significativa, o programa deve informar isso e oferecer o desfazimento da mudança.

### Perfis de otimização

- **Seguro:** apenas alterações de baixo risco;
- **Recomendado:** equilíbrio entre desempenho, consumo e estabilidade;
- **Máximo desempenho:** alterações mais agressivas, sempre com aviso sobre consumo, temperatura e efeitos colaterais.

### Rollback e histórico

Cada otimização relevante deverá registrar configuração anterior, estado atual, mudança realizada, data e motivo. O usuário deverá ter um comando claro para desfazer otimizações e comparar sessões anteriores.

## Limpeza inteligente

A regra central é:

> **Um arquivo não é desnecessário apenas porque é antigo ou grande.**

Cada resultado deverá informar tipo, origem, tamanho, função, motivo da recomendação, risco, possibilidade de recriação e possível efeito após a limpeza.

Categorias previstas:

- temporários do Windows;
- caches de aplicativos e navegadores;
- miniaturas;
- logs antigos;
- resíduos de atualização;
- crash dumps;
- cache de shaders;
- instaladores antigos;
- Lixeira, Downloads e arquivos grandes, sempre exigindo revisão.

Arquivos pessoais, saves, documentos, DLLs, drivers, configurações, componentes do Windows, arquivos em uso e origens desconhecidas devem ser protegidos ou desmarcados.

### Classificação de risco

| Nível | Significado | Exemplos |
| --- | --- | --- |
| 🟢 Muito baixo / baixo | Conhecido, recriável e sem conteúdo pessoal esperado | temporários, miniaturas e alguns caches |
| 🟡 Revisar | Pode ser removido, mas depende do contexto do usuário | Lixeira, logs, crash dumps, shaders e instaladores |
| 🔴 Alto / não recomendado | Pode conter dados pessoais ou afetar o sistema | saves, documentos, drivers, DLLs e componentes protegidos |

O risco deve ser definido por regras verificáveis, não apenas por tamanho, extensão ou idade.

### Fluxo obrigatório de segurança

```text
Arquivo encontrado
    ↓
Identificar origem e função
    ↓
Verificar uso, dependências e recriação
    ↓
Classificar o risco
    ↓
Explicar em linguagem simples
    ↓
Usuário escolhe
    ↓
Proteger, limpar e registrar
    ↓
Medir o resultado e permitir desfazer
```

## Proteções implementadas

A limpeza atual foi desenhada para ser reversível:

- não usa exclusão direta com `unlink`;
- exige confirmação explícita;
- rejeita links simbólicos;
- exige que o arquivo esteja dentro da raiz aprovada pela regra;
- bloqueia caminhos que contenham áreas protegidas como `Windows`, `System32`, `Program Files`, `Installer` e `WinSxS`;
- nunca seleciona automaticamente itens de alto risco;
- ignora arquivos inexistentes, bloqueados ou que não sejam arquivos comuns;
- registra as movimentações em `quarantine.json`.

O mecanismo de decisão deve ser determinístico. A IA pode melhorar a explicação, mas não pode decidir sozinha que um arquivo deve ser removido.

## Papel da IA

A IA será um assistente contextual para:

- explicar arquivos e processos;
- traduzir termos técnicos;
- resumir o diagnóstico;
- responder perguntas como “posso apagar isso?” ou “por que meu PC está lento?”;
- adaptar a explicação ao nível de conhecimento do usuário.

Fluxo planejado:

```text
Scanner → Motor de regras → Safety Engine → Resultado estruturado → IA explica
```

A IA não terá controle de ações destrutivas. Dados pessoais, nomes de usuário, caminhos completos e outras informações sensíveis devem ser removidos ou anonimizados antes de qualquer envio externo. A integração futura deverá usar um provedor substituível, sem salvar chaves no código-fonte.

## Modelo de segurança para otimizações futuras

A interface não deve permanecer aberta como administrador. Quando uma ação exigir elevação, a arquitetura planejada é:

```text
Interface sem privilégios
        ↓
Core e motor de segurança
        ↓
Helper administrativo limitado
        ↓
API oficial do sistema
```

O helper deverá aceitar apenas operações conhecidas e validadas. Comandos PowerShell, quando necessários, devem usar parâmetros validados e saídas estruturadas, sem montar comandos administrativos a partir de texto livre ou respostas da IA.

## Tecnologias

### Em uso no MVP atual

- Python 3.11 ou superior;
- PySide6 para a interface;
- psutil para monitoramento;
- SQLite para histórico;
- JSON para regras de limpeza.

### Planejadas

- Python 3.12+ como versão de referência;
- `winreg`, `ctypes`, pywin32 e WMI/CIM para integrações avançadas com Windows;
- YAML ou JSON para o motor de regras;
- API de IA com provedor substituível;
- PyInstaller para empacotamento;
- Inno Setup para o instalador do Windows;
- pytest e GitHub Actions para testes e automação.

## Dados locais

O estado local normalmente fica em:

- Windows: `%LOCALAPPDATA%/Flash-Lite`;
- Linux: `$XDG_DATA_HOME/flash-lite` ou `~/.local/share/flash-lite`;
- fallback: `./flash-lite-data`, quando a pasta padrão do usuário não puder ser criada.

Nesse diretório são armazenados o banco `flash-lite.db`, a pasta `quarantine/` e o manifesto `quarantine.json`.

## Como executar

O projeto possui `pyproject.toml` e `main.py` na pasta pai de `app`. As dependências mínimas são `psutil` e `PySide6`.

Execute a partir da pasta pai do projeto:

```bash
cd /home/cayoh093/Projetos/flash-lite
python -m pip install psutil PySide6
python -c "from app.ui.main_window import run_app; raise SystemExit(run_app())"
```

No Linux, é necessário um ambiente com display disponível. No Windows, o backend de inicialização usa `winreg` para ler as chaves `Run` do Registro.

Para gerar um aplicativo Windows com todas as dependências incluídas e um instalador `.exe`, consulte [`BUILD_WINDOWS.md`](BUILD_WINDOWS.md). O build deve ser executado no Windows.

## Roadmap

### V1 — Fundação Windows

- scanner do PC;
- limpeza segura;
- aplicativos de inicialização;
- processos consumindo RAM;
- interface simples;
- primeiro modo jogo.

### V2 — Perfis e medições

- perfis por jogo;
- benchmark antes/depois;
- histórico de sessões;
- diagnóstico de gargalos.

### V3 — Assistente

- chat contextual;
- explicações adaptadas ao usuário;
- integração com provedor de IA com proteção de privacidade.

### V4 — Linux

- Arch-based;
- Debian/Ubuntu;
- Fedora;
- sistemas imutáveis como Bazzite;
- GameMode, Gamescope, MangoHud e ferramentas de energia.

## Estado atual e próximos passos

O núcleo de diagnóstico e a limpeza segura já estão estruturados, mas o projeto ainda é uma primeira versão:

- falta um entrypoint oficial;
- falta declarar e fixar dependências;
- não há testes automatizados visíveis;
- a restauração da quarentena existe no `QuarantineCleaner`, mas ainda não está exposta na interface;
- a página de jogos ainda é um placeholder;
- a interface lista itens de inicialização, mas ainda não permite editá-los;
- o histórico é gravado, mas ainda não possui gráficos ou tela de consulta;
- modo jogo, benchmark, otimizações temporárias e IA externa ainda estão planejados.

O diferencial pretendido do Flash-Lite não é apenas encontrar “7 GB de lixo”, mas explicar a composição:

```text
Encontramos 7 GB que podem ser removidos.

4,2 GB são caches seguros.
1,7 GB são instaladores antigos.
1,1 GB estão na pasta Downloads e podem ser pessoais.

Recomendamos limpar apenas os 5,9 GB classificados como seguros.
```

## Resumo

O Flash-Lite será um assistente inteligente de otimização e desempenho para PC, focado em usuários comuns e gamers. Ele deverá analisar o sistema, explicar problemas em linguagem simples, aplicar otimizações seguras, limpar arquivos desnecessários, preparar o computador para jogos, medir resultados e desfazer alterações.

Prioridade de plataformas:

```text
Prioridade máxima: Windows
Suporte oficial: Linux
Estratégia Linux: Windows-first, Linux-native
```

**Objetivo final:** fazer com que uma pessoa que não sabe nada sobre otimização consiga entender o que está deixando seu PC lento e melhorar o sistema com segurança.
