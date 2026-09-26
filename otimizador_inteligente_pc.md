# Flash-Lite

## Assistente Inteligente de Otimização e Desempenho para PC

## Nome do Projeto

**Flash-Lite**

O nome transmite os principais objetivos do projeto:

- **Flash**: rapidez, resposta imediata e desempenho;
- **Lite**: leveza, simplicidade e baixo consumo de recursos.

O Flash-Lite deve ser especialmente leve para continuar funcionando bem justamente em computadores antigos ou de entrada, que fazem parte do público-alvo do projeto.

> **Flash-Lite — deixe seu PC pronto para jogar sem precisar entender de otimização.**

---

## Visão Geral

Este projeto é um **otimizador inteligente de PC focado principalmente em jogos e em usuários que não sabem otimizar o próprio computador**.

A proposta não é criar mais um “FPS Booster” genérico que fecha alguns processos, limpa RAM e promete ganhos irreais.

A ideia é construir um sistema que:

- analisa o computador;
- identifica problemas reais;
- explica tudo em linguagem simples;
- recomenda ações seguras;
- aplica otimizações com poucos cliques;
- mede o resultado;
- restaura alterações quando necessário;
- usa IA apenas para ajudar o usuário a entender o que está acontecendo.

A filosofia central do produto é:

> **O usuário não precisa entender de otimização para ter um PC bem configurado.**

---

# 1. Público-alvo

O público principal são pessoas que:

- jogam no PC;
- têm computadores antigos ou de entrada;
- não entendem de otimização;
- não sabem quais processos podem fechar;
- não sabem quais arquivos podem apagar;
- não sabem diferenciar cache, arquivos pessoais e arquivos do sistema;
- não entendem conceitos como prioridade de CPU, serviços, plano de energia, shader cache, processos em segundo plano etc.;
- querem melhorar o PC sem correr risco de quebrar o sistema.

Exemplo de usuário:

> Uma pessoa com um PC antigo percebe que os jogos estão travando, mas não sabe se o problema é RAM, armazenamento, processos em segundo plano, temperatura ou configuração do sistema.

O programa deve responder a essa pessoa em linguagem simples.

---

# 2. Posicionamento

O produto não deve se posicionar apenas como:

> "FPS Booster"

A proposta é mais ampla.

Possíveis formas de definir o projeto:

> **Assistente inteligente de desempenho para PC.**

ou:

> **Um otimizador para pessoas que não sabem otimizar o PC.**

ou:

> **Deixe seu PC pronto para jogar com um clique.**

O objetivo é juntar:

- otimização;
- diagnóstico;
- limpeza;
- modo jogo;
- monitoramento;
- explicações;
- automação;
- segurança;
- benchmark.

---

# 3. Plataforma prioritária

## Prioridade máxima: Windows

O Windows será a plataforma principal.

Motivos:

- maior público gamer;
- maior quantidade de usuários leigos;
- grande quantidade de processos e serviços em segundo plano;
- muito espaço para automação e simplificação;
- forte demanda por ferramentas de limpeza e otimização.

A maior parte do esforço inicial deve ir para Windows.

Sugestão:

- 70–80% do esforço inicial em Windows;
- 20–30% em Linux.

---

# 4. Linux

Linux terá suporte oficial, mas não deve ser tratado como um simples port do Windows.

A ideia é:

> **Windows-first, Linux-native.**

O aplicativo terá um núcleo compartilhado, mas diferentes backends para cada sistema.

No Linux, o projeto deve detectar:

- distribuição;
- família da distribuição;
- desktop environment;
- compositor;
- sistema de áudio;
- ferramentas de energia;
- launcher de jogos;
- sistema de pacotes;
- suporte a GameMode;
- suporte a Gamescope;
- suporte a MangoHud.

---

# 5. Arquitetura geral

```text
                  Interface
                      │
                      ▼
              Optimization Core
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
 Windows Engine                Linux Engine
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
             Arch-based        Debian-based       Fedora-based
```

O Core deve ser independente do sistema operacional.

Exemplo:

```python
optimizer.clean_storage()
optimizer.optimize_game(game)
optimizer.get_startup_apps()
optimizer.set_performance_mode()
optimizer.restore()
```

O Core pede uma ação.

O backend do sistema decide como executar.

---

# 6. Arquitetura modular do Linux

Não criar um aplicativo diferente para cada distro.

Criar módulos/adapters.

Exemplo:

```text
Linux
│
├── Distribution
│   ├── Arch
│   ├── Debian
│   ├── Fedora
│   └── Fedora Atomic
│
├── Desktop
│   ├── KDE Plasma
│   ├── GNOME
│   └── Hyprland
│
├── Audio
│   └── PipeWire
│
├── Gaming
│   ├── Steam
│   ├── Lutris
│   └── Heroic
│
└── Power
    ├── power-profiles-daemon
    ├── TLP
    └── tuned
```

---

# 7. Distribuições Linux

## Arch-based

Exemplos:

- Arch Linux;
- CachyOS;
- EndeavourOS;
- Manjaro.

Integrações possíveis:

