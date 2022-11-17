using laba_4;
using System;
using System.Diagnostics;
using Xunit;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var russia = new State("Россия", 144_000_000,"17.1 Млн км^2","Европа") as MainLand;
            var greenLand = new Island("субарктический", "Гренландия") as Land;
            var belarus = new State("Беларусь",9_430_000,"207.6 км^2","Европа");
            //belarus.StatePopulation = 0;
            Assert.NotEqual(0, belarus.StatePopulation);
            try
            {
                //belarus.StatePopulation = -5;
                //belarus.StatePopulation = 1_000_000_000;
                //belarus.MainLand = "Слово";
                //belarus.StatePopulation = belarus.StatePopulation / 0;
                try
                {
                    //belarus.StatePopulation = 1_000_000_000;
                    try
                    {
                        belarus.MainLand = "Слово";
                    }
                    catch(DivideByZeroException ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                }
                catch(Exception ex) 
                {
                    Console.WriteLine($"Метод в котором вызвано исключение: {ex.TargetSite}");
                    Console.WriteLine($"Строковое представление стека вызовов: {ex.StackTrace}");
                    Console.WriteLine($"Имя объекта или сборки: {ex.Source}");
                    Console.WriteLine($"Сообщение об ошибке: {ex.Message}");
                    if(ex.InnerException != null)
                        Console.WriteLine($"Информация об исключении, которое вызвало данное исключение: {ex.InnerException}");
                }
            }
            catch(TypeException ex)
            {
                Console.WriteLine(ex.Message);
            }
            catch (PopulationException ex)
            {
                Console.WriteLine(ex.Message);
            }
            catch (ContinentException ex)
            {
                Console.WriteLine(ex.Message); 
            }
            catch(DivideByZeroException ex)
            {
                Console.WriteLine(ex.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
            finally
            {
                Console.WriteLine("Блок Try-Catch-Finally закончился");
            }
            Debug.Assert(belarus.StateArea != "207.6 км^2", "Дебажим");
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