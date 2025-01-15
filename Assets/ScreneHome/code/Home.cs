using UnityEngine;
using UnityEngine.SceneManagement;

public class Home : MonoBehaviour
{
    public player[] characterPrefabs; // Danh sách các prefab nhân vật
    public Transform spawnPoint;       // Điểm xuất hiện của nhân vật

    void Start()
    {
        // Lấy ID từ PlayerPrefs
        int selectedID = PlayerPrefs.GetInt("SelectedCharacterID", 0);

        // Tìm và spawn nhân vật dựa trên ID
        foreach (var character in characterPrefabs)
        {
            if (character.characterID == selectedID)
            {
                Instantiate(character.gameObject, spawnPoint.position, Quaternion.identity);
                return;
            }
        }

        Debug.LogError("Character with the selected ID not found!");
    }
}
