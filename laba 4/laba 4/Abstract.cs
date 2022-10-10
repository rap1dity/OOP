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
    public abstract class Sea : IGetSalinity
    {
        public abstract string Salinity { get; }
        public virtual void GetSalinity() => Console.WriteLine($"{GetType().Name} Солёность: {Salinity}");
        public override string ToString() => "Море";

    }
    class Printer
    {
        public void iAmPrinting(Land someobj)
        {
            Console.WriteLine("Тип объекта = " + someobj.ToString());
        }
    }
}