- pacman;
- systemd;
- PipeWire;
- GameMode;
- MangoHud;
- Gamescope;
- KDE;
- Hyprland;
- power-profiles-daemon.

---

## Debian-based

Exemplos:

- Debian;
- Ubuntu;
- Linux Mint;
- Pop!_OS.

Integrações possíveis:

- apt;
- systemd;
- Snap;
- Flatpak;
- GameMode;
- GNOME;
- KDE;
- power profiles.

---

## Fedora-based

Exemplos:

- Fedora;
- Nobara.

Integrações:

- dnf;
- rpm;
- systemd;
- GameMode;
- Gamescope;
- Flatpak.

---

## Sistemas imutáveis

Exemplos:

- Bazzite;
- Fedora Silverblue;
- Fedora Kinoite.

Esses sistemas precisam de tratamento diferente.

Exemplo:

```text
Sistema detectado:
Bazzite

Base:
Fedora Atomic

Backend:
FedoraImmutableOptimizer
```

O programa nunca deve assumir que Fedora normal e Fedora Atomic funcionam da mesma forma.

---

# 8. Detecção do ambiente

Ao iniciar, o programa deve detectar automaticamente:

```text
Sistema: Linux
Distribuição: CachyOS
Família: Arch
Desktop: KDE Plasma
Áudio: PipeWire
GPU: AMD
Launcher: Steam
GameMode: instalado
MangoHud: instalado
Gamescope: disponível
```

A partir disso, carrega os módulos corretos.

---

# 9. Referências de outros programas

O objetivo não é copiar um único produto.

A ideia é pegar o melhor de várias ferramentas.

---

## Razer Cortex

Aproveitar:

- modo jogo;
- detecção automática de jogos;
- pausa de processos;
- preparação do PC antes do jogo;
- restauração depois que o jogo fecha.

Melhorar:

- mais transparência;
- explicar o que está sendo feito;
- evitar promessas genéricas de FPS;
- mostrar resultado real.

---

## Microsoft PC Manager

Aproveitar:

- simplicidade;
- interface amigável;
- poucos botões;
- visão rápida da saúde do PC;
- boa experiência para usuários leigos.

---

## BleachBit

Aproveitar:

- identificação de cache;
- temporários;
- logs;
- arquivos descartáveis;
- preview antes da limpeza;
- abordagem transparente.

Melhorar:

- linguagem simples;
- classificação de risco;
- explicação detalhada;
- integração com jogos.

---

## Process Lasso

Aproveitar:

- prioridade de processos;
- gerenciamento inteligente de CPU;
- CPU Sets;
- affinity;
- I/O priority;
- regras por processo.

Mas esconder a complexidade do usuário comum.

Em vez de:

```text
CPU Affinity
CPU Sets
Priority Class
```

mostrar:

> **Priorizar seu jogo**

---

## CCleaner

Aproveitar:

- gerenciamento de programas em segundo plano;
- startup apps;
- limpeza;
- detecção de aplicações consumindo recursos.

---

## Chris Titus Tech WinUtil

Aproveitar:

- tweaks reais do Windows;
- presets;
- debloat;
- ajustes de serviços;
- opções avançadas;
- rollback.

Evitar:

- complexidade excessiva para usuários comuns.

---

## GameMode

Aproveitar no Linux:

- otimização temporária;
- CPU governor;
- prioridade;
- scheduler;
- scripts;
- ajustes durante a execução de jogos.

---

# 10. Tela inicial

A tela inicial deve mostrar o estado geral do computador.

Exemplo:

```text
Saúde do PC: 68/100

🟢 CPU: normal
🟡 RAM: utilização alta
🟢 Temperatura: normal
🔴 Armazenamento: quase cheio
🟡 14 programas iniciam junto com o sistema

[ Melhorar meu PC ]
```

O usuário não deve precisar entender os detalhes técnicos.

---

# 11. O que o Flash-Lite deve otimizar

O Flash-Lite não deve tentar “otimizar tudo”. Ele deve se concentrar no que realmente pode melhorar:

- estabilidade e consistência dos jogos;
- FPS e, principalmente, frametime e `1% lows`;
- tempo de inicialização do sistema;
- uso de RAM, CPU, GPU, disco e rede;
- espaço livre no armazenamento;
- facilidade para descobrir o que está deixando o computador lento.

O programa não deve prometer ganhos irreais. Antes de recomendar uma mudança, precisa identificar o problema, estimar o impacto e explicar o motivo.

## Inicialização do sistema

Detectar programas que iniciam junto com o Windows ou Linux e explicar:

- o que o programa faz;
- quanto ele atrasa a inicialização;
- quanto consome em segundo plano;
- se desativar a inicialização automática afeta seu funcionamento;
- como reativá-lo depois.

Desativar a inicialização automática não significa desinstalar o programa.

## Processos em segundo plano

Identificar aplicativos que consomem CPU, RAM, disco, GPU ou rede enquanto o usuário joga.

O FL deve permitir:

- manter o processo;
- pausar somente durante o jogo;
- fechar manualmente;
- ignorar permanentemente aquela recomendação;
- restaurar o estado ao encerrar o jogo.

## Arquivos temporários e caches

