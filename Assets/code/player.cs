using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class player : MonoBehaviour
{
    public int characterID;      // ID của nhân vật
    public float movespeed = 5f;

    public float rollBust = 2f;

    private float rollTime;
    public float RollTime;
    bool rollOnce = false;

    private Rigidbody2D rb;
    public Animator animator;

    public SpriteRenderer characterSR;

    public Vector3 moveInput;
    public GameObject ghosteff;
    public float delayS;
    private Coroutine dashcoroutine;

    public AudioClip footstepSound; // Clip âm thanh bước chân
    private AudioSource audioSource;
    public AudioClip rollSound; // Clip âm thanh roll
    public float timeroll; // Thời gian roll
    private float rollCD = 5f; // Thời gian hồi chiêu cho roll
    private float currentCDroll = 0f; // Biến để theo dõi thời gian hồi chiêu hiện tại
    private int rollCharges = 1; // Số lần roll có thể thực hiện, ban đầu 1 lần
    private void Start()
    {
        animator = GetComponent<Animator>();
        audioSource = GetComponent<AudioSource>();

        if (audioSource == null)
        {
            Debug.LogError("No AudioSource component found on player. Adding one.");
            audioSource = gameObject.AddComponent<AudioSource>();  // Tự động thêm AudioSource nếu chưa có
        }
        audioSource.loop = true; // Phát lặp âm thanh bước chân
    }

    private void Update()
    {
        moveInput.x = Input.GetAxis("Horizontal");
        moveInput.y = Input.GetAxis("Vertical");
        transform.position += moveInput * movespeed * Time.deltaTime;

        animator.SetFloat("speed", moveInput.sqrMagnitude);

        if (Input.GetKeyDown(KeyCode.Space) && rollTime <= 0 && rollOnce == false && currentCDroll <= 0 && rollCharges > 0)
        {
            animator.SetBool("roll", true);
            movespeed += rollBust;
            rollTime = RollTime;
            rollOnce = true;
            rollCharges--; // Giảm số lần roll có thể sử dụng
            Startdasheff();
            // Phát âm thanh khi bắt đầu roll
            if (rollSound != null)
            {
                audioSource.volume = 0.8f; // Giảm âm lượng âm thanh roll xuống 70%
                audioSource.PlayOneShot(rollSound);
            }
            currentCDroll = rollCD; // Thiết lập lại cooldown
        }

        if (rollTime <= 0 && rollOnce == true)
        {
            animator.SetBool("roll", false);
            movespeed -= rollBust;
            rollOnce = false;
            Stopdasheff();
        }
        else
        {
            rollTime -= Time.deltaTime;
        }
        // Cập nhật cooldown
        if (currentCDroll > 0)
        {
            currentCDroll -= Time.deltaTime;
        }
        // Tích lũy lại roll khi cooldown hoàn thành và có ít nhất 1 lần roll
        if (currentCDroll <= 0 && rollCharges == 0)
        {
            rollCharges = 1; // Tích lũy thêm 1 lần roll
        }

        if (moveInput.x != 0)
        {
            if (moveInput.x > 0)
            {
                characterSR.transform.localScale = new Vector3(1, 1, 0);
            }
            else
            {
                characterSR.transform.localScale = new Vector3(-1, 1, 0);
            }

        }
        // Kiểm tra di chuyển
        if (moveInput.sqrMagnitude > 0  && !audioSource.isPlaying)
        {
            // Phát âm thanh bước chân chỉ khi người chơi di chuyển
            if (footstepSound != null)
            {
                audioSource.volume = 0.05f; // Giảm âm lượng âm thanh bước chân xuống
                audioSource.PlayOneShot(footstepSound);
            }
        }
        else if (moveInput.sqrMagnitude == 0 && audioSource.isPlaying)
        {
            audioSource.Stop();
        }

    }

    void Stopdasheff()
    {
        if (dashcoroutine != null) StopCoroutine(dashcoroutine);
    }
    void Startdasheff()
    {
        if (dashcoroutine != null) StopCoroutine(dashcoroutine);
        dashcoroutine = StartCoroutine(Dashcoroutine());
    }
    IEnumerator Dashcoroutine()
    {
        while (true) 
        {
            GameObject ghost = Instantiate(ghosteff, transform.position, transform.rotation);
            Sprite Csprite = characterSR.sprite;
            ghost.GetComponentInChildren<SpriteRenderer>().sprite = Csprite;

            Destroy(ghost, 0.5f);


            yield return new WaitForSeconds(delayS);
        }
    }
}
