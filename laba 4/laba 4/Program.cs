using laba_4;
using System;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var russia = new State("Россия", "144.1 Млн","17.1 Млн км^2","Европа") as MainLand;
            var greenLand = new Island("субарктический", "Гренландия") as Land;
            var belarus = new State("Беларусь","9.399 Млн","207.6 км^2","Европа");
            belarus.SetBuilding(State.BuildingType.arrowTower);
            var madagascar = new Island("субарктический", "Мадагаскар");
            var sea = new Drinking();
            sea.GetPopulation(greenLand);
            sea.GetSalinity();
            if (belarus is MainLand) Console.WriteLine("Да, это так!");
            Printer printer = new Printer();
            Land[] landArray = { russia, greenLand, belarus, madagascar };
            foreach (Land i in landArray) { printer.iAmPrinting(i); }
            Earth earth = new Earth();
            earth.Add(belarus);
            earth.Add(madagascar);
            earth.Add(greenLand);
            earth.Add(sea);
            earth.ShowLands();
            EarthController controller = new EarthController();
            controller.StateAmount("Европа",earth);
            controller.SeaAmount(earth);
            controller.Islands(earth);
            var fromFileData = EarthController.GetEarthFromFile();
            var fromJSONData = EarthController.GetEarthFromJSONFile();
            fromFileData.Show();
            fromJSONData.Show();
        }
    }
}