Analisar arquivos temporários, caches conhecidos, logs antigos, Lixeira, miniaturas e resíduos de atualizações.

Cada grupo deve mostrar:

- tamanho ocupado;
- origem;
- função;
- por que pode ser removido;
- possível efeito depois da limpeza;
- nível de risco;
- se o arquivo pode ser recriado.

## Modo jogo

Ao abrir um jogo, o Flash-Lite poderá aplicar otimizações temporárias, como:

- pausar processos dispensáveis;
- interromper downloads e sincronizações escolhidos pelo usuário;
- ativar o modo de jogo do sistema;
- ajustar temporariamente o plano de energia;
- aumentar a prioridade do processo do jogo dentro de limites seguros;
- silenciar notificações;
- restaurar todas as alterações quando o jogo fechar.

## RAM

Mostrar quais programas estão usando memória e recomendar fechar apenas os que forem realmente dispensáveis.

O Flash-Lite não deve usar falsos “limpadores de RAM”. Forçar a remoção de dados úteis da memória pode apenas transferir o trabalho para o disco e piorar o desempenho.

## CPU

Detectar:

- processos com uso anormal;
- plano de energia inadequado;
- limitação por temperatura;
- tarefas pesadas em segundo plano;
- provável gargalo de processador.

## GPU

Verificar:

- driver instalado e atualizações importantes;
- perfil de energia;
- processos usando a GPU em segundo plano;
- uso de VRAM;
- temperatura e throttling;
- provável gargalo gráfico.

O FL não deve prometer “FPS mágico” apenas por alterar opções da GPU.

## Armazenamento

Analisar:

- espaço livre;
- arquivos temporários e caches;
- arquivos muito grandes;
- Downloads esquecidos;
- instaladores antigos;
- jogos e programas pouco usados;
- velocidade e atividade excessiva do disco.

Arquivos grandes ou antigos nunca devem ser classificados automaticamente como lixo.

## Rede para jogos

Detectar atividades que podem aumentar ping, instabilidade ou perda de pacotes:

- downloads em segundo plano;
- launchers atualizando jogos;
- sincronização em nuvem;
- outros aplicativos consumindo banda;
- processos enviando ou recebendo muitos dados.

O FL deve explicar que nem toda lentidão de internet pode ser resolvida pelo computador.

## Serviços do sistema

Mostrar serviços potencialmente dispensáveis, mas agir com muito cuidado.

Nenhum serviço do Windows deve ser desativado apenas porque uma lista genérica da internet diz que ele é “inútil”. A recomendação deve considerar a função, dependências, estado atual e uso real daquele computador.

## Aplicativos instalados

Detectar programas esquecidos, duplicados, pouco usados ou considerados bloatware, mostrando primeiro:

- para que servem;
- quando foram usados;
- quanto espaço ocupam;
- quais componentes dependem deles;
- o que pode parar de funcionar se forem removidos.

## Configuração dos jogos

Usar o hardware e medições reais para sugerir uma configuração aproximada:

- resolução;
- qualidade baixa, média, alta ou personalizada;
- sombras;
- texturas conforme a VRAM;
- distância de visão;
- ray tracing;
- upscaling;
- limite de FPS.

As sugestões devem priorizar estabilidade e informar o custo visual de cada ajuste.

## Temperatura e throttling

Avisar quando CPU ou GPU reduzem a própria velocidade devido à temperatura. O programa deve diferenciar falta de desempenho causada por software de problemas térmicos ou limitações do hardware.

## Energia

Detectar quando um notebook está em economia de energia, funcionando sem o carregador ou usando um perfil inadequado durante o jogo.

Ao recomendar desempenho máximo, explicar o aumento de consumo, ruído e temperatura.

## Overlays

Mostrar o possível impacto de overlays do Discord, Steam, Xbox Game Bar, NVIDIA, AMD e outros aplicativos. O usuário decide quais serão mantidos, pois muitos overlays oferecem funções úteis.

## Atualizações

Avisar sobre drivers ou atualizações importantes do sistema, mas nunca instalar silenciosamente. O FL deve preferir fontes oficiais e permitir que o usuário veja o que será atualizado.

## Organização principal

O aplicativo pode apresentar suas funções em três níveis simples:

1. **Limpeza** — libera espaço removendo apenas itens analisados e explicados;
2. **Desempenho** — reduz consumo desnecessário de recursos;
3. **Gaming** — aplica ajustes temporários enquanto o jogo estiver aberto.

Em todas as áreas deve existir a pergunta:

> **Por que isso está sendo recomendado?**

Exemplo:

```text
Discord inicia junto com o PC

Impacto estimado: baixo/médio
Uso aproximado em segundo plano: 300 MB de RAM

Por que recomendamos isso?
O Discord permanece aberto mesmo quando você não está usando-o.

O que acontece se eu desativar?
Ele não será desinstalado. Você poderá abri-lo normalmente quando quiser.
```

## O que o Flash-Lite deve evitar

O programa não deve aplicar tweaks placebo ou perigosos, como:

