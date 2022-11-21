using laba_8;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Security.Cryptography.X509Certificates;
using System.Security.Principal;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Programmer Andrew = new();
            var Java = new ProgrammerLanguage("Java");
            var Python = new ProgrammerLanguage("Python");
            Andrew.Language += Java.ChangeName;
            Andrew.Language += message => OperationDisplay(message);
            Andrew.LanguageAddOption+= Python.AddOperation;
            Andrew.LanguageAddOption += Java.AddOperation;
            Andrew.LanguageRemoveOption += Python.RemoveOperation;
            Andrew.SetVersion += Python.ChangeVersion;
            Andrew._ChangeName("Unknown");
            Andrew._AddOption("classes");
            Andrew._AddOption("inheritance");
            Andrew._RemoveOption("classes");
            Andrew._RemoveOption("unknown");
            Andrew._SetVersion(10.9);
            Console.WriteLine($"Питон имеет версию: {Python.Version}");
            Console.WriteLine(Java.Name);
            foreach (var item in Java.Operations)
            {
                Console.WriteLine(item);
            }
            foreach (var item in Python.Operations)
            {
                Console.WriteLine(item);
            }
            void OperationDisplay(string name) => Console.WriteLine($"Имя языка программирования было изменено на {name}");
            string str = " apple,orange,box,c#,sql ";
            Func<string, string> operation = str =>
            {
                string temp = "";
                for (int i = 0; i < str.Length; i++)
                {
                    temp += str[i] == ',' ? ' ' : str[i];
                }
                return temp;
            };
            Func<string, string> upperCase = str => str.ToUpper();
            Func<string, string> killingSpace = str => str.Trim();
            Console.WriteLine(killingSpace(str));
            Console.WriteLine(upperCase(str));
            str = operation(str);
            Console.WriteLine(str);
            Action action = (x, y) => { Console.WriteLine($"Сумма {x} + {y} = {x + y}"); };
            action(6, 10);
            Predicate<int> predicate = (x) => x != 0;
            Console.WriteLine(predicate(1));
        }
        public delegate void Action(int x, int y);
        public delegate bool Predicate<in T>(T x) where T : struct;
    }
}