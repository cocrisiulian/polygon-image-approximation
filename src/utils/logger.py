"""
Logger personalizat pentru separarea output-urilor SA și GA.
"""

import sys
import os
from datetime import datetime
from typing import Optional


class AlgorithmLogger:
    """Logger care scrie în fișiere separate pentru SA și GA."""
    
    def __init__(self, log_dir: str = "results/logs"):
        """
        Inițializează logger-ul.
        
        Args:
            log_dir: Directorul pentru log-uri
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Creem timestamp pentru sesiune
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Fișiere de log
        self.sa_log_path = os.path.join(log_dir, f"SA_{timestamp}.log")
        self.ga_log_path = os.path.join(log_dir, f"GA_{timestamp}.log")
        self.combined_log_path = os.path.join(log_dir, f"Combined_{timestamp}.log")
        
        # Handlers
        self.sa_file = None
        self.ga_file = None
        self.combined_file = None
        
        self._open_files()
    
    def _open_files(self):
        """Deschide fișierele de log."""
        self.sa_file = open(self.sa_log_path, 'w', encoding='utf-8')
        self.ga_file = open(self.ga_log_path, 'w', encoding='utf-8')
        self.combined_file = open(self.combined_log_path, 'w', encoding='utf-8')
        
        # Scrie header
        header = f"=== Log generat la {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n"
        self.sa_file.write(header)
        self.ga_file.write(header)
        self.combined_file.write(header)
    
    def log_sa(self, message: str):
        """
        Loghează mesaj pentru SA.
        
        Args:
            message: Mesajul de logat
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        if self.sa_file:
            self.sa_file.write(formatted_msg)
            self.sa_file.flush()
        
        if self.combined_file:
            self.combined_file.write(f"[SA] {formatted_msg}")
            self.combined_file.flush()
    
    def log_ga(self, message: str):
        """
        Loghează mesaj pentru GA.
        
        Args:
            message: Mesajul de logat
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        if self.ga_file:
            self.ga_file.write(formatted_msg)
            self.ga_file.flush()
        
        if self.combined_file:
            self.combined_file.write(f"[GA] {formatted_msg}")
            self.combined_file.flush()
    
    def log_general(self, message: str):
        """
        Loghează mesaj general.
        
        Args:
            message: Mesajul de logat
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        if self.combined_file:
            self.combined_file.write(formatted_msg)
            self.combined_file.flush()
    
    def get_log_paths(self) -> dict:
        """Returnează căile către fișierele de log."""
        return {
            'sa': self.sa_log_path,
            'ga': self.ga_log_path,
            'combined': self.combined_log_path
        }
    
    def close(self):
        """Închide toate fișierele de log."""
        if self.sa_file:
            self.sa_file.close()
        if self.ga_file:
            self.ga_file.close()
        if self.combined_file:
            self.combined_file.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class LogCapture:
    """Capturează stdout și îl redirecționează către logger."""
    
    def __init__(self, logger: AlgorithmLogger, algorithm: str):
        """
        Inițializează captura.
        
        Args:
            logger: Logger-ul unde să scrie
            algorithm: 'sa' sau 'ga'
        """
        self.logger = logger
        self.algorithm = algorithm
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def write(self, message: str):
        """Scrie mesajul."""
        if message.strip():  # Doar dacă nu e gol
            if self.algorithm == 'sa':
                self.logger.log_sa(message.strip())
            elif self.algorithm == 'ga':
                self.logger.log_ga(message.strip())
            
            # Scrie și în stdout original
            self.original_stdout.write(message)
    
    def flush(self):
        """Flush output."""
        self.original_stdout.flush()
    
    def __enter__(self):
        """Activează captura."""
        sys.stdout = self
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Dezactivează captura."""
        sys.stdout = self.original_stdout
