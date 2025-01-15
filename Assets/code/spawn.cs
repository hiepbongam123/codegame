using UnityEngine;

public class spawn : MonoBehaviour
{
    public GameObject[] enemyPrefabs; // Mảng các prefab quái vật
    public Vector2 spawnAreaMin; // Góc dưới bên trái của vùng spawn
    public Vector2 spawnAreaMax; // Góc trên bên phải của vùng spawn
    public float spawnInterval = 5f; // Thời gian giữa các lần spawn

    private void Start()
    {
        InvokeRepeating("SpawnEnemy", 0f, spawnInterval); // Gọi phương thức SpawnEnemy định kỳ
    }

    void SpawnEnemy()
    {
        // Chọn một enemy prefab ngẫu nhiên
        int randomIndex = Random.Range(0, enemyPrefabs.Length);
        GameObject selectedEnemy = enemyPrefabs[randomIndex];

        // Chọn vị trí spawn ngẫu nhiên trong phạm vi
        float spawnX = Random.Range(spawnAreaMin.x, spawnAreaMax.x);
        float spawnY = Random.Range(spawnAreaMin.y, spawnAreaMax.y);
        Vector3 spawnPosition = new Vector3(spawnX, spawnY, 0f); // Nếu 2D, Z = 0

        // Spawn enemy tại vị trí ngẫu nhiên
        Instantiate(selectedEnemy, spawnPosition, Quaternion.identity);
    }
}
