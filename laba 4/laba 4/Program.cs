using laba_4;
using System;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var russia = new State("Россия", "144.1 Млн","17.1 Млн км^2") as MainLand;
            var greenLand = new Island("субарктический", "unknown") as Land;
            var belarus = new State("Беларусь","9.399 Млн","207.6 км^2");
            var greenLand2 = new Island("субарктический", "unknown2");
            var sea = new Drinking();
            sea.GetPopulation(greenLand);
            sea.GetSalinity();
            if (belarus is MainLand) Console.WriteLine("Да, это так!");
            Printer printer = new Printer();
            Land[] landArray = { russia, greenLand, belarus, greenLand2 };
            foreach (Land i in landArray) { printer.iAmPrinting(i); }
        }
    }
}