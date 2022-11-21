using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_8
{
    public class ProgrammerLanguage
    {
        public string Name { get; private set; }
        public double Version { get; set; }
        public List<string> Operations;
        public ProgrammerLanguage(string Name)
        {
            this.Name = Name;
            Operations = new List<string>();
        }
        public void ChangeName(string name)
        {
            Name = name;
        }
        public void ChangeVersion(double version)
        {
            Version = version;
        }
        public void AddOperation(string Operation)
        {
            Operations.Add(Operation);
        }
        public void RemoveOperation(string Operation)
        {
            Operations.Remove(Operation);
        }
    }
}