- limpeza agressiva do Registro;
- “limpeza” forçada de RAM;
- desativação automática de dezenas de serviços;
- exclusão indiscriminada do Prefetch;
- alterações misteriosas em timers do Windows;
- tweaks de HPET sem diagnóstico;
- scripts e comandos da internet sem origem, explicação e reversão;
- promessas como “+300% de FPS”.

---

# 12. Limpeza inteligente do Windows

Uma das funções principais do Flash-Lite será mostrar arquivos possivelmente desnecessários do Windows de forma simples, explicando por que cada item existe e por que pode ou não ser removido.

O FL não deve mostrar apenas “lixo encontrado”. Ele deve separar os resultados por **tipo, origem, risco e motivo**.

| Categoria | Por que pode ser desnecessária | Possível efeito da limpeza | Risco padrão |
| --- | --- | --- | --- |
| Arquivos temporários do Windows | São criados durante instalações e operações temporárias e podem permanecer depois que a tarefa termina. | Normalmente nenhum; arquivos em uso devem ser ignorados. | 🟢 Muito baixo |
| Cache de aplicativos | Guarda dados para acelerar programas, mas pode crescer e geralmente pode ser recriado. | O aplicativo pode demorar um pouco mais na primeira abertura. | 🟢 Baixo |
| Cache de navegador | Armazena imagens, scripts e páginas para carregar sites mais rápido. | Sites podem carregar novamente os dados; contas, senhas e favoritos não devem ser apagados. | 🟢 Baixo |
| Lixeira | Contém itens que o usuário já excluiu, mas que ainda ocupam espaço. | Depois de esvaziada, a recuperação fica mais difícil. | 🟡 Revisar |
| Logs antigos | Registram atividades e erros; perdem utilidade depois do período relevante de diagnóstico. | Informações antigas de diagnóstico deixam de estar disponíveis. | 🟢 ou 🟡, conforme idade e origem |
| Miniaturas do Windows | São prévias de imagens e vídeos que o Windows consegue recriar. | As miniaturas podem levar alguns segundos para reaparecer. | 🟢 Muito baixo |
| Resíduos de atualização | São arquivos usados durante atualizações já concluídas e validadas. | Pode reduzir opções de reversão de determinadas atualizações. | 🟡 Revisar |
| Crash dumps | São gerados após travamentos para diagnóstico técnico. | O erro antigo ficará mais difícil de investigar. | 🟡 Revisar |
| Cache de shaders da GPU | Contém shaders compilados para acelerar jogos e pode ser recriado. | Pode haver pequenas travadas na primeira execução após a limpeza. | 🟡 Revisar |
| Instaladores antigos | Arquivos `.exe`, `.msi`, `.zip` ou semelhantes podem já ter sido usados. | Pode ser necessário baixá-los novamente; alguns podem ser pessoais ou importantes. | 🟡 Revisar |

O risco padrão pode mudar conforme origem, uso recente, bloqueio do arquivo, dependências e capacidade de recuperação.

## Informações obrigatórias para cada item

Cada resultado deve mostrar:

```text
Nome da categoria ou arquivo
Tamanho total
Localização
Origem provável

O que é?
Por que existe?
Por que pode ser removido?
O que não será perdido?
Qual efeito pode acontecer depois?
Foi usado recentemente?
Pode ser recriado?
Risco da limpeza

[ Ver arquivos ] [ Ignorar ] [ Limpar ]
```

Exemplo:

```text
Cache de miniaturas — 846 MB

Risco: 🟢 Muito baixo

O que é?
O Windows salva pequenas prévias de fotos e vídeos para mostrá-las mais rapidamente.

Por que posso apagar?
Esses arquivos podem ser recriados automaticamente pelo Windows.

Vou perder minhas fotos ou vídeos?
Não. Somente as prévias serão removidas.

Possível efeito:
As miniaturas podem demorar alguns segundos para reaparecer.

[ Ver arquivos ] [ Limpar 846 MB ]
```

Outro exemplo:

```text
Arquivo grande encontrado — 20,3 GB

Risco: 🔴 Não selecionar automaticamente

Não conseguimos determinar com segurança se este arquivo é desnecessário.
Ele pode ser um arquivo pessoal importante e não foi selecionado para remoção.

[ Abrir localização ] [ Ignorar ]
```

---

# 13. Classificação de risco

Todos os itens encontrados devem ter uma classificação baseada em regras verificáveis, e não somente em tamanho, extensão ou idade.

## Verde

```text
🟢 Seguro para limpar
```

Itens conhecidos, recriáveis e sem conteúdo pessoal esperado.

Exemplos:

- temporários não utilizados;
- miniaturas;
- caches conhecidos de baixo risco;
- logs antigos sem valor de diagnóstico atual.

Mesmo na categoria verde, arquivos em uso devem ser ignorados e nenhuma limpeza deve ocorrer silenciosamente.

## Amarelo

```text
🟡 Limpar com atenção
```

Itens que podem ser removidos, mas cuja utilidade depende do usuário ou do momento.

Exemplos:

- Lixeira;
- crash dumps;
- logs recentes;
- cache de shaders;
- caches de jogos;
- resíduos de atualização;
- Downloads;
- arquivos ISO;
- instaladores;
- arquivos grandes;
- arquivos duplicados;
- ZIPs antigos.

