using System;
using System.Text.Json;

namespace MyApp
{
    public class Person
    {
        public string? Name { get; set; }
        public int Age { get; set; }

        public Person(string? name, int age)
        {
            Name = name;
            Age = age;
        }
        public void WriteToFile()
        {
            using (FileStream fs = new FileStream("person.json", FileMode.OpenOrCreate))
            {
                JsonSerializer.Serialize(fs, this);
                Console.WriteLine("Данные успешно записаны");
            }
        }
        public void ReadFromFile()
        {
            using (FileStream fs = new FileStream("person.json", FileMode.Open))
            {
                Person? person = JsonSerializer.Deserialize<Person>(fs);
                Console.WriteLine($"Имя: {person.Name} Возраст: {person.Age}");
            }
        }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            Person person = new Person("Андрей", 18);
            person.WriteToFile();
            person.ReadFromFile();
        }
    }
}