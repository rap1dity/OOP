using laba_7;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Text.Json;

namespace MyApp
{
    public class CollectionType<T> : Stack, IFunctions<T> where T : Production
    {
        public List<T> list = new();
        public CollectionType() { }
        public static CollectionType<T> operator +(CollectionType<T> stack,int num) { stack.Push(num); return stack; }
        public static CollectionType<T> operator --(CollectionType<T> stack) { stack.Pop(); return stack; }
        public static bool operator true(CollectionType<T> stack) { return stack.Count == 0; }
        public static bool operator false(CollectionType<T> stack) { return stack.Count != 0; }
        public static CollectionType<T> operator >(CollectionType<T> stack1, CollectionType<T> stack2)
        {
            ArrayList array = new ArrayList();
            array.AddRange(stack1);
            array.AddRange(stack2);
            var temp = array.ToArray();
            Array.Sort(temp);
            stack2.Clear();
            foreach (var item in temp)
            {
                stack2.Push(item);
            }
            return stack2;
        }
        public static CollectionType<T> operator <(CollectionType<T> stack1, CollectionType<T> stack2)
        {
            ArrayList array = new ArrayList();
            array.AddRange(stack1);
            array.AddRange(stack2);
            var temp = array.ToArray();
            Array.Sort(temp);
            stack2.Clear();
            foreach (var item in temp)
            {
                stack2.Push(item);
            }
            return stack2;
        }
        public class Developer
        {
            string Фамилия;
            string Имя;
            string Отчество;
            int id;
            string department;
            public Developer(string Фамилия, string Имя, string Отчество, int id, string department)
            {
                this.Фамилия = Фамилия;
                this.Имя = Имя;
                this.Отчество = Отчество;
                this.id = id;
                this.department = department;
            }
        }
        public void WriteToFile(Production prod)
        {
            using (FileStream fs = new FileStream("Prod.json", FileMode.OpenOrCreate))
            {
                JsonSerializer.Serialize(fs, prod);
                Console.WriteLine("Production wrote");
            }
        }
        public void ReadFromFile()
        {
            using (FileStream fs = new FileStream("Prod.json", FileMode.Open))
            {
                Production? prod = JsonSerializer.Deserialize<Production>(fs);
                Console.WriteLine($"id: {prod.id} orgName:{prod.orgName}");
            }
        }

        public void add(T value)
        {
            Push(value);
        }

        public void remove()
        {
            try
            {
                Pop();
            }
            catch(Exception ex)
            {
                Console.WriteLine($"Вы попытались удалить элемент в пустом стеке\n Код ошибки: {ex.Message}");
            }
            finally{
                Console.WriteLine("Операция успешно завершена");
            }
        }
        public bool predicate()
        {
            return Count > 5;
        }
    }
    public class Production
    {
        public int id { get; set; }
        public string orgName { get; set; }
        public Production(int id, string orgName)
        {
            this.id = id;
            this.orgName = orgName;
        }
    }
}