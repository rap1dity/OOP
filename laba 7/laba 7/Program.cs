using laba_7;
using System;
using System.Collections;
using System.Collections.Generic;

namespace MyApp // Note: actual namespace depends on the project name.
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var stack = new CollectionType<Production>();
            stack.remove();
            stack.add(new Production(1, "prod1"));
            stack.add(new Production(2, "prod2"));
            stack.add(new Production(3, "prod3"));
            stack.add(new Production(4, "prod4"));
            stack.add(new Production(5, "prod5"));
            stack.remove();
            Console.WriteLine(stack.predicate());
            foreach (Production item in stack)
            {
                Console.WriteLine(item.orgName);
            }
            stack.WriteToFile(new Production(10, "name"));
            stack.ReadFromFile();
        }
    }
}