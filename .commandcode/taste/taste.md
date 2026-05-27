# UI Layout
- In Settings dialog, make API key input full width by removing trailing QSpacerItem in its QHBoxLayout. Confidence: 0.75
- Model dropdown and "Test Connection" button go in a single QHBoxLayout row with stretch factors (dropdown 3, button 1) for ~75/25 split. Confidence: 0.75
- Use setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) on widgets that need to stretch to full width in a layout. Confidence: 0.70
- Add placeholder text via setPlaceholderText() to input fields and combo boxes for better UX. Confidence: 0.70

# PySide6
- Always import Signal from PySide6.QtCore when defining custom signals in widget classes. Confidence: 0.70

# Architecture
- Instant file detection (FSWatcher) must skip rules that have time-based conditions (age, date, modified, created, days, weeks, months) — those rules are handled exclusively by the scheduled timer. Confidence: 0.80
- Before processing any file, verify it is fully written using file_guard checks: partial extensions, size stability, file locking, and mtime stability. Confidence: 0.75

# Git
- Use gitmoji in commit messages. Confidence: 0.70

# Workflow
- After implementing changes, perform end-to-end verification and check for dead code before committing. Confidence: 0.75

# UI Styling
- Rules window table should have alternating two-tone row colors for the entire section. Confidence: 0.70
