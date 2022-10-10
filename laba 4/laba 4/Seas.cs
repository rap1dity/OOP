using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    public class Maritime : Sea
    {
        public override string Salinity => "средней солёности";
        public void GetSalinity(IGetSalinity salinity) => salinity.GetSalinity();
        public void GetPopulation(IGetPopulation population) => population.GetPopulation();
        public override string ToString()
        {
            return "Maritime";
        }

    }
    public class Drinking : Sea
    {
        public override string Salinity => "Не солёная";
        public void GetSalinity(IGetSalinity salinity) => salinity.GetSalinity();
        public void GetPopulation(IGetPopulation population) => population.GetPopulation();
        public override string ToString()
        {
            return "Drinking";
        }
    }
}
