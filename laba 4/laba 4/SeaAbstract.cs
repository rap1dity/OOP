using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    public abstract class Sea : IGetSalinity
    {
        public abstract string Salinity { get; }
        public virtual void GetSalinity() => Console.WriteLine($"{GetType().Name} Солёность: {Salinity}");
        public override string ToString() => "Море";

    }
}
