import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def euclidean_distance(point1, point2):
    """Menghitung jarak Euclidean antara dua titik."""
    return np.sqrt(np.sum((point1 - point2)**2))

def initialize_centroids(data, k, random_state=None):
    """Menginisialisasi k centroid secara acak dari titik data."""
    if random_state:
        np.random.seed(random_state)
    indices = np.random.choice(data.shape[0], k, replace=False)
    return data[indices]

def assign_to_clusters(data, centroids):
    """Menugaskan setiap titik data ke centroid terdekatnya."""
    clusters = [[] for _ in range(len(centroids))]
    for i, point in enumerate(data):
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        closest_centroid_index = np.argmin(distances)
        clusters[closest_centroid_index].append(i) 
    return clusters

def update_centroids(data, clusters):
    """Memperbarui posisi centroid berdasarkan rata-rata titik data di setiap cluster."""
    new_centroids = []
    for cluster_indices in clusters:
        if cluster_indices: # 
            cluster_points = data[cluster_indices]
            new_centroids.append(np.mean(cluster_points, axis=0))
        else: 
            
            new_centroids.append(np.random.rand(*data.shape[1])) 
    return np.array(new_centroids)

def kmeans_manual(data, k, max_iterations=100, random_state=None):
    """
    Implementasi algoritma K-Means Clustering secara manual.
    Mengembalikan list cluster (berisi indeks titik data) dan posisi centroid akhir.
    """
    centroids = initialize_centroids(data, k, random_state)
    
    for iteration in range(max_iterations):
        old_centroids = centroids.copy()
        
        clusters = assign_to_clusters(data, centroids)
        centroids = update_centroids(data, clusters)
        
        if np.allclose(old_centroids, centroids, atol=1e-6): 
            print(f"Converged at iteration {iteration + 1}")
            break
    return clusters, centroids

def calculate_wcss(data, clusters, centroids):
    """Menghitung Within-Cluster Sum of Squares (WCSS)."""
    wcss = 0
    for i, cluster_indices in enumerate(clusters):
        for point_index in cluster_indices:
            wcss += euclidean_distance(data[point_index], centroids[i])**2
    return wcss

if __name__ == "__main__":
    print("--- Memulai K-Means Clustering untuk Segmentasi Pelanggan ---")

    try:
        df = pd.read_csv('Mall_Customers.csv.xlsx')
        print("Data 'Mall_Customers.csv' berhasil dimuat.")
    except FileNotFoundError:
        print("Error: File 'Mall_Customers.csv' tidak ditemukan. Pastikan file ada di direktori yang sama.")
        exit()

    X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values
    print(f"Jumlah data pelanggan: {X.shape[0]}")
    print(f"Fitur yang digunakan: Annual Income (k$), Spending Score (1-100)")

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    print("Data berhasil dinormalisasi.")

    print("\n--- Menjalankan Elbow Method untuk menemukan K optimal ---")
    wcss_values = []
    k_range = range(1, 11) 

    for k in k_range:
        clusters, centroids = kmeans_manual(X_scaled, k, random_state=42)
        wcss_values.append(calculate_wcss(X_scaled, clusters, centroids))

    plt.figure(figsize=(8, 5))
    plt.plot(k_range, wcss_values, marker='o', linestyle='--')
    plt.title('Elbow Method untuk K-Means Clustering')
    plt.xlabel('Jumlah Klaster (K)')
    plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
    plt.grid(True)
    plt.xticks(k_range)
    plt.savefig('elbow_method.png')
    plt.show()
    print("Plot Elbow Method disimpan sebagai 'elbow_method.png'.")
    print("Lihat plot untuk menentukan nilai K yang optimal (cari titik 'siku').")
    print("Berdasarkan pengalaman, nilai K=5 sering menjadi 'siku' yang baik untuk dataset ini.")

    optimal_k = 5
    print(f"\n--- Menjalankan K-Means dengan K optimal = {optimal_k} ---")
    final_clusters, final_centroids = kmeans_manual(X_scaled, optimal_k, random_state=42) 

    print("\n--- Visualisasi Hasil Klastering ---")
    plt.figure(figsize=(10, 7))
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'purple', 'orange', 'brown', 'pink'] 

    for i, cluster_indices in enumerate(final_clusters):
        cluster_points = X_scaled[cluster_indices]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                    s=50, color=colors[i % len(colors)],
                    label=f'Klaster {i+1}')

    plt.scatter(final_centroids[:, 0], final_centroids[:, 1],
                marker='X', s=200, color='black', edgecolor='white', linewidth=1.5,
                label='Centroid Klaster')

    plt.title(f'Hasil K-Means Clustering (K={optimal_k}) untuk Segmentasi Pelanggan')
    plt.xlabel('Pendapatan Tahunan (Normalized)')
    plt.ylabel('Skor Pengeluaran (Normalized)')
    plt.legend()
    plt.grid(True)
    plt.savefig('kmeans_clustering_result.png') 
    plt.show()
    print("Plot hasil K-Means Clustering disimpan sebagai 'kmeans_clustering_result.png'.")
    print("\nProses K-Means Clustering Selesai.")