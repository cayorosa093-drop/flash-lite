"""Entry point do Flash-Lite."""

from __future__ import annotations

import argparse
import json

from app.core.service import FlashLiteService


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Assistente seguro de otimização e desempenho para PC."
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="exibe o diagnóstico no terminal em vez de abrir a interface",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="com --cli, imprime o diagnóstico como JSON",
    )
    return parser


def _run_cli(service: FlashLiteService, as_json: bool = False) -> int:
    snapshot = service.scan_system()
    processes = service.top_processes(limit=8)
    startup = service.startup_entries()

    result = {
        "system": snapshot.to_dict(),
        "top_processes": [item.to_dict() for item in processes],
        "startup_count": len(startup),
        "startup": [item.to_dict() for item in startup],
    }

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"Flash-Lite — saúde estimada: {snapshot.health_score}/100")
    print(
        f"Sistema: {snapshot.platform} | CPU: {snapshot.cpu_percent:.0f}% | "
        f"RAM: {snapshot.memory_percent:.0f}% | "
        f"Disco livre: {snapshot.disk_free_percent:.0f}%"
    )
    print("\nProcessos com maior uso de RAM:")
    for process in processes:
        print(f"  - {process.name} (PID {process.pid}): {process.memory_mb:.1f} MB")
    print(f"\nAplicativos de inicialização detectados: {len(startup)}")
    return 0


def main() -> int:
    args = _build_parser().parse_args()
    service = FlashLiteService()

    if args.cli:
        return _run_cli(service, as_json=args.json)

    from app.ui.main_window import run_app

    return run_app(service)


if __name__ == "__main__":
    raise SystemExit(main())

