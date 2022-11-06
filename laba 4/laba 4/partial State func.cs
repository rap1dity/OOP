using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    partial class State
    {
        public string Name { get; set; }
        public string StatePopulation { get; set; }
        public string StateArea { get; set; }
        public string MainLand { get; set; }
        public State(string Name, string StatePopulation, string StateArea, string MainLand)
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
