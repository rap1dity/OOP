using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_8
{
    public class Programmer
    {
        public delegate void LanguageName(string name);
        public delegate void AddOption(string option);
        public delegate void RemoveOption(string option);
        public delegate void Version(double version);
        public event Version? SetVersion;
        public event LanguageName? Language;
        public event AddOption? LanguageAddOption;
        public event RemoveOption? LanguageRemoveOption;
        public void _ChangeName(string Name)
        {
            Language?.Invoke(Name);
        }
        public void _RemoveOption(string option)
        {
            LanguageRemoveOption?.Invoke(option);
        }
        public void _AddOption(string option)
        {
            LanguageAddOption?.Invoke(option);
        }
        public void _SetVersion(double version)

        {
            SetVersion?.Invoke(version);
        }
    }
}
