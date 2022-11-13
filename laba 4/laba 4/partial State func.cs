using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    partial class State
    {
        private string[] continents = { "Европа","Северная Америка","Южная Америка","Африка","Австралия","Антарктида" };
        private long population;
        private string mainLand;
        public string Name { get; set; }
        public long StatePopulation 
        {
            get => population;
            set 
            { 
                if (value >= 1_000_000_000)
                    throw new PopulationException("Размер населения превышает максимальное значение");
                if (value < 0)
                    throw new TypeException("Размер население не может быть отрицательным");
                population = value;
            } 
        }
        public string StateArea { get; set; }
        public string MainLand { 
            get => mainLand; set 
            {
                if (continents.Contains(value))
                    mainLand = value;
                else
                    throw new ContinentException("Вы установили недопустимый континент");
            }
        }
        public State(string Name, long StatePopulation, string StateArea, string MainLand)
        {
            this.Name = Name;
            this.StatePopulation = StatePopulation;
            this.StateArea = StateArea;
            this.MainLand = MainLand;
        }
        public bool CheckMainLand(string mainLand)
        {
            if (mainLand == MainLand)
                return true;
            else return false;
                
        }
        public override void Area()
        {
            Console.WriteLine("local");
        }
        public override void Type()
        {
            Console.WriteLine("Это государство");
        }
        public override string ToString()
        {
            return "Государство";
        }
    }
}