Esses itens não devem vir selecionados automaticamente quando houver chance de conter dados pessoais ou afetar recuperação e diagnóstico.

## Vermelho

```text
🔴 Não recomendado ou protegido
```

Itens que o Flash-Lite não consegue declarar desnecessários com segurança ou cuja remoção pode quebrar o sistema, programas ou dados do usuário.

Exemplos:

- saves;
- documentos e arquivos pessoais;
- DLLs;
- drivers;
- configurações;
- arquivos em uso;
- componentes do Windows;
- conteúdo de `C:\\Windows\\Installer`;
- conteúdo de `WinSxS` removido manualmente;
- arquivos de origem desconhecida.

O FL pode explicar por que esses itens ocupam espaço, mas não deve sugerir exclusão manual perigosa.

---

# 14. Regras e fluxo de segurança da limpeza

Regra principal:

> **Um arquivo não é desnecessário apenas porque é antigo ou grande.**

O programa nunca deve apagar automaticamente algo que possa ser pessoal, importante ou necessário ao sistema.

Fluxo obrigatório:

```text
Arquivo encontrado
    ↓
Identificar origem e função
    ↓
Verificar uso, dependências e possibilidade de recriação
    ↓
Classificar o risco
    ↓
Explicar em linguagem simples
    ↓
Usuário escolhe
    ↓
Criar proteção adequada
    ↓
Limpar e registrar a ação
    ↓
Medir o resultado e permitir desfazer
```

Proteções importantes:

- nunca apagar silenciosamente;
- começar com todos os itens duvidosos desmarcados;
- ignorar arquivos bloqueados ou em uso;
- preferir a Lixeira ou uma quarentena temporária quando possível;
- usar backup para arquivos que realmente possam ser restaurados;
- criar ponto de restauração antes de alterações relevantes do sistema;
- lembrar que ponto de restauração não substitui backup de arquivos pessoais;
- registrar arquivo, tamanho, origem, data e ação executada;
- permitir listas de exclusão;
- permitir desfazer sempre que tecnicamente possível;
- interromper a limpeza se a origem ou a classificação não forem confiáveis.

O mecanismo de decisão deve usar regras determinísticas e uma lista de locais e formatos conhecidos. A IA pode melhorar a explicação, mas não pode decidir sozinha que um arquivo deve ser removido.

---

# 15. IA

A IA será utilizada como um **assistente de explicação**.

Ela não deve ser responsável por decidir se algo pode ou não ser apagado.

Arquitetura:

```text
Scanner
   ↓
Motor de regras
   ↓
Safety Engine
   ↓
Classificação
   ↓
IA
   ↓
Explicação simples
```

A IA recebe apenas dados já analisados.

Exemplo:

```text
Arquivo:
Cache do Chrome

Tamanho:
3.4 GB

Classificação:
Seguro

Recriável:
Sim
```

A IA transforma isso em uma explicação humana.

---

# 16. IA rápida e leve

Para computadores antigos, a IA não deve necessariamente rodar localmente.

Modo recomendado:

```text
Aplicativo
    ↓
API
    ↓
modelo pequeno e rápido
    ↓
explicação
```

Uma possibilidade é utilizar serviços de inferência rápida como Groq.

O modelo não precisa ser gigantesco.

A função principal é:

- explicar;
- resumir;
- traduzir termos técnicos;
- responder dúvidas contextuais.

---

# 17. Chat contextual

O usuário poderá perguntar:

> "Posso apagar isso?"

> "Vou perder meu save?"

> "Por que meu PC está lento?"

> "Isso aumenta FPS?"

> "O que é esse processo?"

> "Por que isso está usando tanta RAM?"

A IA deve responder utilizando os dados reais do computador.

---

# 18. Modo jogo

Ao detectar um jogo:

```text
Jogo iniciado:
Cyberpunk 2077

Encontramos:
Chrome usando 2,3 GB de RAM
OneDrive sincronizando
Adobe Updater ativo
12 programas em segundo plano

Podemos liberar aproximadamente:
3,1 GB de RAM

[ Otimizar e jogar ]
```

---

# 19. Ações possíveis durante o modo jogo

Dependendo do sistema:

- alterar plano de energia;
- priorizar o jogo;
- pausar processos;
- suspender sincronizações;
- silenciar notificações;
- ativar GameMode;
- configurar CPU;
- ajustar prioridade de I/O;
- reduzir atividades em segundo plano;
- ativar overlay;
- limitar FPS;
- monitorar temperaturas;
- restaurar tudo ao fechar.

---

# 20. Perfis de otimização

Criar níveis simples.

## Seguro

Somente alterações de baixo risco.

```text
🟢 Seguro
```

---

## Recomendado

Equilíbrio entre desempenho, consumo e estabilidade.

```text
🟡 Recomendado
```

---

## Máximo desempenho

Mudanças mais agressivas.

```text
🔴 Máximo desempenho
```

Deve explicar:

- consumo maior;
- temperaturas maiores;
- possíveis efeitos colaterais.

---

