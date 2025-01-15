using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class healthEnemy : MonoBehaviour
{
    public int maxHealth = 100; // Máu tối đa
    private int currentHealth;  // Máu hiện tại

    private health healthUI; // Tham chiếu đến script health để cập nhật giao diện
    public Image fillBar;  // Thanh máu (Image)
    public TextMeshProUGUI value;  // Text hiển thị số máu

    public AudioClip damageSound; // Clip âm thanh khi dính đòn
    private AudioSource audioSource;
    private GameManager gameManager;

    private void Start()
    {
        audioSource = GetComponent<AudioSource>();
        currentHealth = maxHealth;
        healthUI = GetComponentInChildren<health>(); // Tìm script health trong các thành phần con
        UpdateHealthUI();
        gameManager = FindFirstObjectByType<GameManager>();
    }

    public void TakeDamage(int damage)
    {
        // Logic trừ máu
        currentHealth -= damage;

        // Phát âm thanh dính đòn
        if (damageSound != null)
        {
            audioSource.PlayOneShot(damageSound);
        }

        // Kiểm tra máu về 0
        if (currentHealth <= 0)
        {
            Die();
        }
    }
    //void Start()
    //{
    //    currentHealth = maxHealth;
    //    healthUI = GetComponentInChildren<health>(); // Tìm script health trong các thành phần con
    //    UpdateHealthUI();
    //}

    public void TakeDam(int damage)
    {
        currentHealth -= damage; // Giảm máu
        currentHealth = Mathf.Clamp(currentHealth, 0, maxHealth); // Đảm bảo máu không âm
        UpdateHealthUI();

        if (currentHealth <= 0)
        {
            Die(); // Gọi hàm khi quái vật chết
        }
    }

    void UpdateHealthUI()
    {
        if (healthUI != null)
        {
            healthUI.Update(currentHealth, maxHealth); // Gọi hàm Update trong script health
        }
    }

    void Die()
    {
        // Logic khi quái chết
        Debug.Log($"{gameObject.name} đã chết!");

        // Gửi thông báo về GameManager
        GameManager gameManager = FindFirstObjectByType<GameManager>();
        if (gameManager != null)
        {
            gameManager.EnemyKilled();
        }

        Destroy(gameObject); // Xóa quái khỏi game
    }
}
