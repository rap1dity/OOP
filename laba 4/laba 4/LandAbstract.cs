using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    public abstract class Land : IGetPopulation
    {
        public abstract string Population { get; }
        abstract public void Area();
        abstract public void Type();
        public virtual void GetPopulation() => Console.WriteLine($"{GetType().Name} Население: {Population}");
        public override string ToString() => "Суша";
    }
}
