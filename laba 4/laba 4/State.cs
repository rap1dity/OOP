using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    public class State : MainLand
    {
        public string Name { get; set; }
        public string StatePopulation { get; set; }
        public string StateArea { get; set; }
        public State(string Name, string StatePopulation, string StateArea)
        {
            this.Name = Name;
            this.StatePopulation = StatePopulation;
            this.StateArea = StateArea;
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
