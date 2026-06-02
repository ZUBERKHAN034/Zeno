import subprocess
import os
import sys
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QListWidgetItem


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


def reveal_in_finder(path: str):
    """
    Reveal a file or folder in Finder with it selected and highlighted.
    Falls back gracefully if the path no longer exists.
    """
    if sys.platform != "darwin":
        return

    path = os.path.expanduser(path)
    p = Path(path)

    if not p.exists():
        parent = p.parent
        if parent.exists():
            subprocess.run(["open", str(parent)], check=False)
        else:
            show_not_found_alert(path)
        return

    escaped = path.replace('"', '\\"')
    script = f'''
        tell application "Finder"
            activate
            reveal POSIX file "{escaped}"
        end tell
    '''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        subprocess.run(["open", "-R", path], check=False)


def show_not_found_alert(path: str):
    """Show a message if file no longer exists at the expected path."""
    msg = QMessageBox()
    msg.setWindowTitle("File Not Found")
    msg.setText(
        f"The file could not be found at its expected location:\n\n"
        f"{path}\n\n"
        f"It may have been moved or deleted."
    )
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.exec()


def handle_notification_item_clicked(item: QListWidgetItem):
    """
    Handle click on a notification list item — reveal the file in Finder.
    Handles delete/trash actions with appropriate fallback.
    """
    path = item.data(Qt.ItemDataRole.UserRole)
    action = item.data(Qt.ItemDataRole.UserRole + 1)
    dryrun = item.data(Qt.ItemDataRole.UserRole + 2)

    if not path:
        return

    if action == "delete":
        if dryrun:
            reveal_in_finder(path)
        else:
            QMessageBox.information(
                None,
                "File Deleted",
                f"This file was permanently deleted:\n{path}",
            )
        return

    if action == "trash":
        if dryrun:
            reveal_in_finder(path)
        else:
            trash_path = os.path.expanduser("~/.Trash")
            if os.path.isdir(trash_path):
                subprocess.run(["open", trash_path], check=False)
            else:
                show_not_found_alert(path)
        return

    reveal_in_finder(path)
