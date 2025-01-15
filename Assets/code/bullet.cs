using System.Collections;
using UnityEngine;

public class bullet : MonoBehaviour
{
    public int mindame; // Sát thương tối thiểu
    public int maxdame; // Sát thương tối đa
    public bool goodsizebulet; // Đạn bắn quái (true) hoặc người chơi (false)

    public GameObject damePopupPrefab; // Prefab hiển thị số sát thương

    public AudioClip shootSound; // Clip âm thanh tiếng bắn
    private AudioSource audioSource;

    public bool isHoming; // Đạn tự tìm mục tiêu
    public float searchRadius = 10f;
    public float homingSpeed = 5f; // Tốc độ đạn tự tìm mục tiêu
    private Transform target; // Mục tiêu của đạn
    public bool isLaser; // Đạn là tia laze hay không
    public bool rotateInFlight; // Đạn xoay hướng khi bay
    public float rotationSpeed = 200f; // Tốc độ xoay của đạn

    public bool isOrbit; // Đạn xoay quanh nhân vật
    private Transform player;
    public float orbitRadius = 2f;
    public float orbitSpeed = 100f;

    public float slowAmount = 1f; // Tỉ lệ giảm tốc độ (ví dụ: 50%)
    public float slowDuration = 0f; // Thời gian hiệu ứng làm chậm


    private void Start()
    {
        audioSource = GetComponent<AudioSource>();
        FindNearestTarget();

        // Tự động tìm Player bằng tag
        if (player == null)
        {
            GameObject playerObject = GameObject.FindWithTag("Player");
            if (playerObject != null)
            {
                player = playerObject.transform;
            }
            else
            {
                Debug.LogError("Không tìm thấy đối tượng với tag 'Player'.");
            }
        }

        if (audioSource != null)
        {
            audioSource.volume = 0.3f;
            Shoot();
        }
    }

    private void Update()
    {
        if (isHoming && target != null)
        {
            // Tìm hướng tới mục tiêu
            Vector2 direction = (target.position - transform.position).normalized;
            transform.position = Vector2.MoveTowards(transform.position, target.position, homingSpeed * Time.deltaTime);
            RotateTowards(direction);
        }

        if (rotateInFlight)
        {
            // Đạn tự xoay khi bay
            transform.Rotate(Vector3.forward * rotationSpeed * Time.deltaTime);
        }
        if (isOrbit && player != null)
        {
            OrbitAroundPlayer();
        }


    }

    private void Shoot()
    {
        // Phát âm thanh bắn đạn
        if (shootSound != null)
        {
            audioSource.PlayOneShot(shootSound);
        }

    }

    private void RotateTowards(Vector2 direction)
    {
        float angle = Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg;
        transform.rotation = Quaternion.Euler(0, 0, angle);
    }

    private void OrbitAroundPlayer()
    {
        transform.RotateAround(player.position, Vector3.forward, orbitSpeed * Time.deltaTime);
        Vector3 offset = (transform.position - player.position).normalized * orbitRadius;
        transform.position = player.position + offset;
    }
    private void FindNearestTarget()
    {
        Collider2D[] hits = Physics2D.OverlapCircleAll(transform.position, searchRadius);

        float closestDistance = Mathf.Infinity;
        Transform closestTarget = null;

        foreach (var hit in hits)
        {
            if (hit.CompareTag("Enemy"))
            {
                float distance = Vector2.Distance(transform.position, hit.transform.position);
                if (distance < closestDistance)
                {
                    closestDistance = distance;
                    closestTarget = hit.transform;
                }
            }
        }

        if (closestTarget != null)
        {
            target = closestTarget;
            Debug.Log("Found target: " + target.name); // Debug xem đã tìm thấy mục tiêu chưa
        }
        else
        {
            Debug.Log("No target found."); // Nếu không tìm thấy mục tiêu
        }
    }

    private void ApplySlowEffect(GameObject target)
    {
        var enemyMovement = target.GetComponent<AI>(); // Thay thế bằng script di chuyển của kẻ địch
        if (enemyMovement != null)
        {
            StartCoroutine(ApplySlowToEnemy(enemyMovement));
        }
    }

    private IEnumerator ApplySlowToEnemy(AI enemyMovement)
    {
        float originalSpeed = enemyMovement.movespeed;
        enemyMovement.movespeed *= slowAmount; // Giảm tốc độ di chuyển

        yield return new WaitForSeconds(slowDuration); // Chờ trong thời gian hiệu ứng làm chậm

        enemyMovement.movespeed = originalSpeed; // Khôi phục tốc độ ban đầu
    }


    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player") && !goodsizebulet)
        {
            int dame = Random.Range(mindame, maxdame);
            var playerHealth = collision.GetComponent<playerhealth>();
            if (playerHealth != null)
            {
                playerHealth.takeDam(dame);
                ShowDamePopup(collision.transform.position, dame);

            }

            if (!isLaser && !isOrbit) Destroy(gameObject);
        }
        else if (collision.CompareTag("Enemy") && goodsizebulet)
        {
            int dame = Random.Range(mindame, maxdame);
            var enemyController = collision.GetComponent<healthEnemy>();
            if (enemyController != null)
            {
                enemyController.TakeDam(dame);
                ShowDamePopup(collision.transform.position, dame);


                enemyController.TakeDam(dame); // Cập nhật sát thương
            }
            // Áp dụng hiệu ứng làm chậm cho người chơi
            ApplySlowEffect(collision.gameObject);
            if (!isLaser && !isOrbit) Destroy(gameObject);
        }
    }


    private void ShowDamePopup(Vector3 position, int dame)
    {
        if (damePopupPrefab != null)
        {
            GameObject popup = Instantiate(damePopupPrefab, position, Quaternion.identity);
            TMPro.TextMeshProUGUI text = popup.GetComponentInChildren<TMPro.TextMeshProUGUI>();
            if (text != null)
            {
                text.text = dame.ToString();
            }
            Destroy(popup, 0.7f);
        }
    }
}