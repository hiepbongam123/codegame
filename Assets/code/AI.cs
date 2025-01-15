using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using Pathfinding;
public class AI : MonoBehaviour
{
    public bool roaming = true;
    public float movespeed;
    public float nextWPdis;
    public Seeker seeker;
    public bool updateCont;
    Path path;
    Coroutine movecoroutine;
    bool reachDes = false;

    //bắn
    public bool isshoot =false;
    public GameObject bullet;
    public float bulletSpeed;
    public float timeBTWfire;
    private float fireCD;
    public Transform spriteHolder;

    // Tầm tấn công duy nhất
    public float attackRange = 10f; // Tầm tấn công

    public float originalSpeed;  // Thêm originalSpeed để phục hồi khi hết làm chậm
    public bool isSlowed = false; // Kiểm tra xem AI có bị làm chậm không



    private void Start()
    {
        originalSpeed = movespeed;  // Lưu lại tốc độ gốc của AI
        InvokeRepeating("CalculatePath",0f,0.5f);
        reachDes = true;
    }

    private void Update()
    {
        fireCD -= Time.deltaTime;
        if ( fireCD < 0)
        {
            fireCD = timeBTWfire;
            //shoot
            enemyFireBullet();


        }
    }

    public void ApplySlowEffect(float slowAmount, float duration)
    {
        if (!isSlowed)  // Kiểm tra xem AI có đang bị làm chậm hay không
        {
            isSlowed = true;  // Đánh dấu AI đang bị làm chậm
            movespeed *= slowAmount; // Áp dụng tốc độ làm chậm

            // Sau thời gian làm chậm, khôi phục lại tốc độ ban đầu
            StartCoroutine(RemoveSlowEffect(duration));
        }
    }

    // Coroutine để khôi phục tốc độ khi hiệu ứng làm chậm hết
    private IEnumerator RemoveSlowEffect(float duration)
    {
        yield return new WaitForSeconds(duration); // Chờ hết thời gian làm chậm
        movespeed = originalSpeed; // Khôi phục tốc độ ban đầu
        isSlowed = false;  // Đánh dấu không còn bị làm chậm
    }


    void enemyFireBullet()
    {
        Vector3 playerPos = FindFirstObjectByType<player>().transform.position;
        float distanceToPlayer = Vector3.Distance(transform.position, playerPos);

        // Chọn tốc độ viên đạn tùy theo khoảng cách
        float adjustedBulletSpeed = (distanceToPlayer < attackRange) ? bulletSpeed : bulletSpeed * 1.5f; // Tăng tốc độ nếu xa

        // Tạo viên đạn và bắn theo hướng
        var bulletTmp = Instantiate(bullet, transform.position, Quaternion.identity);
        Rigidbody2D rb = bulletTmp.GetComponent<Rigidbody2D>();
        Vector3 direction = playerPos - transform.position;

        // Bắn viên đạn
        rb.AddForce(direction.normalized * adjustedBulletSpeed, ForceMode2D.Impulse);
    }

    void CalculatePath()
    {
        Vector2 target = FindTarget();
        if (seeker.IsDone() && (reachDes || updateCont))
        {
            seeker.StartPath(transform.position, target, OnPathComplete);
        }
    }
    void OnPathComplete(Path p) 
    {
        if (p.error) return;
        path = p;
        // move to target
        MoveTarget();

    }
    void MoveTarget()
    {
        if (movecoroutine != null) StopCoroutine(movecoroutine);    
        movecoroutine = StartCoroutine(MoveTargetCoroutine());
    }

    IEnumerator MoveTargetCoroutine()
    {
        int currenWP =0;
        reachDes = false;
        while(currenWP < path.vectorPath.Count) 
        {
            Vector2 direction = ((Vector2)path.vectorPath[currenWP] - (Vector2)transform.position).normalized;

            // Lật mặt quái vật dựa trên hướng di chuyển (chỉ SpriteHolder)
            if (direction.x != 0)
            {
                spriteHolder.localScale = new Vector3(direction.x > 0 ? 1 : -1, 1, 1);
            }

            Vector2 force = direction * movespeed * Time.deltaTime;
            transform.position += (Vector3)force;

            float distance = Vector2.Distance(transform.position, path.vectorPath[currenWP]);
            if ( distance < nextWPdis) 
                currenWP++;

            yield return null;
        }
        reachDes = true;
    }

    Vector2 FindTarget()
    {
        Vector3 playerPos = FindFirstObjectByType<player>().transform.position;
        if (roaming == true)
        {
            return (Vector2)playerPos + (Random.Range(10f,50f) * new Vector2(Random.Range(-1,1), Random.Range(-1, 1)).normalized);
        }
        else
        {
            return playerPos;
        }
    }

}
