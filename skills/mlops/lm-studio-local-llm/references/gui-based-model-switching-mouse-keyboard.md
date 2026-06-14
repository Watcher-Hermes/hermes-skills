## GUI-Based Model Switching (Mouse/Keyboard)

When using mouse/keyboard to switch models in LM Studio's GUI window:

### Finding the LM Studio Window

LM Studio is an Electron app (`Chrome_WidgetWin_1`). UIA sees it as `Pane`, not `Window`:

```bash