# 21. Processos em segundo plano

O programa deve identificar aplicações consumindo recursos.

Exemplo:

```text
Spotify
RAM: 450 MB

Você usa Spotify enquanto joga?

[ Sim, manter ]
[ Não, pausar ]
```

Outro:

```text
Adobe Creative Cloud

Está executando mesmo sem nenhum aplicativo Adobe aberto.

Recomendação:
Pausar enquanto joga.

[ Pausar automaticamente ]
```

---

# 22. Apps de inicialização

Mostrar de forma simples:

```text
12 programas iniciam automaticamente com o Windows.

Isso pode aumentar o tempo de inicialização e consumir RAM.

Recomendamos desativar 7 deles.
```

Cada programa deve receber explicação individual.

---

# 23. Diagnóstico de gargalo

Uma funcionalidade importante será detectar o que realmente limita o jogo.

Monitorar:

- CPU;
- GPU;
- RAM;
- VRAM;
- armazenamento;
- temperatura;
- FPS;
- frametime;
- 1% lows.

Exemplo:

```text
GPU: 97%
CPU: 48%
RAM: 72%

Provável gargalo:
GPU

Fechar programas provavelmente terá pouco impacto no FPS.

Recomendação:
reduzir qualidade gráfica.
```

---

# 24. Benchmark antes e depois

Esse recurso diferencia o projeto de boosters genéricos.

Antes:

```text
FPS médio: 47
1% Low: 29
RAM usada: 7,3 GB
```

Depois:

```text
FPS médio: 51
1% Low: 36
RAM usada: 5,8 GB
```

Resultado:

```text
FPS médio: +8%
1% Low: +24%
RAM liberada: 1,5 GB
```

Se não melhorar:

> Nenhuma melhoria significativa detectada.

O programa deve poder recomendar desfazer a mudança.

---

# 25. Transparência

Regra central:

> **Nenhuma otimização misteriosa.**

Toda mudança deve mostrar:

```text
O que será alterado?
Por que?
Qual o benefício esperado?
Qual o risco?
É reversível?
```

Exemplo:

```text
Modo de desempenho da CPU

O que faz:
Mantém frequências maiores durante o jogo.

Benefício:
Pode reduzir oscilações de desempenho.

Desvantagem:
Maior consumo de energia e temperatura.

Reversível:
Sim.

[ Ativar ]
```

---

# 26. Sistema de rollback

Toda otimização importante deve poder ser desfeita.

O programa deve salvar:

```text
configuração anterior
estado atual
mudança realizada
data
motivo
```

Botão:

```text
[ Desfazer otimizações ]
```

---

# 27. Histórico

Registrar sessões:

```text
Minecraft
Data: 11/09/2026

Antes:
41 FPS
1% Low: 26

Depois:
48 FPS
1% Low: 34

RAM liberada:
1,4 GB
```

O usuário pode comparar sessões.

---

# 28. Explicar em vez de assustar

Evitar termos técnicos na interface principal.

Não mostrar:

```text
CPU Set
Affinity
Priority Class
I/O Priority
Shader Cache
```

sem explicação.

Mostrar:

```text
Priorizar o jogo
Reduzir programas em segundo plano
Liberar espaço
Melhorar estabilidade
```

O modo avançado pode revelar os detalhes técnicos.

---

# 29. Modos de interface

## Modo simples

Para usuários comuns.

Poucos botões.

Exemplo:

```text
[ Analisar meu PC ]

[ Otimizar ]

[ Jogos ]

[ Limpeza ]
```

---

## Modo avançado

Para usuários experientes.

Permitir:

- affinity;
- CPU Sets;
- serviços;
- power plans;
- GameMode;
- MangoHud;
- Gamescope;
- regras personalizadas;
- scripts.

---

# 30. Áreas principais do aplicativo

O aplicativo pode ser dividido em cinco áreas.

## Início

Resumo do computador.

## Jogos

Jogos instalados e perfis.

## Limpeza

Arquivos desnecessários.

## Desempenho

CPU, GPU, RAM, temperaturas e processos.

## Assistente

IA para explicações.

---

# 31. Estrutura sugerida

```text
optimizer/
│
├── core/
│   ├── scanner
│   ├── safety
│   ├── recommendations
│   ├── benchmark
│   ├── rollback
│   └── profiles
│
├── platforms/
│   ├── windows/
│   │
│   └── linux/
│       ├── arch/
│       ├── debian/
│       ├── fedora/
│       └── atomic/
│
├── integrations/
│   ├── steam
│   ├── lutris
│   ├── heroic
│   ├── gamemode
│   ├── mangohud
│   └── gamescope
│
├── ai/
│   ├── explanations
│   ├── prompts
│   └── providers
│
└── ui/
```

---

# 32. Tecnologias recomendadas

O MVP do Flash-Lite deve usar uma stack que permita desenvolver rápido, seja leve o suficiente para computadores de entrada e não impeça uma evolução mais profissional no futuro.

Stack principal recomendada:

