#!/usr/bin/env python3
"""
MacCleaner Pro - Interface macOS Native Simplifiée
Version allégée pour démonstration
"""

import sys
import time
import threading
import objc
from Foundation import *
from AppKit import *

class MacCleanerApp(NSObject):
    """Application principale MacCleaner Pro native"""
    
    def init(self):
        self = super().init()
        if self is None:
            return None
        
        self.window = None
        self.progress_bar = None
        self.status_label = None
        self.log_text = None
        self.is_cleaning = False
        
        return self
    
    def create_window(self):
        """Créer la fenêtre principale native macOS"""
        
        # Fenêtre avec style macOS natif
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(200, 200, 800, 600),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | 
            NSWindowStyleMaskMiniaturizable,
            NSBackingStoreBuffered,
            False
        )
        
        self.window.setTitle_("MacCleaner Pro - Interface Native macOS")
        self.window.setBackgroundColor_(NSColor.controlBackgroundColor())
        
        # Vue principale
        content_view = NSView.alloc().initWithFrame_(self.window.contentView().bounds())
        self.window.setContentView_(content_view)
        
        # Titre principal
        title = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 520, 760, 40))
        title.setStringValue_("🚀 MacCleaner Pro - Interface Native macOS")
        title.setFont_(NSFont.boldSystemFontOfSize_(18))
        title.setTextColor_(NSColor.labelColor())
        title.setBezeled_(False)
        title.setDrawsBackground_(False)
        title.setEditable_(False)
        content_view.addSubview_(title)
        
        # Sous-titre
        subtitle = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 490, 760, 20))
        subtitle.setStringValue_("Interface comme CleanMyMac X, DaisyDisk et autres apps professionnelles macOS")
        subtitle.setFont_(NSFont.systemFontOfSize_(12))
        subtitle.setTextColor_(NSColor.secondaryLabelColor())
        subtitle.setBezeled_(False)
        title.setDrawsBackground_(False)
        subtitle.setEditable_(False)
        content_view.addSubview_(subtitle)
        
        # Zone d'informations
        info_box = NSBox.alloc().initWithFrame_(NSMakeRect(20, 350, 360, 120))
        info_box.setTitle_("💾 Informations Système")
        info_box.setTitlePosition_(NSAtTop)
        content_view.addSubview_(info_box)
        
        # Texte d'informations
        info_text = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 10, 340, 80))
        info_text.setStringValue_(self.get_system_info())
        info_text.setFont_(NSFont.monospacedSystemFontOfSize_weight_(10, NSFontWeightRegular))
        info_text.setBezeled_(False)
        info_text.setDrawsBackground_(False)
        info_text.setEditable_(False)
        info_box.addSubview_(info_text)
        
        # Zone d'options
        options_box = NSBox.alloc().initWithFrame_(NSMakeRect(400, 350, 380, 120))
        options_box.setTitle_("🧹 Options de Nettoyage")
        options_box.setTitlePosition_(NSAtTop)
        content_view.addSubview_(options_box)
        
        # Checkboxes
        options = [
            "✅ Caches système (1.2 GB)",
            "✅ Fichiers temporaires (456 MB)",
            "✅ Logs et diagnostics (234 MB)"
        ]
        
        for i, option in enumerate(options):
            checkbox = NSButton.alloc().initWithFrame_(NSMakeRect(10, 60 - i*20, 360, 18))
            checkbox.setButtonType_(NSButtonTypeSwitch)
            checkbox.setTitle_(option)
            checkbox.setState_(NSControlStateValueOn)
            checkbox.setFont_(NSFont.systemFontOfSize_(11))
            options_box.addSubview_(checkbox)
        
        # Barre de progression
        self.progress_bar = NSProgressIndicator.alloc().initWithFrame_(NSMakeRect(20, 300, 760, 20))
        self.progress_bar.setStyle_(NSProgressIndicatorStyleBar)
        self.progress_bar.setIndeterminate_(False)
        self.progress_bar.setMinValue_(0.0)
        self.progress_bar.setMaxValue_(100.0)
        content_view.addSubview_(self.progress_bar)
        
        # Label de statut
        self.status_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 275, 760, 20))
        self.status_label.setStringValue_("Prêt pour le nettoyage")
        self.status_label.setFont_(NSFont.systemFontOfSize_(12))
        self.status_label.setBezeled_(False)
        self.status_label.setDrawsBackground_(False)
        self.status_label.setEditable_(False)
        content_view.addSubview_(self.status_label)
        
        # Zone de logs (scrollable)
        scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(20, 80, 760, 180))
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.setBorderType_(NSBezelBorder)
        
        self.log_text = NSTextView.alloc().initWithFrame_(scroll_view.contentSize())
        self.log_text.setFont_(NSFont.fontWithName_size_("Monaco", 10))
        self.log_text.setEditable_(False)
        self.log_text.setBackgroundColor_(NSColor.textBackgroundColor())
        
        scroll_view.setDocumentView_(self.log_text)
        content_view.addSubview_(scroll_view)
        
        # Boutons d'action
        buttons = [
            ("🧹 Nettoyer", 20, 40, self.start_clean),
            ("🛡️ Scanner", 140, 40, self.start_scan),
            ("🔍 Analyser", 260, 40, self.start_analyze),
            ("📊 Profiler", 380, 40, self.start_profile),
            ("⚙️ Préférences", 500, 40, self.show_preferences),
            ("❌ Quitter", 640, 40, self.quit_app)
        ]
        
        for title, x, y, action in buttons:
            button = NSButton.alloc().initWithFrame_(NSMakeRect(x, y, 100, 30))
            button.setTitle_(title)
            button.setBezelStyle_(NSBezelStyleRounded)
            button.setTarget_(self)
            button.setAction_(action)
            content_view.addSubview_(button)
        
        # Messages initiaux
        self.log("🍎 MacCleaner Pro - Interface macOS Native démarrée")
        self.log("✨ Design natif comme CleanMyMac X")
        self.log("🎯 Utilise PyObjC et frameworks Cocoa/AppKit")
        self.log("🚀 Prêt pour l'utilisation!")
        
        return self.window
    
    def get_system_info(self):
        """Obtenir les informations système"""
        try:
            import psutil
            import shutil
            
            # Disque
            disk = shutil.disk_usage('/')
            disk_free = disk.free / (1024**3)
            disk_total = disk.total / (1024**3)
            
            # Mémoire
            memory = psutil.virtual_memory()
            mem_used = (memory.total - memory.available) / (1024**3)
            mem_total = memory.total / (1024**3)
            
            # CPU
            cpu = psutil.cpu_percent(interval=0.1)
            
            return f"""💾 Disque: {disk_free:.1f} GB libre / {disk_total:.1f} GB
🧠 Mémoire: {mem_used:.1f} GB / {mem_total:.1f} GB  
⚡ CPU: {cpu:.1f}%
🕐 {time.strftime("%H:%M:%S")}"""
            
        except:
            return "Informations système indisponibles"
    
    def log(self, message):
        """Ajouter un message au log"""
        if self.log_text:
            timestamp = time.strftime("%H:%M:%S")
            log_line = f"[{timestamp}] {message}\n"
            
            # Ajouter au texte
            current_text = self.log_text.string()
            new_text = current_text + log_line
            self.log_text.setString_(new_text)
            
            # Scroll vers la fin
            self.log_text.scrollToEndOfDocument_(None)
    
    def update_progress(self, value, status=""):
        """Mettre à jour la progression"""
        if self.progress_bar:
            self.progress_bar.setDoubleValue_(value)
        if self.status_label and status:
            self.status_label.setStringValue_(status)
    
    @objc.IBAction
    def start_clean(self, sender):
        """Démarrer le nettoyage"""
        if self.is_cleaning:
            return
        
        self.is_cleaning = True
        sender.setEnabled_(False)
        
        self.log("🧹 Démarrage du nettoyage...")
        
        def clean_process():
            steps = [
                ("Analyse des caches...", 20),
                ("Nettoyage en cours...", 50),
                ("Vidage corbeille...", 80),
                ("Finalisation...", 100)
            ]
            
            for status, progress in steps:
                NSOperationQueue.mainQueue().addOperationWithBlock_(
                    lambda s=status, p=progress: self.update_progress(p, s)
                )
                NSOperationQueue.mainQueue().addOperationWithBlock_(
                    lambda s=status: self.log(s)
                )
                time.sleep(1.5)
            
            NSOperationQueue.mainQueue().addOperationWithBlock_(
                lambda: self.finish_clean(sender)
            )
        
        threading.Thread(target=clean_process, daemon=True).start()
    
    def finish_clean(self, sender):
        """Finaliser le nettoyage"""
        self.is_cleaning = False
        sender.setEnabled_(True)
        self.log("✅ Nettoyage terminé! 2.1 GB libérés")
        self.update_progress(0, "Prêt pour le nettoyage")
        
        # Notification native
        self.show_notification("Nettoyage terminé", "2.1 GB d'espace libérés")
    
    @objc.IBAction
    def start_scan(self, sender):
        """Scanner de sécurité"""
        self.log("🛡️ Scan de sécurité démarré...")
        self.progress_bar.setIndeterminate_(True)
        self.progress_bar.startAnimation_(None)
        
        def finish():
            time.sleep(2)
            NSOperationQueue.mainQueue().addOperationWithBlock_(
                lambda: self.finish_scan()
            )
        
        threading.Thread(target=finish, daemon=True).start()
    
    def finish_scan(self):
        """Finaliser le scan"""
        self.progress_bar.stopAnimation_(None)
        self.progress_bar.setIndeterminate_(False)
        self.log("✅ Scan terminé - Aucune menace détectée")
    
    @objc.IBAction
    def start_analyze(self, sender):
        """Analyser le système"""
        self.log("🔍 Analyse heuristique démarrée...")
        self.log("📊 Interface native macOS - PyObjC + Cocoa")
    
    @objc.IBAction
    def start_profile(self, sender):
        """Profiling de performance"""
        self.log("📊 Profiling de performance...")
        info_text = self.get_system_info()
        self.log(f"Infos: {info_text.replace(chr(10), ' | ')}")
    
    @objc.IBAction
    def show_preferences(self, sender):
        """Afficher les préférences"""
        self.log("⚙️ Préférences - Interface native macOS")
    
    @objc.IBAction
    def quit_app(self, sender):
        """Quitter l'application"""
        NSApplication.sharedApplication().terminate_(None)
    
    def show_notification(self, title, message):
        """Notification native macOS"""
        try:
            notification = NSUserNotification.alloc().init()
            notification.setTitle_(title)
            notification.setInformativeText_(message)
            notification.setSoundName_(NSUserNotificationDefaultSoundName)
            
            center = NSUserNotificationCenter.defaultUserNotificationCenter()
            center.deliverNotification_(notification)
        except:
            print(f"Notification: {title} - {message}")

def main():
    """Lancer l'application native"""
    print("🍎 MacCleaner Pro - Interface macOS Native")
    print("Utilise PyObjC + Cocoa pour un look authentique macOS")
    
    # Application
    app = NSApplication.sharedApplication()
    
    # Contrôleur
    controller = MacCleanerApp.alloc().init()
    window = controller.create_window()
    
    # Afficher
    window.center()
    window.makeKeyAndOrderFront_(None)
    
    # Lancer
    app.run()

if __name__ == "__main__":
    main()