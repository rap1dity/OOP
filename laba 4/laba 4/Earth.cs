using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    public class Earth : IEnumerable
    {
        public List<Land> ListOfLands;
        public List<Sea> ListOfSeas;
        public List<Land> GetStateList { get => ListOfLands; }
        public List<Sea> GetSeaList { get => ListOfSeas; }
        public Earth()
        {
            ListOfLands = new List<Land>();
            ListOfSeas = new List<Sea>();
        }
        public Earth(Land obj)
        {
            ListOfLands.Add(obj);
        }
        public Earth(Sea obj)
        {
            ListOfSeas.Add(obj);
        }
        public void Add(Land obj)
        {
            ListOfLands.Add(obj);
        }
        public void Add(Sea obj)
        {
            ListOfSeas.Add(obj);
        }
        public bool RemoveLand(int index)
        {
            if (ListOfLands.Count < index)
                throw new Exception("Размер списка меньше, чем заданный индекс");
            Console.WriteLine("Материк успешно удалён");
            ListOfLands.RemoveAt(index);
            return true;
        }
        public bool RemoveSea(int index)
        {
            if (ListOfSeas.Count < index)
                throw new Exception("Размер списка меньше, чем заданный индекс");
            Console.WriteLine("Море успешно удалён");
            ListOfLands.RemoveAt(index);
            return true;
        }
        public void ShowLands()
        {
            Console.WriteLine("Список государств:");
            foreach (dynamic item in ListOfLands)
            {
                if (item is State)
                {
                    Console.WriteLine(item.Name);
                }
            }
            Console.WriteLine("Список островов");
            foreach (dynamic item in ListOfLands)
            {
                if (item is Island)
                {
                    Console.WriteLine(item.Name);
                }
            }
        }
        public void ShowSeas()
        {
            Console.WriteLine("Список морей");
            foreach (var item in ListOfSeas)
            {
                Console.WriteLine(item);
            }
        }
        public IEnumerator GetEnumerator()
        {
            return ListOfLands.GetEnumerator();
        }
    }
    public class EarthController
    {
        private List<Land> Lands;
        private List<Sea> Seas;
        public EarthController()
        {
            Lands = new List<Land>();
            Seas = new List<Sea>();
        }
        public void Add(Land land)
        {
            Lands.Add(land);
        }
        public void Add(Sea sea)
        {
            Seas.Add(sea);
        }
        public void StateAmount(string continent, Earth land)
        {
            int counter = 0;
            foreach (dynamic item in land)
            {
                if (item is State)
                {
                    if (item.CheckMainLand(continent))
                        counter++;
                }
            }
            Console.WriteLine($"Количество государств в {continent} равняется {counter}");
        }
        public void SeaAmount(Earth sea)
        {
            Console.WriteLine($"Количество морей равняется {sea.ListOfSeas.Count()}");
        }
        public void Islands(Earth land)
        {
            List<string> islands = new List<string>();
            foreach(dynamic item in land)
            {
                if(item is Island)
                {
                    islands.Add(item.Name);
                }
            }
            islands.Sort();
            Console.WriteLine("Список островов в алфавитном порядке");
            foreach (var item in islands)
            {
                Console.WriteLine(item);
            }
        }
        public void Show()
        {
            Console.WriteLine("Список суш");
            foreach (dynamic item in Lands)
            {
                Console.WriteLine(item.Name);
            }
        }
        private const string path = @"C:\Users\rap1dity\source\repos\laba 4\laba 4\default.txt";
        private const string JSONpath = @"C:\Users\rap1dity\source\repos\laba 4\laba 4\notdefault.json";
        public static EarthController GetEarthFromFile()
        {
            using (FileStream fstream = File.OpenRead(path))
            {
                EarthController fileData = new EarthController();
                byte[] buffer = new byte[fstream.Length];
                fstream.Read(buffer, 0, buffer.Length);
                string[] textFromFile = Encoding.Default.GetString(buffer).Split('|');
                foreach (var item in textFromFile)
                {
                    var shell = new State(item);
                    fileData.Add(shell);
                }
                return fileData;
            }
        }
        public static EarthController GetEarthFromJSONFile()
        {
            using (FileStream fstream = File.OpenRead(JSONpath))
            {
                EarthController fileData = new EarthController();
                byte[] buffer = new byte[fstream.Length];
                fstream.Read(buffer, 0, buffer.Length);
                string textFromFile = Encoding.Default.GetString(buffer);
                if (textFromFile == "")
                {
                    throw new Exception("146 line | Container.CS| file is empty");
                }
                var JSONFile = JsonConvert.DeserializeObject<List<State>>(textFromFile);

                foreach (var item in JSONFile)
                {
                    fileData.Add(item);
                }
                return fileData;
            }
        }
    }
    partial class State
    {
        [JsonConstructor]
        public State(string Name)
        {
            this.Name = Name;
        }
    }
}