| Parte do sistema | Tecnologia |
| --- | --- |
| Linguagem principal | Python 3.12 ou superior |
| Interface gráfica | PySide6 |
| Monitoramento do computador | psutil |
| Integração com Windows | pywin32, `winreg`, `ctypes`, PowerShell e WMI/CIM |
| Armazenamento local | SQLite |
| Regras de limpeza | YAML ou JSON |
| IA explicativa | API da Groq, com provedor substituível |
| Geração do executável | PyInstaller |
| Instalador do Windows | Inno Setup |
| Testes | pytest |
| Versionamento e automação | Git, GitHub e GitHub Actions |

## Python como linguagem principal

Python deve ser utilizado no MVP para:

- scanner de arquivos;
- motor de classificação de risco;
- análise de processos;
- monitoramento de CPU, RAM, disco e rede;
- recomendações;
- histórico;
- rollback;
- integração com a IA;
- coordenação dos backends de Windows e Linux.

A escolha combina com o nível atual de desenvolvimento do projeto, permite criar protótipos rapidamente e possui bibliotecas maduras para monitoramento e integração com o sistema.

Rust ou C++ não são necessários para começar. Se, no futuro, alguma parte crítica precisar de mais desempenho, controle de memória ou segurança, somente esse módulo poderá ser refeito em Rust sem reescrever todo o aplicativo.

## PySide6 para a interface

O PySide6 deve ser a interface principal por oferecer:

- componentes profissionais;
- tabelas grandes para exibir arquivos e processos;
- gráficos e painéis de monitoramento;
- ícone na bandeja do sistema;
- notificações;
- suporte a tarefas em segundo plano;
- separação entre interface e lógica;
- suporte oficial do Qt para Python;
- capacidade de crescer junto com o projeto.

CustomTkinter pode ser utilizado em um protótipo pequeno, mas PySide6 é mais adequado para a versão principal do Flash-Lite.

Documentação oficial: <https://doc.qt.io/qtforpython-6/>

## psutil para monitoramento

O psutil será utilizado para obter informações sobre:

- processos;
- CPU;
- memória RAM;
- discos;
- rede;
- prioridade e afinidade de processos;
- algumas informações de sensores, conforme o sistema.

Ele funciona tanto no Windows quanto no Linux, ajudando a manter uma parte do núcleo compartilhada.

Documentação oficial: <https://psutil.readthedocs.io/stable/>

## Integração específica com Windows

O backend do Windows utilizará:

- `winreg` para partes controladas do Registro e itens de inicialização;
- pywin32 para acessar APIs, processos, serviços e recursos do Windows;
- `ctypes` para funções nativas que não possuam uma abstração adequada;
- PowerShell para operações administrativas bem definidas;
- WMI/CIM para informações de hardware, sistema e drivers;
- APIs oficiais do Windows sempre que estiverem disponíveis.

Comandos PowerShell devem usar parâmetros validados e saídas estruturadas, preferencialmente JSON. O programa não deve montar comandos administrativos diretamente a partir de texto fornecido pelo usuário ou pela IA.

## Separação de privilégios

A interface do Flash-Lite não deve permanecer aberta como administrador.

Arquitetura recomendada:

```text
Interface sem privilégios
        ↓
Core e motor de segurança
        ↓
Solicitação de uma ação autorizada
        ↓
Helper administrativo com funções limitadas
        ↓
API do Windows
```

O helper administrativo deve aceitar apenas ações conhecidas e validadas. A elevação de privilégio deve acontecer somente quando uma função realmente precisar dela.

## Motor de regras

A decisão de limpeza deve ser baseada em regras determinísticas armazenadas em YAML ou JSON. A IA não participa da decisão de apagar.

Exemplo:

```yaml
- id: windows_thumbnails
  category: "Miniaturas do Windows"
  path: "%LOCALAPPDATA%/Microsoft/Windows/Explorer"
  patterns:
    - "thumbcache_*.db"
  risk: "very_low"
  recreatable: true
  automatic_selection: true
  explanation: >
    São prévias de imagens e vídeos que o Windows
    consegue recriar automaticamente.
```

Cada regra deve possuir, quando aplicável:

- identificador único;
- sistema operacional compatível;
- caminhos permitidos;
- padrões de nomes;
- proprietário ou aplicativo de origem;
- nível de risco;
- condições que impedem a limpeza;
- informação sobre recriação;
- seleção automática permitida ou proibida;
- estratégia de rollback;
- explicação padrão;
- testes automatizados.

Isso permite atualizar as regras, revisar falsos positivos e criar conjuntos diferentes para Windows e Linux sem reescrever o programa inteiro.

## SQLite

O SQLite armazenará localmente:

- configurações;
- histórico de análises;
- arquivos e recomendações ignorados;
- otimizações realizadas;
- estado anterior;
- resultados de benchmarks;
- perfis de jogos;
- registros necessários para desfazer ações.

O banco não precisa de servidor e combina com a proposta de um aplicativo leve.

## IA com Groq

A integração inicial poderá utilizar a API da Groq com um modelo pequeno e rápido.

A IA servirá apenas para:

- explicar arquivos e processos;
- traduzir termos técnicos;
- resumir diagnósticos;
- responder dúvidas contextuais;
- adaptar a explicação ao nível do usuário.

