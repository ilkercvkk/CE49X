# bitti.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from src.data_input import DataInput
from src.calculations import LCACalculator
from src.visualization import LCAVisualizer

def main():
    """
    Ana LCA analiz fonksiyonu.
    Veriyi yükler, hesaplamaları yapar ve çıktıları kaydeder.
    """
    # --- 1. Çıktı Klasörlerini Oluşturma ---
    # Bu klasörlerin proje ana dizininde olduğundan emin olun
    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('outputs/data', exist_ok=True)

    # --- 2. Veri Yükleme ---
    print("Veri yükleniyor...")
    data_input = DataInput()
    # Dosya yollarının, script'in ana klasörden çalıştırıldığı varsayılarak düzeltildiğine dikkat edin
    product_data = data_input.read_data('data/raw/sample_data.csv')
    impact_factors = data_input.read_impact_factors('data/raw/impact_factors.json')
    print("Veri başarıyla yüklendi.")
    print("Product Data Shape:", product_data.shape)

    # --- 3. Hesaplama ---
    print("\nHesaplamalar yapılıyor...")
    # Not: Bu kod, LCACalculator'ın __init__ metodunun güncellenmiş halini bekler.
    # Eğer güncellemediyseniz, aşağıdaki satırı eski haliyle değiştirmeniz gerekebilir.
    # Eski: calculator = LCACalculator(impact_factors_path='data/raw/impact_factors.json')
    calculator = LCACalculator(impact_factors_path='data/raw/impact_factors.json') 
    
    impacts = calculator.calculate_impacts(product_data)
    total_impacts = calculator.calculate_total_impacts(impacts)
    
    # Hesaplanan verileri CSV olarak kaydet
    impacts.to_csv('outputs/data/all_impacts_by_stage.csv', index=False)
    total_impacts.to_csv('outputs/data/total_impacts_by_product.csv', index=False)
    print("Hesaplamalar yapıldı ve sonuçlar 'outputs/data' klasörüne kaydedildi.")
    print("\nTotal Impacts by Product:")
    print(total_impacts.head())

    # --- 4. Görselleştirme ve Kaydetme ---
    visualizer = LCAVisualizer()
    
    print("\nGörseller oluşturuluyor ve 'outputs/figures' klasörüne kaydediliyor...")
    
    # Karbon etkisi dağılımı
    fig1 = visualizer.plot_impact_breakdown(impacts, 'carbon_impact', 'material_type', title="Karbon Etkisi Dağılımı (Malzeme Türüne Göre)")
    fig1.savefig('outputs/figures/carbon_breakdown_by_material.png')
    plt.close(fig1)

    # P001 için yaşam döngüsü etkileri
    fig2 = visualizer.plot_life_cycle_impacts(impacts, 'P001')
    fig2.suptitle('P001 Ürünü İçin Yaşam Döngüsü Etkileri', fontsize=16)
    fig2.savefig('outputs/figures/lifecycle_impacts_P001.png')
    plt.close(fig2)

    # Ürün Karşılaştırma
    fig3 = visualizer.plot_product_comparison(impacts, ['P001', 'P002'])
    fig3.savefig('outputs/figures/comparison_P001_vs_P002.png')
    plt.close(fig3)

    # P001 için ömür sonu yönetimi
    fig4 = visualizer.plot_end_of_life_breakdown(impacts, 'P001')
    fig4.savefig('outputs/figures/end_of_life_P001.png')
    plt.close(fig4)

    # Etki korelasyonu
    fig5 = visualizer.plot_impact_correlation(impacts)
    fig5.savefig('outputs/figures/impact_correlations.png')
    plt.close(fig5)
    
    print("\nAnaliz tamamlandı!")

main()