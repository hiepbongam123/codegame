using UnityEngine;
using UnityEngine.UI;

public class setlevel : MonoBehaviour
{
    public Dropdown difficultyDropdown; // Tham chiếu đến Dropdown

    void Start()
    {
        // Lắng nghe sự kiện khi người chơi chọn mức khó
        difficultyDropdown.onValueChanged.AddListener(OnDifficultyChanged);
    }

    // Hàm xử lý khi chọn mức khó
    void OnDifficultyChanged(int index)
    {
        string selectedDifficulty = difficultyDropdown.options[index].text;

        switch (selectedDifficulty)
        {
            case "Easy":
                Debug.Log("Mức khó: Easy");
                // Gọi hàm thiết lập mức chơi Easy
                SetDifficulty(1);
                break;

            case "Medium":
                Debug.Log("Mức khó: Medium");
                // Gọi hàm thiết lập mức chơi Medium
                SetDifficulty(2);
                break;

            case "Hard":
                Debug.Log("Mức khó: Hard");
                // Gọi hàm thiết lập mức chơi Hard
                SetDifficulty(3);
                break;

            default:
                Debug.Log("Không xác định mức khó");
                break;
        }
    }

    void SetDifficulty(int level)
    {
        // Xử lý mức chơi tương ứng (1 = Easy, 2 = Medium, 3 = Hard)
        Debug.Log("Đã thiết lập mức chơi: " + level);
        // Thêm logic cụ thể của bạn ở đây
    }
}
