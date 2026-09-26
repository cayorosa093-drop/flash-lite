"""Interface gráfica inicial do Flash-Lite.

A interface mantém a linguagem simples da especificação e deixa as ações
destrutivas fora do caminho principal. A limpeza passa por prévia, confirmação
e quarentena reversível.
"""

from __future__ import annotations

import sys
from dataclasses import replace
from html import escape

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from app.core.cleaner import QuarantineCleaner
from app.core.models import CleanupCandidate, RiskLevel, SystemSnapshot
from app.core.service import FlashLiteService


APP_STYLE = """
* {
    font-family: "Segoe UI", "Noto Sans", sans-serif;
}
QMainWindow, QWidget {
    background: #f5f7fb;
    color: #172033;
}
QLabel {
    background: transparent;
}
QFrame#sidebar {
    background: #111827;
    border: 0;
}
QLabel#brand {
    color: #ffffff;
    font-size: 24px;
    font-weight: 700;
}
QLabel#brandCaption {
    color: #94a3b8;
    font-size: 12px;
}
QPushButton#navButton {
    background: transparent;
    color: #cbd5e1;
    border: 0;
    border-radius: 9px;
    padding: 11px 14px;
    text-align: left;
    font-size: 14px;
}
QPushButton#navButton:hover {
    background: #1f2937;
    color: #ffffff;
}
QPushButton#navButton:checked {
    background: #2563eb;
    color: #ffffff;
    font-weight: 600;
}
QLabel#pageTitle {
    color: #172033;
    font-size: 25px;
    font-weight: 700;
}
QLabel#pageSubtitle, QLabel#muted {
    color: #64748b;
}
QFrame#card, QGroupBox#card {
    background: #ffffff;
    border: 1px solid #e5eaf2;
    border-radius: 14px;
}
QFrame#heroCard {
    background: #eaf2ff;
    border: 1px solid #cfe0ff;
    border-radius: 16px;
}
QLabel#heroTitle {
    color: #173b7a;
    font-size: 20px;
    font-weight: 700;
}
QLabel#heroScore {
    color: #2563eb;
    font-size: 38px;
    font-weight: 800;
}
QLabel#metricTitle {
    color: #64748b;
    font-size: 12px;
    font-weight: 600;
}
QLabel#metricValue {
    color: #172033;
    font-size: 22px;
    font-weight: 700;
}
QLabel#sectionTitle {
    color: #172033;
    font-size: 16px;
    font-weight: 700;
}
QPushButton#primaryButton {
    background: #2563eb;
    color: #ffffff;
    border: 0;
    border-radius: 9px;
    padding: 10px 16px;
    font-weight: 600;
}
QPushButton#primaryButton:hover {
    background: #1d4ed8;
}
QPushButton#secondaryButton {
    background: #ffffff;
    color: #1d4ed8;
    border: 1px solid #bfd3f8;
    border-radius: 9px;
    padding: 9px 15px;
    font-weight: 600;
}
QPushButton#secondaryButton:hover {
    background: #eff6ff;
}
QPushButton#dangerButton {
    background: #dc2626;
    color: #ffffff;
    border: 0;
    border-radius: 9px;
    padding: 10px 16px;
    font-weight: 600;
}
QPushButton#dangerButton:hover {
    background: #b91c1c;
}
QProgressBar {
    background: #dbe7fa;
    border: 0;
    border-radius: 5px;
    height: 10px;
    text-align: center;
}
QProgressBar::chunk {
    background: #2563eb;
    border-radius: 5px;
}
QTableWidget, QListWidget, QTextBrowser {
    background: #ffffff;
    border: 1px solid #e5eaf2;
    border-radius: 10px;
    gridline-color: #eef2f7;
    selection-background-color: #dbeafe;
    selection-color: #172033;
}
QHeaderView::section {
    background: #f8fafc;
    color: #64748b;
    border: 0;
    border-bottom: 1px solid #e5eaf2;
    padding: 8px;
    font-weight: 600;
}
QLineEdit {
    background: #ffffff;
    border: 1px solid #d7deea;
    border-radius: 9px;
    padding: 10px 12px;
}
QLineEdit:focus {
    border: 1px solid #2563eb;
}
QGroupBox {
    border: 1px solid #e5eaf2;
    border-radius: 14px;
    margin-top: 8px;
    padding-top: 10px;
    font-weight: 700;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 13px;
    padding: 0 5px;
    color: #172033;
}
"""


