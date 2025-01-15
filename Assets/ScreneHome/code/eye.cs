using UnityEngine;

public class eye : MonoBehaviour
{
    public RectTransform eyefl; // Transform của mắt
    public RectTransform pupil; // Transform của con ngươi
    public float pupilMoveRadius = 15f; // Bán kính mà con ngươi có thể di chuyển trong mắt

    void Update()
    {
        // Lấy vị trí chuột trên màn hình
        Vector2 mousePosition = Input.mousePosition;

        // Chuyển đổi vị trí chuột sang không gian của Canvas
        Vector2 eyeCenter = RectTransformUtility.WorldToScreenPoint(Camera.main, eyefl.position);
        Vector2 direction = (mousePosition - eyeCenter).normalized;

        // Giới hạn chuyển động của con ngươi trong bán kính cho phép
        Vector2 pupilOffset = direction * Mathf.Min(pupilMoveRadius, Vector2.Distance(mousePosition, eyeCenter));

        // Cập nhật vị trí của con ngươi
        pupil.anchoredPosition = pupilOffset;
    }
}
