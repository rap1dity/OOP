using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_9
{
    public class ServicesQueue<T> : Queue<T> where T : Services
    {
        public void Insert(T item)
        {
            Enqueue(item);
        }
        public void Print() {
            Console.WriteLine("Список очереди ->");
            foreach(var item in this)
            {
                Console.WriteLine(item.Name);
            }
        }
        public void Delete(T item) {
            if (Count == 0)
            {
                Console.WriteLine("Очередь пуста");
                return;
            }

            List<T> arr = new List<T>(this);
            if (arr.Remove(item)) {
                Clear();
                for(int i = 0; i < arr.Count; i++)
                {
                    Enqueue(arr[i]);
                }
                Console.WriteLine("Элемент удалён из очереди");
            }
            else
            {
                Console.WriteLine("Такой элемент не существует");
                return;
            }
        }
        public void Find(string Name)
        {
            int count = 0;
            foreach (T item in this)
            {
                if (item.Name == Name)
                {
                    count++;
                    Console.WriteLine($"Найден элемент по имени {Name}");
                    Console.WriteLine($"Цена услуги: {item.Price}$");
                    Console.WriteLine($"Отзывы об услуге:\n{item.GetFeedBack()}");
                    item.GetExecuteDay();
                }
            }
            if (count == 0)
            {
                Console.WriteLine($"Не было найдено услуги с именем {Name}");
                return;
            }
        }
    }
}
