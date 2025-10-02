from tkinter import ttk

IOS_COLORS = {
    'accent': '#007AFF',
    'bg_dark': '#1C1C1E',
    'bg_light': '#F2F2F7',
    'panel': '#2C2C2E',
    'panel_light': '#FFFFFF',
    'border': '#3A3A3C',
    'danger': '#FF3B30',
    'warning': '#FF9500',
    'success': '#34C759',
    'text_primary_dark': '#FFFFFF',
    'text_primary_light': '#000000'
}

class ThemeManager:
    def __init__(self, root, dark=True):
        self.root = root
        self.dark = dark

    def apply(self):
        style = ttk.Style()
        # Base theme
        style.theme_use('clam')
        if self.dark:
            bg = IOS_COLORS['bg_dark']
            panel = IOS_COLORS['panel']
            fg = IOS_COLORS['text_primary_dark']
        else:
            bg = IOS_COLORS['bg_light']
            panel = IOS_COLORS['panel_light']
            fg = IOS_COLORS['text_primary_light']
        accent = IOS_COLORS['accent']

        self.root.configure(bg=bg)
        style.configure('TFrame', background=bg)
        style.configure('Card.TLabelframe', background=panel, foreground=fg, bordercolor=IOS_COLORS['border'])
        style.configure('Card.TLabelframe.Label', background=panel, foreground=fg, font=('SF Pro Text', 11, 'bold'))
        style.configure('Accent.TButton', background=accent, foreground='white', focusthickness=3, focuscolor=accent)
        style.map('Accent.TButton', background=[('active', accent), ('pressed', accent)])
        style.configure('TLabel', background=bg, foreground=fg, font=('SF Pro Text', 11))
        style.configure('Status.TLabel', background=panel, foreground=accent, font=('SF Pro Text', 10, 'bold'))
        style.configure('Danger.TLabel', foreground=IOS_COLORS['danger'], background=panel)
        style.configure('Warning.TLabel', foreground=IOS_COLORS['warning'], background=panel)
        style.configure('Success.TLabel', foreground=IOS_COLORS['success'], background=panel)
        style.configure('TCheckbutton', background=panel, foreground=fg, font=('SF Pro Text', 10))
        style.configure('TProgressbar', background=accent, troughcolor=panel, bordercolor=panel, lightcolor=accent, darkcolor=accent)
        
        # Scrollbar minimaliste
        style.element_create('plain.border', 'from', 'clam')
        style.layout('Vertical.TScrollbar', [
            ('Vertical.Scrollbar.trough', {'children': [
                ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})
            ], 'sticky': 'ns'})
        ])
        style.configure('Vertical.TScrollbar', background=panel, troughcolor=panel, bordercolor=panel, lightcolor=panel, darkcolor=panel, arrowcolor=fg)
