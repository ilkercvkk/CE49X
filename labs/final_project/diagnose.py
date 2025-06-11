import sys
import os

print("--- Python Teşhis Raporu ---")
print(f"Kullanılan Python Yorumlayıcısı: {sys.executable}")
print(f"Mevcut Çalışma Klasörü: {os.getcwd()}")
print("\n--- Python'un Modül Arama Yolları (sys.path) ---")
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")
print("--- Rapor Sonu ---")