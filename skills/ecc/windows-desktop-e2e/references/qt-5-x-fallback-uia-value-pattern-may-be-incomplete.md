# Qt 5.x fallback: UIA Value Pattern may be incomplete
            import sys, pywinauto.keyboard as kb
            print(f"[windows-desktop-e2e] set_edit_text failed ({e}), using keyboard fallback", file=sys.stderr)
            ctrl.click_input()
            kb.send_keys("^a")
            kb.send_keys(text, with_spaces=True)

    def get_text(self, spec):
        ctrl = spec.wrapper_object()
        for attr in ("window_text", "get_value"):
            try:
                v = getattr(ctrl, attr)()
                if v:
                    return v
            except Exception:
                pass
        return ""