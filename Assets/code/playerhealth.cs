using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.Events;
public class playerhealth : MonoBehaviour
{
    [SerializeField] int maxHealth;
    public int currenHealth;

    public health health;

    public UnityEvent onDeath;

    public float safetime = 1f;
    float safeCD;

    public AudioClip damageSound; // Clip âm thanh khi dính đòn
    private AudioSource audioSource;
    private void OnEnable()
    {
        onDeath.AddListener(Death);
    }
    private void OnDisable()
    {
        onDeath.RemoveListener(Death);
    }
    private void Start()
    {
        audioSource = GetComponent<AudioSource>();
        currenHealth = maxHealth;
        health.Update(currenHealth,maxHealth);
    }

    public void takeDam(int dame)
    {
        if (safeCD <= 0) // Chỉ nhận sát thương khi hết thời gian an toàn
        {
            currenHealth -= dame; // Trừ sát thương vào máu

            if (damageSound != null)
            {
                audioSource.PlayOneShot(damageSound);
            }
            if (currenHealth <= 0)
            {
                currenHealth = 0; // Đảm bảo máu không âm
                onDeath.Invoke(); // Gọi sự kiện chết
            }
            safeCD = safetime; // Đặt lại thời gian an toàn
            health.Update(currenHealth, maxHealth); // Cập nhật thanh máu
        }
    }
    public void Death()
    {
        Debug.Log("Player đã chết!");

        // Gọi GameManager để xử lý thất bại, nhưng phải đảm bảo rằng hủy đối tượng player sau khi gọi GameOver
        GameManager.Instance.GameOver(false); // Gọi GameOver với tham số false để thua
        // Hủy đối tượng Player sau khi thông báo kết thúc game
        Destroy(gameObject);
    }
    private void Update()
    {
        safeCD -= Time.deltaTime;

    }


}
