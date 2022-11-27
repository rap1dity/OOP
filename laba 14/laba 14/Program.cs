using System.Diagnostics;

namespace laba_14
{
    internal class Program
    {
        static void Main(string[] args)
        {
            foreach (Process item in Process.GetProcesses())
            {
                // Невозможно получить из-за отсутствия прав доступа
                //Console.WriteLine($"ID процесса: {item.Id}, Имя процесса: {item.ProcessName}, Приоритет: {item.BasePriority}, Время запуска: {item.StartTime}, Текущее состояние: {item.HasExited}, Общее время работы: {item.TotalProcessorTime}");
                Console.WriteLine($"ID процесса: {item.Id}, Имя процесса: {item.ProcessName}, Приоритет: {item.BasePriority}");
            }
            AppDomain domain = AppDomain.CurrentDomain;
            Console.WriteLine($"Имя домена: {domain.FriendlyName}\nДетали конфигурации: {domain.SetupInformation.TargetFrameworkName}, {domain.SetupInformation.ApplicationBase}");
            Console.WriteLine("Список сборок в домене");
            foreach (var item in domain.GetAssemblies())
            {
                Console.WriteLine(item.FullName);
            }
            Console.WriteLine("AppDomain domain = AppDomain.CreateDomain(\"MyDomain\")");
            Console.WriteLine("var assebly = domain.Load(\"File.dll\")");
            Console.WriteLine("AppDomain.Unload(domain)");
            //File.Create("numbers.txt");
            Console.WriteLine("Введите число: ");
            int count = Convert.ToInt32(Console.ReadLine());
            Thread iteration = new Thread(() =>
            {
                for(int i = 1; i <= count; i++)
                {
                    Thread.Sleep(100);
                    Console.WriteLine(i);
                    using (StreamWriter sw = File.AppendText("numbers.txt"))
                    {
                        sw.WriteLine(i);
                    }
                }
            });
            iteration.Name = "bistreebietoujekonchilos";
            iteration.Start();
            Console.WriteLine($"Имя потока: {iteration.Name}, Статус потока: {iteration.ThreadState}, Приоритет потока: {iteration.Priority}, Идентификатор потока: {iteration.ManagedThreadId}");
            Thread.Sleep(2000);
            //File.Create("evenodd.txt");
            Console.WriteLine("Задание 4");
            Thread Even = new Thread(() =>
            {
                for (int i = 0; i <= 10; i += 2)
                {
                    Console.WriteLine(i);
                        File.AppendAllText("evenodd.txt", $"{i}");
                    Thread.Sleep(100);
                }
            });
            Thread Odd = new Thread(() =>
            {
                for (int i = 1; i <= 10; i += 2)
                {
                    Console.WriteLine(i);
                    File.AppendAllText("evenodd.txt", $"{i}");
                    Thread.Sleep(150);
                }
            });
            Even.Priority = ThreadPriority.AboveNormal;
            Even.Start();
            Odd.Start();
            Thread.Sleep(2000);
            object locker = new();
            //File.Create("asyncnumb.txt");
            Thread part1 = new Thread(() =>
            {
                lock (locker)
                {
                    for (int i = 0; i <= 10; i += 2)
                    {
                        Console.WriteLine(i);
                        Thread.Sleep(100);
                    }
                }
            });
            Thread part2 = new Thread(() =>
            {
                lock (locker)
                {
                    for (int i = 1; i <= 10; i += 2)
                    {
                        Console.WriteLine(i);
                        Thread.Sleep(100);
                    }
                }
            });
            part1.Start();
            part2.Start();
            Thread.Sleep(2000);
            Mutex mute = new();
            part1 = new Thread(() =>
            {
                for(int i = 0; i < 10; i+=2)
                {
                    mute.WaitOne();
                    Console.WriteLine(i);
                    Thread.Sleep(100);
                    mute.ReleaseMutex();
                }
            });
            part2 = new Thread(() =>
            {
                for (int i = 1; i < 10; i+=2)
                {
                    mute.WaitOne();
                    Console.WriteLine(i);
                    Thread.Sleep(100);
                    mute.ReleaseMutex();
                }
            });
            part1.Start();
            part2.Start();
            Thread.Sleep(2000);
            Console.WriteLine("Задание 5");
            int num = 0;
            TimerCallback tm = new TimerCallback(Count);
            Timer timer = new Timer(tm, num, 0, 2000);
            void Count(object obj)
            {
                int x = (int)obj;
                for (int i = 1; i < 10; i++, x++)
                {
                    Console.WriteLine(x * i);
                }
            }
            Console.ReadLine();
        }
    }
}