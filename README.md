# Flash-Lite

Assistente inteligente de otimização e desempenho para PC, focado em usuários
comuns e jogos. O projeto segue a especificação em
`/home/cayoh093/Downloads/otimizador_inteligente_pc.md`.

## Estado atual

O primeiro incremento do MVP já contém:

- scanner de CPU, memória e armazenamento;
- lista dos processos que mais usam RAM;
- descoberta de aplicativos de inicialização no Windows e Linux;
- motor de regras para prévia de arquivos limpáveis;
- classificação de risco e proteção contra caminhos perigosos;
- quarentena reversível para ações confirmadas;
- histórico local em SQLite;
- dashboard inicial em PySide6 e modo CLI.

A limpeza começa em modo de prévia. Nenhum arquivo é apagado silenciosamente.

## Executar

Com Python 3.12+ e as dependências instaladas:

```bash
python -m pip install -e ".[dev]"
python main.py
```

Para uma leitura rápida no terminal:

```bash
python main.py --cli
```

Os dados locais são gravados em `~/.local/share/flash-lite` no Linux e em
`%LOCALAPPDATA%\\Flash-Lite` no Windows.

## Testar

```bash
python -m pytest
```

O backend Windows foi desenhado para ser usado sem manter a interface como
administrador. Ações que exigirem elevação e integrações específicas serão
adicionadas somente depois que o fluxo de prévia, confirmação e rollback
estiver estabilizado.

