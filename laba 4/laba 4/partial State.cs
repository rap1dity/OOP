namespace laba_4
{
    struct Construction
    {
        public string typeOfBuilding;
        public int price;
        public string size;
        public Construction(string typeOfBuilding, int price, string size)
        {
            this.typeOfBuilding = typeOfBuilding;
            this.price = price;
            this.size = size;
        }
    }
    public partial class State : MainLand
    {
        Construction construction;
        Construction tower = new("arrowTower", 250, "medium");
        Construction castle = new("castle", 2000, "huge");
        Construction bridge = new("bridge", 100, "small");

        public enum BuildingType
        {
            arrowTower = 1,
            castle,
            bridge
        }
        public void SetBuilding(BuildingType buildType)
        {
            switch (buildType)
            {
                case BuildingType.arrowTower:
                    construction = tower;
                    Console.WriteLine("Вы построили вышку лучника");
                    break;
                case BuildingType.castle:
                    construction = castle;
                    Console.WriteLine("Вы построили замок");
                    break;
                case BuildingType.bridge:
                    construction = bridge;
                    Console.WriteLine("Вы построили мост");
                    break;
                default:
                    Console.WriteLine("Вы попытались создать несуществующее строение");
                    break;
            }
        }
    }
}
