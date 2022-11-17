using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_7
{
    public interface IFunctions<T>
    {
        void add(T value);
        void remove();
        bool predicate();
    }
}