Fluxo:

```text
Scanner
   ↓
Motor de regras
   ↓
Safety Engine
   ↓
Resultado estruturado
   ↓
IA produz a explicação
```

A integração deve usar uma interface de provedor para que a Groq possa ser substituída ou acompanhada por outro serviço no futuro.

Informações pessoais, nomes de usuário, caminhos completos e outros dados sensíveis devem ser removidos ou anonimizados antes de qualquer envio externo. A chave da API nunca deve ser salva diretamente no código-fonte.

Documentação oficial: <https://console.groq.com/docs/quickstart>

## Distribuição do programa

O PyInstaller será utilizado inicialmente para empacotar o aplicativo e suas dependências. Assim, o usuário poderá executar o Flash-Lite sem instalar Python manualmente.

A versão do Windows deve ser gerada no Windows e a versão do Linux deve ser gerada no Linux, pois o PyInstaller não funciona como compilador cruzado.

O Inno Setup poderá criar o instalador final:

```text
Flash-Lite-Setup.exe
```

Documentação oficial do PyInstaller: <https://www.pyinstaller.org/en/stable/>

## Testes e qualidade

O pytest deve testar principalmente:

- regras de classificação;
- caminhos protegidos;
- arquivos que nunca podem ser removidos;
- estimativa de espaço recuperável;
- comportamento quando um arquivo está em uso;
- criação e execução do rollback;
- backends de cada sistema;
- entradas malformadas;
- falhas de permissão;
- garantia de que a IA não controla ações destrutivas.

O GitHub Actions poderá executar testes automaticamente a cada alteração. Testes que modificam o sistema devem usar ambientes isolados e dados falsos, nunca o computador real do usuário.

## Estrutura técnica sugerida

```text
flash-lite/
├── app/
│   ├── core/
│   │   ├── scanner/
│   │   ├── safety/
│   │   ├── optimizer/
│   │   ├── rollback/
│   │   └── benchmark/
│   ├── platforms/
│   │   ├── windows/
│   │   └── linux/
│   ├── rules/
│   │   ├── windows/
│   │   └── linux/
│   ├── ai/
│   │   ├── providers/
│   │   ├── explanations/
│   │   └── privacy/
│   ├── database/
│   ├── privileged_helper/
│   └── ui/
├── tests/
├── assets/
├── installer/
└── main.py
```

Escolha final para o MVP:

> **Python + PySide6 + psutil + APIs nativas do Windows + SQLite + Groq + PyInstaller.**

---

# 33. MVP

A primeira versão não precisa ter tudo.

## MVP Windows

Implementar:

1. scanner do PC;
2. armazenamento;
3. arquivos seguros para limpeza;
4. programas de inicialização;
5. processos consumindo RAM;
6. modo jogo;
7. CPU/RAM/GPU;
8. explicações simples;
9. rollback;
10. perfis de otimização.

---

# 34. Roadmap

## V1

Fundação.

- scanner;
- limpeza;
- startup;
- processos;
- modo jogo;
- Windows;
- interface simples.

## V2

Perfis por jogo.

## V3

Benchmark antes/depois.

## V4

Diagnóstico de gargalos.

## V5

Assistente de IA.

## V6

Linux Arch-based.

## V7

Debian/Ubuntu.

## V8

Fedora.

## V9

Sistemas imutáveis como Bazzite.

---

# 35. Filosofia de desenvolvimento

O projeto deve priorizar:

- segurança;
- simplicidade;
- transparência;
- reversibilidade;
- desempenho real;
- métricas;
- explicação;
- confiança.

Evitar:

- placebo;
- promessas absurdas;
- hacks sem comprovação;
- deletar arquivos silenciosamente;
- tweaks perigosos;
- mudanças irreversíveis;
- interface cheia de termos técnicos.

---

# 36. Regra principal

> **O programa nunca deve piorar o PC tentando otimizá-lo.**

Toda funcionalidade deve respeitar isso.

---

# 37. Diferencial final

O grande diferencial não será apenas otimizar.

Será explicar.

Outros programas normalmente dizem:

> Encontramos 7 GB de lixo.

Este projeto deve dizer:

> Encontramos 7 GB que podem ser removidos.
>
> 4,2 GB são caches seguros.
>
> 1,7 GB são instaladores antigos.
>
> 1,1 GB estão na pasta Downloads e podem ser pessoais.
>
> Recomendamos limpar apenas os 5,9 GB classificados como seguros.

---

# 38. Resumo do produto

O projeto será um:

> **Assistente inteligente de otimização e desempenho para PC, focado em usuários comuns e gamers, capaz de analisar o sistema, explicar problemas em linguagem simples, aplicar otimizações seguras, limpar arquivos desnecessários, preparar o computador para jogos, medir resultados e desfazer alterações.**

Plataformas:

```text
Prioridade máxima:
Windows

Suporte oficial:
Linux

Linux:
Arch
Debian
Fedora
Fedora Atomic
```

Objetivo final:

> Fazer alguém que não sabe absolutamente nada sobre otimização conseguir entender o que está deixando seu PC lento e melhorar o sistema com segurança.
