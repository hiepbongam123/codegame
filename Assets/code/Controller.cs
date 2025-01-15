using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public class Controller : MonoBehaviour
{
    playerhealth players;
    public int mindame;
    public int maxdame;
    public bool damepopup;
    public bool flash;

    health health;

    // Tham chiếu đến UI hoặc game manager để hiển thị số quái đã tiêu diệt
    public TextMeshProUGUI killCountText; // Text hiển thị số quái đã tiêu diệt
    public int requiredKills = 10; // Số quái cần tiêu diệt để chiến thắng

    private GameManager gameManager; // Tham chiếu đến GameManager để theo dõi killCount

    void Start()
    {
        health = GetComponent<health>();
        gameManager = FindFirstObjectByType<GameManager>(); // Lấy tham chiếu đến GameManager (nếu có)
    }

    void Update()
    {
        // Kiểm tra nếu player hết máu
        if (players != null && players.currenHealth <= 0)
        {
            // Player chết, chuyển đến màn hình thất bại
            GameOver(false);
        }

        // Kiểm tra nếu đã tiêu diệt đủ số quái vật
        if (gameManager != null && gameManager.killCount >= requiredKills)
        {
            // Đạt đủ số quái vật bị tiêu diệt, chuyển đến màn hình chiến thắng
            GameOver(true);
        }

        // Cập nhật số lượng quái đã tiêu diệt lên UI
        if (killCountText != null)
        {
            killCountText.text = $"KILL:{gameManager.killCount} /{gameManager.requiredKills}";
        }
    }

    public void Takedame(int dame)
    {
        health.takeDam(dame);
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        // Kiểm tra nếu va chạm với đối tượng có thẻ "Player"
        if (collision.CompareTag("Player"))
        {
            // Gán player vào biến players
            players = collision.GetComponent<playerhealth>();

            if (players != null)
            {
                int dame = Random.Range(mindame, maxdame); // Tính sát thương ngẫu nhiên
                players.takeDam(dame); // Gây sát thương cho người chơi
            }

            // Gọi hàm dameplayer liên tục khi player ở trong vùng va chạm
            InvokeRepeating("dameplayer", 0f, 1f); // Gây sát thương mỗi giây
        }
    }

    private void OnTriggerExit2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            // Hủy việc gọi dameplayer khi người chơi rời khỏi vùng va chạm
            CancelInvoke("dameplayer");
            players = null; // Đặt lại biến players
        }
    }

    void dameplayer()
    {
        if (players != null) // Kiểm tra nếu player còn trong vùng va chạm
        {
            int dame = Random.Range(mindame, maxdame); // Tính toán sát thương
            Debug.Log("Player took damage: " + dame);
            players.takeDam(dame); // Gây sát thương cho người chơi
        }
    }

    void GameOver(bool victory)
    {
        if (victory)
        {
            Debug.Log("Bạn đã chiến thắng!");
            // Chuyển đến màn hình chiến thắng hoặc sảnh chờ
        }
        else
        {
            Debug.Log("Bạn đã thua!");
            // Chuyển đến màn hình thất bại hoặc sảnh chờ
        }
    }
}
