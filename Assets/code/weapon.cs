using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class weapon : MonoBehaviour
{
    public GameObject bullet; // Prefab viên đạn
    public Transform firePos; // Vị trí bắn
    public bool isAutoShooting = false; // Bật/Tắt chế độ tự động bắn
    public float TimeBtwFire = 0.2f; // Thời gian giữa các lần bắn
    public float bulletForce; // Lực bắn

    private float timeBtwFire;

    public enum FireMode { Single, Shotgun, Laser, Homing } // Các kiểu bắn
    public FireMode fireMode = FireMode.Single; // Kiểu bắn hiện tại

    public int shotgunBulletCount = 5; // Số đạn trong một lần bắn shotgun
    public float shotgunSpreadAngle = 15f; // Góc lệch giữa các viên đạn shotgun

    // Update is called once per frame
    void Update()
    {
        RotateGun();

        // Tự động bắn nếu chế độ tự động bắn được bật
        if (isAutoShooting && timeBtwFire <= 0)
        {
            FireBullet();
        }

        // Đếm ngược thời gian giữa các lần bắn
        timeBtwFire -= Time.deltaTime;

        // Kiểm tra chuột để bật/tắt chế độ tự động bắn (Tùy chỉnh nếu cần)
        if (Input.GetKeyDown(KeyCode.F)) // Nhấn phím F để bật/tắt tự động bắn
        {
            isAutoShooting = !isAutoShooting;
        }

        if (Input.GetMouseButton(0) && timeBtwFire < 0)
        {
            FireBullet();
        }
    }

    void RotateGun()
    {
        Vector3 mousePos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        Vector2 lookDir = mousePos - transform.position;
        float angle = Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg;

        Quaternion rotation = Quaternion.Euler(0, 0, angle);
        transform.rotation = rotation;

        if (transform.eulerAngles.z > 90 && transform.eulerAngles.z < 270)
            transform.localScale = new Vector3(1, -1, 0);
        else
            transform.localScale = new Vector3(1, 1, 0);
    }

    void FireBullet()
    {
        timeBtwFire = TimeBtwFire;

        switch (fireMode)
        {
            case FireMode.Single:
                FireSingleBullet();
                break;

            case FireMode.Shotgun:
                FireShotgun();
                break;

            case FireMode.Laser:
                FireLaser();
                break;

            case FireMode.Homing:
                FireHomingBullet();
                break;
        }
    }

    void FireSingleBullet()
    {
        GameObject bulletTmp = Instantiate(bullet, firePos.position, firePos.rotation);
        Rigidbody2D rd = bulletTmp.GetComponent<Rigidbody2D>();
        rd.AddForce(firePos.right * bulletForce, ForceMode2D.Impulse);
    }

    void FireShotgun()
    {
        float startAngle = -shotgunSpreadAngle * (shotgunBulletCount - 1) / 2;
        for (int i = 0; i < shotgunBulletCount; i++)
        {
            float angle = startAngle + i * shotgunSpreadAngle;
            Quaternion rotation = Quaternion.Euler(0, 0, firePos.eulerAngles.z + angle);

            GameObject bulletTmp = Instantiate(bullet, firePos.position, rotation);
            Rigidbody2D rd = bulletTmp.GetComponent<Rigidbody2D>();
            rd.AddForce(bulletTmp.transform.right * bulletForce, ForceMode2D.Impulse);
        }
    }

    void FireLaser()
    {
        GameObject laserTmp = Instantiate(bullet, firePos.position, firePos.rotation);

        // Điều chỉnh kích thước của tia laze
        float laserLength = 10f; // Chiều dài của tia laze
        float laserWidth = 0.2f; // Độ dày của tia laze
        laserTmp.transform.localScale = new Vector3(laserLength, laserWidth, 1);

        // Di chuyển tia laze về phía trước súng (firePos)
        Vector3 offset = firePos.right * laserLength / 2; // Di chuyển nửa chiều dài về phía trước
        laserTmp.transform.position += (offset * 10);
    }

    void FireHomingBullet()
    {
        GameObject bulletTmp = Instantiate(bullet, firePos.position, firePos.rotation);
        // Hành vi tự tìm mục tiêu sẽ được xử lý trong script của đạn
    }
}
