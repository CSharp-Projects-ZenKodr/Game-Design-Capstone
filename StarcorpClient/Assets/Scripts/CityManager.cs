﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class CityManager : MonoBehaviour
{
    private GameController controller;

    public City cityPrefab;

    // TODO move these to somewhere more appropriate
    private float playerMoney;
    public Text playerMoneyLabel;
    public List<Text> cityLabels;

    private Socket socket;

    private Dictionary<Position, City> cities;


    // Start is called before the first frame update
    void Start()
    {
        this.controller = GetComponent<GameController>();

        this.cities = new Dictionary<Position, City>();
    }

    public void Initialize(Socket socket)
    {
        this.socket = socket;
        int cityCount = 0;
        socket.Register("load_city", (ev) =>
        {
            var data = ev.Data[0];

            City city = this.CreateCity((JObject)data);

            city.label = this.cityLabels[cityCount++];
        });

        socket.Register("resources_sold", (ev) =>
        {
            var data = ev.Data[0];
            var playerData = data["player"];
            var cityData = data["city"];

            this.playerMoney = (float)playerData["money"];

            var cityResources = cityData["resources"];
            foreach (var resource in (JObject)playerData["resources"])
            {
                this.controller.ResourceManager.Set(resource.Key, (int)resource.Value);

                var position = new Position((string)cityData["position"]);
                City city = this.cities[position];
                city.resources[resource.Key] = (int)cityResources[resource.Key];
            }
        });

        socket.Emit("get_cities");
    }

    City CreateCity(JObject data)
    {
        Position position = new Position((string)data["position"]);


        Vector3 worldPos = controller.gameGrid.getWorldPosition(position);

        City city = Instantiate(cityPrefab, worldPos, Quaternion.identity);

        city.Initialize(data);

        this.controller.ObjectManager.Track((string)data["uuid"], city.gameObject);
        this.cities.Add(position, city);

        return city;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(1))
        {
            Debug.Log($"Processing click at {Input.mousePosition}");
            Position pos = this.controller.gameGrid.getTile(Camera.main.ScreenToWorldPoint(Input.mousePosition)).position;
            Debug.Log($"Processing click at cube pos {pos}");

            City city;
            if (this.cities.ContainsKey(pos))
            {
                city = this.cities[pos];

                city.OnClick();

                JObject obj = new JObject();
                obj["city_id"] = city.uuid;
                Debug.Log($"Attempting to sell to {city}");
                this.socket.Emit("sell_resource", obj);
            }
        }
    }

    void OnGUI()
    {
        this.playerMoneyLabel.text = $"$ {this.playerMoney}";
    }
}
