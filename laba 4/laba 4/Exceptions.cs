using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    public class PopulationException : Exception
    {
        public PopulationException(string message) : base(message) { }
    }
    public class TypeException : ArgumentException
    {
        public TypeException(string message) : base(message){ }
    }
    public class ContinentException : ArgumentOutOfRangeException
    {
        public ContinentException(string message) : base(message) { }
    }
}
