# 1. Launch TUI
hermes --tui &
TUI_PID=$(pgrep -f 'ui-tui/dist/entry' | head -1)