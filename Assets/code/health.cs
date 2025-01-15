using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using Pathfinding;
using UnityEngine.UI;
using TMPro;
using System;
public class health : MonoBehaviour
{
    public Image fillBar;
    public TextMeshProUGUI value;

    public void Update(int current, int maxhealth)
    {
        fillBar.fillAmount = (float)current / (float)maxhealth;
        value.text = current.ToString() + " / " + maxhealth.ToString();
    }

    internal void takeDam(int dame)
    {
        throw new NotImplementedException();
    }
}
