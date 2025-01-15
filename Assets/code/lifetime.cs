using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class lifetime : MonoBehaviour

{
    public float Time;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        Destroy(this.gameObject, Time);
    }


}
