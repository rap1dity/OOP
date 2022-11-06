using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_4
{
    class Printer
    {
        public void iAmPrinting(Land someobj)
        {
            Console.WriteLine("Тип объекта = " + someobj.ToString());
        }
    }
}
