import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication


def set_dock_active(active: bool):
    """
    Switch macOS activation policy.

    active=True  → show Dock icon with dot
                   (NSApplicationActivationPolicyRegular)
    active=False → hide dot, background mode
                   (NSApplicationActivationPolicyAccessory)
    """
    if sys.platform != "darwin":
        return
    try:
        from AppKit import (
            NSApplication,
            NSApplicationActivationPolicyRegular,
            NSApplicationActivationPolicyAccessory,
        )
        app = NSApplication.sharedApplication()
        if active:
            app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        else:
            app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    except Exception as e:
        print(f"[Dock] Policy switch failed: {e}")


def on_any_window_closed():
    """
    Check if any app window is still visible.
    Only go back to Accessory if all are closed.
    """
    app = QApplication.instance()
    if app is None:
        return
    any_visible = any(
        w.isVisible()
        for w in app.topLevelWidgets()
        if not w.isHidden()
        and w.__class__.__name__ != "QSystemTrayIcon"
    )
    if not any_visible:
        _schedule_dock_hide()


def _schedule_dock_hide():
    """Hide the Dock icon after a small delay to avoid flicker on window close."""
    QTimer.singleShot(150, lambda: set_dock_active(False))
