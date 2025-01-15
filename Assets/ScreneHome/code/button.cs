using UnityEngine;
using UnityEngine.UI;  // Đảm bảo rằng bạn đã sử dụng thư viện này để làm việc với UI
using UnityEngine.SceneManagement;  // Để load các scene

public class button : MonoBehaviour
{
    public Button startButton;  // Reference đến Button Start
    public Button quitButton;   // Reference đến Button Quit

    void Start()
    {
        // Đảm bảo rằng các button đã được gán trong Inspector
        if (startButton != null)
            startButton.onClick.AddListener(StartGame);

        if (quitButton != null)
            quitButton.onClick.AddListener(QuitGame);
    }

    // Hàm gọi khi nhấn vào nút Start
    void StartGame()
    {
        // Load Scene có tên "GameScene"
        SceneManager.LoadScene("GamePlay");  // Đổi tên Scene nếu cần
    }

    // Hàm gọi khi nhấn vào nút Quit
    void QuitGame()
    {
        // Thoát ứng dụng
        SceneManager.LoadScene("HomeMain");  // Đổi tên Scene nếu cần
    }
}
