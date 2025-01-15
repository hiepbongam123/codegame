using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; } // Singleton Instance

    public int requiredKills; // Số quái cần tiêu diệt để chiến thắng
    public int killCount;     // Số quái đã tiêu diệt

    //public TextMeshProUGUI gameOverText;
    public TextMeshProUGUI killCountText;

    public GameObject[] characterPrefabs; // Danh sách các nhân vật
    private GameObject currentPlayer;     // Nhân vật hiện tại
    public Transform spawnPoint;          // Điểm xuất hiện của nhân vật
    public TextMeshProUGUI gameOverText; // Thông báo chiến thắng/thất bại

    private void Awake()
    {
        // Thiết lập Singleton
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject); // Giữ GameManager khi chuyển cảnh
        }
        else
        {
            Destroy(gameObject); // Đảm bảo chỉ có một GameManager tồn tại
        }
    }

    private void Start()
    {
        if (SceneManager.GetActiveScene().name == "HomePlay")
        {
            gameOverText.gameObject.SetActive(false); // Ẩn thông báo ban đầu
            SpawnSelectedCharacter();
            UpdateKillCountUI();
        }
    }
    private void SpawnSelectedCharacter()
    {
        int selectedCharacterIndex = PlayerPrefs.GetInt("SelectedCharacterIndex", 0); // Lấy lựa chọn nhân vật
        GameObject selectedCharacterPrefab = characterPrefabs[selectedCharacterIndex];
        currentPlayer = Instantiate(selectedCharacterPrefab, spawnPoint.position, Quaternion.identity);
    }

    // Hàm này sẽ được gọi mỗi khi một kẻ thù bị tiêu diệt
    public void EnemyKilled()
    {
        killCount++;
        UpdateKillCountUI();

        if (killCount >= requiredKills)
        {
            GameOver(true); // Chiến thắng

        }
    }

    public void UpdateKillCountUI()
    {
        if (killCountText != null)
        {
            killCountText.text = $"KILL: {killCount} / {requiredKills}";
        }
    }

    public void GameOver(bool victory)
    {
        // Hiển thị thông báo khi kết thúc game
        gameOverText.gameObject.SetActive(true); // Hiện thông báo kết thúc game
        if (victory)
        {
            gameOverText.text = "VICTORY!";
        }
        if (!victory)
        {
            gameOverText.text = "DEFEAT!";
        }
        
        killCount = 0;
        Invoke("BackToMenu", 3f); // Chờ 3 giây rồi quay lại sảnh
    }

    // Hàm này sẽ được gọi khi người chơi nhấn vào nút Retry hoặc Back To Menu
    public void BackToMenu()
    {
        // Quay về màn hình chính
        SceneManager.LoadScene("HomeMain");
    }
}