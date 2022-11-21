using laba_9;
using System.Collections.ObjectModel;
using System.Collections.Specialized;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var Courses = new Services("C# курс", 15, 25);
            var Courses2 = new Services("JS курс", 15, 25);
            var Courses3 = new Services("C++ курс", 15, 25);
            Courses.GetExecuteDay();
            var services = new ServicesQueue<Services>();
            services.Enqueue(Courses);
            services.Enqueue(Courses2);
            services.Enqueue(Courses3);
            Courses2.AddFeedback("Хороший курс");
            services.Print();
            services.Delete(Courses);
            services.Print();
            services.Find("JS курс");
            var queue = new SelfQueue<int>();
            queue.Enqueue(15);
            queue.Enqueue(242);
            queue.Enqueue(12312);
            queue.Enqueue(5);
            queue.Enqueue(14);
            var list = new List<int>(queue);
            Console.WriteLine("Вывод второй коллекции");
            foreach (var item in list)
            {
                Console.WriteLine(item);
            }
            Console.WriteLine(list.Find(x => x == 242));
            var observe = new ObservableCollection<Services>();
            observe.CollectionChanged += SelfQueue_CollectionChanged;
            observe.Add(Courses);
            observe.Add(Courses3);
            observe.Remove(Courses);
            observe[0] = Courses2;
            void SelfQueue_CollectionChanged(object? sender, NotifyCollectionChangedEventArgs e)
            {
                switch (e.Action)
                {
                    case NotifyCollectionChangedAction.Add: // если добавление
                        if (e.NewItems?[0] is Services added)
                            Console.WriteLine($"Добавлен новый объект: {added.Name}");
                        break;
                    case NotifyCollectionChangedAction.Remove: // если удаление
                        if (e.OldItems?[0] is Services removed)
                            Console.WriteLine($"Удален объект: {removed.Name}");
                        break;
                    case NotifyCollectionChangedAction.Replace: // если замена
                        if ((e.NewItems?[0] is Services replacing) &&
                            (e.OldItems?[0] is Services replaced))
                            Console.WriteLine($"Объект {replacing.Name} заменен объектом {replaced.Name}");
                        break;
                }
            }
        }
    }
}