def format_bytes(value: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{value} B"


def make_label(text: str, object_name: str | None = None) -> QLabel:
    label = QLabel(text)
    if object_name:
        label.setObjectName(object_name)
    return label


class MetricCard(QFrame):
    def __init__(self, title: str, value: str = "—", detail: str = "") -> None:
        super().__init__()
        self.setObjectName("card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 13, 16, 13)
        layout.setSpacing(3)
        layout.addWidget(make_label(title, "metricTitle"))
        self.value_label = make_label(value, "metricValue")
        layout.addWidget(self.value_label)
        self.detail_label = make_label(detail, "muted")
        self.detail_label.setWordWrap(True)
        layout.addWidget(self.detail_label)

    def set_value(self, value: str, detail: str | None = None) -> None:
        self.value_label.setText(value)
        if detail is not None:
            self.detail_label.setText(detail)


class MainWindow(QMainWindow):
    NAV_ITEMS = (
        ("⌂", "Início"),
        ("◈", "Jogos"),
        ("⌫", "Limpeza"),
        ("◒", "Desempenho"),
        ("?", "Assistente"),
    )

    def __init__(self, service: FlashLiteService) -> None:
        super().__init__()
        self.service = service
        self.current_snapshot: SystemSnapshot | None = None
        self.cleanup_candidates: list[CleanupCandidate] = []
        self.nav_buttons: list[QPushButton] = []
        self.setWindowTitle("Flash-Lite")
        self.setMinimumSize(960, 650)
        self.resize(1120, 720)
        self.setStyleSheet(APP_STYLE)
        self._build_ui()
        self.refresh_all()

        self.live_timer = QTimer(self)
        self.live_timer.timeout.connect(self.refresh_live_metrics)
        self.live_timer.start(5_000)

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 24, 30, 24)
        content_layout.setSpacing(18)
        content_layout.addLayout(self._build_topbar())

        self.pages = QStackedWidget()
        pages = (
            self._build_home_page(),
            self._build_games_page(),
            self._build_cleanup_page(),
            self._build_performance_page(),
            self._build_assistant_page(),
        )
        for page in pages:
            self.pages.addWidget(page)
        content_layout.addWidget(self.pages, 1)
        root_layout.addWidget(content, 1)
        self.setCentralWidget(root)

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(218)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 25, 18, 20)
        layout.setSpacing(8)

        layout.addWidget(make_label("Flash-Lite", "brand"))
        layout.addWidget(make_label("Otimização sem complicação", "brandCaption"))
        layout.addSpacing(27)

        group = QButtonGroup(self)
        group.setExclusive(True)
        for index, (icon, title) in enumerate(self.NAV_ITEMS):
            button = QPushButton(f"{icon}   {title}")
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.clicked.connect(lambda _checked, page=index: self.navigate(page))
            group.addButton(button, index)
            self.nav_buttons.append(button)
            layout.addWidget(button)

        layout.addStretch(1)
        layout.addWidget(make_label("v0.1 • Windows-first", "brandCaption"))
        self.nav_buttons[0].setChecked(True)
        return sidebar

    def _build_topbar(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        title_box = QVBoxLayout()
        self.page_title = make_label("Início", "pageTitle")
        title_box.addWidget(self.page_title)
        self.page_subtitle = make_label(
            "Veja rapidamente o que merece atenção no seu computador.", "pageSubtitle"
        )
        title_box.addWidget(self.page_subtitle)
        layout.addLayout(title_box)
        layout.addStretch(1)

        refresh = QPushButton("↻  Atualizar")
        refresh.setObjectName("secondaryButton")
        refresh.clicked.connect(self.refresh_all)
        layout.addWidget(refresh)
        return layout

    def _build_home_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        hero = QFrame()
        hero.setObjectName("heroCard")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(22, 18, 22, 18)
        hero_copy = QVBoxLayout()
        hero_copy.addWidget(make_label("Visão geral do seu PC", "heroTitle"))
        self.hero_message = make_label(
            "Analise o computador para receber recomendações simples e seguras."
        )
        self.hero_message.setWordWrap(True)
        hero_copy.addWidget(self.hero_message)
        self.hero_progress = QProgressBar()
        self.hero_progress.setRange(0, 100)
        self.hero_progress.setValue(0)
        self.hero_progress.setTextVisible(False)
        hero_copy.addWidget(self.hero_progress)
        hero_layout.addLayout(hero_copy, 1)
        self.hero_score = make_label("—", "heroScore")
        self.hero_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(self.hero_score)
        layout.addWidget(hero)

        metrics = QGridLayout()
        metrics.setSpacing(12)
        self.home_cpu = MetricCard("CPU", detail="uso atual")
        self.home_memory = MetricCard("RAM", detail="uso atual")
        self.home_disk = MetricCard("Armazenamento", detail="espaço livre")
        self.home_startup = MetricCard("Inicialização", detail="apps detectados")
        for column, card in enumerate(
            (self.home_cpu, self.home_memory, self.home_disk, self.home_startup)
        ):
            metrics.addWidget(card, 0, column)
        layout.addLayout(metrics)

        lower = QHBoxLayout()
        lower.setSpacing(14)
        insights = QGroupBox("O que merece atenção")
        insights.setObjectName("card")
        insights_layout = QVBoxLayout(insights)
        self.insights_list = QListWidget()
        self.insights_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        insights_layout.addWidget(self.insights_list)
        lower.addWidget(insights, 3)

        actions = QGroupBox("Ações rápidas")
        actions.setObjectName("card")
        actions_layout = QVBoxLayout(actions)
        actions_layout.addWidget(make_label("Comece por uma tarefa segura.", "muted"))
        analyze = QPushButton("Analisar novamente")
        analyze.setObjectName("primaryButton")
        analyze.clicked.connect(self.refresh_all)
        actions_layout.addWidget(analyze)
        cleanup = QPushButton("Ver limpeza")
        cleanup.setObjectName("secondaryButton")
        cleanup.clicked.connect(lambda: self.navigate(2))
        actions_layout.addWidget(cleanup)
        performance = QPushButton("Ver desempenho")
        performance.setObjectName("secondaryButton")
        performance.clicked.connect(lambda: self.navigate(3))
        actions_layout.addWidget(performance)
        actions_layout.addStretch(1)
        lower.addWidget(actions, 2)
        layout.addLayout(lower, 1)
        return page

    def _build_games_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        intro = QFrame()
        intro.setObjectName("heroCard")
        intro_layout = QVBoxLayout(intro)
        intro_layout.addWidget(make_label("Prepare seu PC para jogar", "heroTitle"))
        text = make_label(
            "O Flash-Lite vai detectar seus jogos, criar perfis e aplicar mudanças "
            "temporárias enquanto você joga. Tudo será restaurado ao terminar."
        )
        text.setWordWrap(True)
        intro_layout.addWidget(text)
        layout.addWidget(intro)

        empty = QGroupBox("Seus jogos")
        empty.setObjectName("card")
        empty_layout = QVBoxLayout(empty)
        empty_layout.setContentsMargins(22, 28, 22, 28)
        icon = make_label("◈", "heroScore")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(icon)
        title = make_label("Detecção de jogos será ativada em breve", "sectionTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(title)
        description = make_label(
            "A próxima etapa vai integrar Steam e outros launchers. Por enquanto, "
            "você já pode analisar o desempenho geral do computador.",
            "muted",
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        empty_layout.addWidget(description)
        layout.addWidget(empty)
        layout.addStretch(1)
        return page

    def _build_cleanup_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(13)

        info = QFrame()
        info.setObjectName("heroCard")
        info_layout = QHBoxLayout(info)
        info_layout.addWidget(
            make_label(
                "A limpeza começa com uma prévia. Arquivos duvidosos ficam desmarcados "
                "e itens confirmados vão para uma quarentena reversível.",
                "muted",
            ),
            1,
        )
        refresh = QPushButton("Atualizar análise")
        refresh.setObjectName("secondaryButton")
        refresh.clicked.connect(self.refresh_cleanup)
        info_layout.addWidget(refresh)
        layout.addWidget(info)

        summary = QHBoxLayout()
        self.cleanup_count = MetricCard("Itens encontrados", "0", "nada analisado")
        self.cleanup_size = MetricCard("Selecionados", "0 B", "baixo risco")
        summary.addWidget(self.cleanup_count)
        summary.addWidget(self.cleanup_size)
        summary.addStretch(1)
        layout.addLayout(summary)

        self.cleanup_table = QTableWidget(0, 5)
        self.cleanup_table.setHorizontalHeaderLabels(
            ["Selecionar", "Categoria", "Arquivo", "Risco", "Tamanho"]
        )
        self.cleanup_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.cleanup_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        header = self.cleanup_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.cleanup_table.itemChanged.connect(self.update_cleanup_summary)
        layout.addWidget(self.cleanup_table, 1)

        self.cleanup_empty = make_label(
            "Nenhuma regra de limpeza aplicável encontrou arquivos neste sistema.", "muted"
        )
        self.cleanup_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cleanup_empty.setWordWrap(True)
        layout.addWidget(self.cleanup_empty)

        footer = QHBoxLayout()
        self.cleanup_status = make_label("Pronto para analisar.", "muted")
        footer.addWidget(self.cleanup_status, 1)
        clean = QPushButton("Colocar selecionados em quarentena")
        clean.setObjectName("dangerButton")
        clean.clicked.connect(self.clean_selected)
        footer.addWidget(clean)
        layout.addLayout(footer)
        return page

    def _build_performance_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        metrics = QGridLayout()
        metrics.setSpacing(12)
        self.performance_cpu = MetricCard("CPU", detail="atualização automática")
        self.performance_memory = MetricCard("RAM", detail="disponível")
        self.performance_disk = MetricCard("Disco", detail="espaço livre")
        self.performance_process_count = MetricCard("Processos", detail="em execução")
        for column, card in enumerate(
            (
                self.performance_cpu,
                self.performance_memory,
                self.performance_disk,
                self.performance_process_count,
            )
        ):
            metrics.addWidget(card, 0, column)
        layout.addLayout(metrics)

        process_box = QGroupBox("Aplicativos usando mais memória")
        process_box.setObjectName("card")
        process_layout = QVBoxLayout(process_box)
        self.performance_table = QTableWidget(0, 4)
        self.performance_table.setHorizontalHeaderLabels(["Processo", "PID", "RAM", "Estado"])
        self.performance_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.performance_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        process_header = self.performance_table.horizontalHeader()
        process_header.setStretchLastSection(True)
        process_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        process_layout.addWidget(self.performance_table)
        layout.addWidget(process_box, 1)

        footer = QHBoxLayout()
        self.performance_status = make_label("Atualização automática a cada 5 segundos.", "muted")
        footer.addWidget(self.performance_status, 1)
        refresh = QPushButton("Atualizar agora")
        refresh.setObjectName("secondaryButton")
        refresh.clicked.connect(self.refresh_live_metrics)
        footer.addWidget(refresh)
        layout.addLayout(footer)
        return page

    def _build_assistant_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        intro = QFrame()
        intro.setObjectName("heroCard")
        intro_layout = QVBoxLayout(intro)
        intro_layout.addWidget(make_label("Assistente contextual", "heroTitle"))
        intro_text = make_label(
            "Faça perguntas sobre o diagnóstico atual. Esta primeira versão responde "
            "localmente e não envia seus dados para nenhum serviço externo."
        )
        intro_text.setWordWrap(True)
        intro_layout.addWidget(intro_text)
        layout.addWidget(intro)

        self.assistant_history = QTextBrowser()
        self.assistant_history.setOpenExternalLinks(False)
        self.assistant_history.setHtml(
            "<p><b>Flash-Lite:</b> Posso explicar o uso de CPU, RAM, armazenamento "
            "e o significado da limpeza.</p>"
        )
        layout.addWidget(self.assistant_history, 1)

        question_row = QHBoxLayout()
        self.assistant_input = QLineEdit()
        self.assistant_input.setPlaceholderText("Ex.: por que meu PC está usando muita RAM?")
        self.assistant_input.returnPressed.connect(self.ask_assistant)
        question_row.addWidget(self.assistant_input, 1)
        ask = QPushButton("Perguntar")
        ask.setObjectName("primaryButton")
        ask.clicked.connect(self.ask_assistant)
        question_row.addWidget(ask)
        layout.addLayout(question_row)
        return page

    def navigate(self, page_index: int) -> None:
        self.pages.setCurrentIndex(page_index)
        self.page_title.setText(self.NAV_ITEMS[page_index][1])
        subtitles = (
            "Veja rapidamente o que merece atenção no seu computador.",
            "Prepare sessões de jogo e acompanhe seus perfis.",
            "Revise arquivos antes de liberar espaço.",
            "Acompanhe os recursos que estão sendo usados agora.",
            "Entenda o diagnóstico em linguagem simples.",
        )
        self.page_subtitle.setText(subtitles[page_index])
        if page_index == 2:
            self.refresh_cleanup()
        elif page_index == 3:
            self.refresh_live_metrics()

    def refresh_all(self) -> None:
        self.current_snapshot = self.service.scan_system(persist=True)
        self.refresh_live_metrics()
        self.refresh_cleanup()

    def refresh_live_metrics(self) -> None:
        snapshot = self.service.scan_system(persist=False)
        self.current_snapshot = snapshot
        processes = self.service.top_processes(limit=10)
        self.refresh_performance(snapshot, processes)
        self.refresh_home(snapshot)

    def refresh_home(self, snapshot: SystemSnapshot) -> None:
        self.hero_score.setText(f"{snapshot.health_score}/100")
        self.hero_progress.setValue(snapshot.health_score)
        if snapshot.health_score >= 80:
            message = "Seu PC está em uma condição geral boa. Vamos procurar melhorias seguras."
        elif snapshot.health_score >= 60:
            message = "Há alguns pontos que podem ser melhorados antes de jogar."
        else:
            message = "Encontramos pontos importantes para revisar com calma."
        self.hero_message.setText(message)
        self.home_cpu.set_value(f"{snapshot.cpu_percent:.0f}%", "uso atual")
        self.home_memory.set_value(f"{snapshot.memory_percent:.0f}%", "uso atual")
        self.home_disk.set_value(f"{snapshot.disk_free_percent:.0f}%", "espaço livre")
        self.home_startup.set_value("—", "analisando inicialização")

        try:
            startup_count = len(self.service.startup_entries())
            self.home_startup.set_value(str(startup_count), "apps detectados")
        except Exception:
            self.home_startup.set_value("—", "não disponível")

        self.insights_list.clear()
        insights: list[str] = []
        if snapshot.memory_percent >= 80:
            insights.append("RAM está bastante utilizada; veja os processos que mais consomem.")
        if snapshot.disk_free_percent < 15:
            insights.append("Há pouco espaço livre no disco; revise a limpeza antes de apagar algo.")
        if snapshot.cpu_percent >= 85:
            insights.append("A CPU está ocupada agora; isso pode ser temporário.")
        if not insights:
            insights.append("Nenhum alerta importante neste momento.")
            insights.append("O melhor próximo passo é comparar o desempenho durante um jogo.")
        for text in insights:
            item = QListWidgetItem(f"•  {text}")
            item.setToolTip(text)
            self.insights_list.addItem(item)

    def refresh_performance(self, snapshot: SystemSnapshot, processes: list) -> None:
        self.performance_cpu.set_value(f"{snapshot.cpu_percent:.0f}%", "uso total")
        self.performance_memory.set_value(
            f"{snapshot.memory_percent:.0f}%",
            f"{format_bytes(snapshot.memory_available_bytes)} disponíveis",
        )
        self.performance_disk.set_value(
            f"{snapshot.disk_free_percent:.0f}%",
            f"{format_bytes(snapshot.disk_free_bytes)} livres",
        )
        self.performance_process_count.set_value(str(len(processes)), "maiores consumidores")
        self.performance_table.setRowCount(len(processes))
        for row, process in enumerate(processes):
            self.performance_table.setItem(row, 0, QTableWidgetItem(process.name))
            self.performance_table.setItem(row, 1, QTableWidgetItem(str(process.pid)))
            self.performance_table.setItem(row, 2, QTableWidgetItem(f"{process.memory_mb:.1f} MB"))
            self.performance_table.setItem(row, 3, QTableWidgetItem(process.status))
        self.performance_status.setText("Atualizado agora • sem alterar processos")

    def refresh_cleanup(self) -> None:
        try:
            self.cleanup_candidates = self.service.cleanup_preview()
        except (OSError, ValueError) as error:
            self.cleanup_candidates = []
            self.cleanup_status.setText(f"Não foi possível ler as regras: {error}")
            return

        self.cleanup_table.blockSignals(True)
        self.cleanup_table.setRowCount(len(self.cleanup_candidates))
        for row, candidate in enumerate(self.cleanup_candidates):
            checkbox = QTableWidgetItem()
            checkbox.setFlags(
                Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable
            )
            checkbox.setCheckState(
                Qt.CheckState.Checked if candidate.selected else Qt.CheckState.Unchecked
            )
            checkbox.setToolTip("A seleção será revisada antes da confirmação.")
            self.cleanup_table.setItem(row, 0, checkbox)
            self.cleanup_table.setItem(row, 1, QTableWidgetItem(candidate.category))
            file_item = QTableWidgetItem(candidate.path)
            file_item.setToolTip(candidate.explanation)
            self.cleanup_table.setItem(row, 2, file_item)
            risk_item = QTableWidgetItem(candidate.risk.label)
            risk_item.setForeground(QColor(self._risk_color(candidate.risk)))
            self.cleanup_table.setItem(row, 3, risk_item)
            self.cleanup_table.setItem(row, 4, QTableWidgetItem(format_bytes(candidate.size_bytes)))
        self.cleanup_table.blockSignals(False)
        self.cleanup_empty.setVisible(not self.cleanup_candidates)
        self.cleanup_status.setText(
            "Prévia atualizada. Nenhum arquivo foi removido."
            if self.cleanup_candidates
            else "Nenhum item aplicável foi encontrado."
        )
        self.update_cleanup_summary()

    def update_cleanup_summary(self) -> None:
        selected_size = 0
        selected_count = 0
        for row, candidate in enumerate(self.cleanup_candidates):
            item = self.cleanup_table.item(row, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                selected_count += 1
                selected_size += candidate.size_bytes
        self.cleanup_count.set_value(str(len(self.cleanup_candidates)), "itens analisados")
        self.cleanup_size.set_value(format_bytes(selected_size), f"{selected_count} selecionado(s)")

    def clean_selected(self) -> None:
        selected: list[CleanupCandidate] = []
        for row, candidate in enumerate(self.cleanup_candidates):
            item = self.cleanup_table.item(row, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                selected.append(replace(candidate, selected=True))

        if not selected:
            QMessageBox.information(
                self,
                "Nada selecionado",
                "Selecione pelo menos um item de baixo risco para continuar.",
            )
            return

        total = sum(item.size_bytes for item in selected)
        answer = QMessageBox.question(
            self,
            "Confirmar quarentena",
            f"Mover {len(selected)} item(ns), totalizando {format_bytes(total)}, "
            "para a quarentena reversível?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        cleaner = QuarantineCleaner(self.service.state_dir)
        moved = cleaner.clean(selected, confirm=True)
        self.service.database.record_action("quarantine_cleanup", {"items": moved})
        self.cleanup_status.setText(f"{len(moved)} item(ns) enviado(s) para a quarentena.")
        self.refresh_cleanup()

    def ask_assistant(self) -> None:
        question = self.assistant_input.text().strip()
        if not question:
            return
        self.assistant_history.append(f"<p><b>Você:</b> {escape(question)}</p>")
        self.assistant_history.append(f"<p><b>Flash-Lite:</b> {self._answer_question(question)}</p>")
        self.assistant_input.clear()

    def _answer_question(self, question: str) -> str:
        snapshot = self.current_snapshot or self.service.scan_system(persist=False)
        normalized = question.casefold()
        if "ram" in normalized or "memória" in normalized or "memoria" in normalized:
            return (
                f"A RAM está em {snapshot.memory_percent:.0f}% de uso. "
                "Veja a área Desempenho para identificar os aplicativos que mais consomem. "
                "Fechar processos só vale a pena quando você sabe que não precisa deles."
            )
        if "disco" in normalized or "armazenamento" in normalized or "espaço" in normalized:
            return (
                f"O armazenamento tem {snapshot.disk_free_percent:.0f}% de espaço livre. "
                "Na área Limpeza, os itens são analisados antes de qualquer ação; "
                "arquivos pessoais não devem ser selecionados automaticamente."
            )
        if "cpu" in normalized or "processador" in normalized:
            return (
                f"A CPU está em {snapshot.cpu_percent:.0f}% agora. "
                "Esse número é um retrato do momento, então vale observar durante o jogo "
                "antes de concluir que existe um gargalo."
            )
        if "limpar" in normalized or "apagar" in normalized:
            return (
                "O Flash-Lite não apaga arquivos silenciosamente. Primeiro mostra a origem, "
                "o risco e o tamanho; depois uma ação confirmada vai para a quarentena "
                "para permitir restauração."
            )
        return (
            "Ainda estou aprendendo a responder perguntas mais específicas. "
            "Tente perguntar sobre RAM, CPU, disco ou limpeza."
        )

    @staticmethod
    def _risk_color(risk: RiskLevel) -> str:
        return {
            RiskLevel.VERY_LOW: "#15803d",
            RiskLevel.LOW: "#16a34a",
            RiskLevel.MEDIUM: "#b45309",
            RiskLevel.HIGH: "#b91c1c",
        }[risk]


def run_app(service: FlashLiteService | None = None) -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow(service or FlashLiteService())
    window.show()
    return app.exec()
