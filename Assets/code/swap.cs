using UnityEngine;
using Unity.Cinemachine; // Namespace mới cho phiên bản mới

public class Swap : MonoBehaviour
{
    public GameObject player1; // Nhân vật 1
    public GameObject player2; // Nhân vật 2
    public CinemachineCamera virtualCamera; // Camera Cinemachine

    private GameObject currentPlayer; // Nhân vật đang được kích hoạt

    void Start()
    {
        // Mặc định Player1 là nhân vật chính
        currentPlayer = player1;
        virtualCamera.Follow = currentPlayer.transform;
    }
    void Update()
    {
        // Kiểm tra nếu nhấn phím "Q"
        if (Input.GetKeyDown(KeyCode.Q))
        {
            SwapPlayer();
        }
    }

    public void SwapPlayer()
    {
        if (currentPlayer == player1)
        {
            currentPlayer = player2;
            player1.SetActive(false);
            player2.SetActive(true);
        }
        else
        {
            currentPlayer = player1;
            player2.SetActive(false);
            player1.SetActive(true);
        }

        // Cập nhật CinemachineCamera
        virtualCamera.Follow = currentPlayer.transform;
    }
}
