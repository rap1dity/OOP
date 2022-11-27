using System.Collections.Concurrent;
using System.Diagnostics;

namespace laba_15
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Task matrici = new Task(() =>
            {
                var timer = new Stopwatch();
                timer.Start();
                Random rand = new Random();
                int[,] first = new int[100, 100];
                int[,] second = new int[100, 100];
                int[,] result = new int[100, 100];
                for(int i = 0;i < 100; i++)
                {
                    for(int j = 0; j < 100; j++)
                    {
                        first[i, j] = rand.Next(1,10);
                    }
                }
                for (int i = 0; i < 100; i++)
                {
                    for (int j = 0; j < 100; j++)
                    {
                        second[i, j] = rand.Next(1, 10);
                    }
                }
                Console.WriteLine("Результат ->\n");
                for (int i = 0; i < 100; i++)
                {
                    for (int j = 0; j < 100; j++)
                    {
                        result[i, j] = first[i,j] * second[i,j];
                        Console.Write($"{result[i,j]}\t");
                    }
                    Console.WriteLine("\n");
                }
                timer.Stop();
                Console.WriteLine($"Время выполнения перемножения: {timer.Elapsed}");
            });
            matrici.Start();
            Console.WriteLine($"Идентификатор текущей задачи: {matrici.Id}, Статус выполнения: {matrici.Status}");
            matrici.Wait();
            Thread.Sleep(2000);
            CancellationTokenSource cancelCourse = new CancellationTokenSource();
            CancellationToken token = cancelCourse.Token;
            matrici = new Task(() =>
            {
                var timer = new Stopwatch();
                timer.Start();
                Random rand = new Random();
                int[,] first = new int[100, 100];
                int[,] second = new int[100, 100];
                int[,] result = new int[100, 100];
                for (int i = 0; i < 100; i++)
                {
                    for (int j = 0; j < 100; j++)
                    {
                        first[i, j] = rand.Next(1, 10);
                    }
                }
                for (int i = 0; i < 100; i++)
                {
                    for (int j = 0; j < 100; j++)
                    {
                        second[i, j] = rand.Next(1, 10);
                    }
                }
                Console.WriteLine("Результат ->\n");
                for (int i = 0; i < 100; i++)
                {
                    for (int j = 0; j < 100; j++)
                    {
                        result[i, j] = first[i, j] * second[i, j];
                        Console.Write($"{result[i, j]}\t");
                    }
                    Console.WriteLine("\n");
                    if (token.IsCancellationRequested)
                    {
                        Console.WriteLine("Задача была остановлена!");
                        return;
                    }
                }
                timer.Stop();
                Console.WriteLine($"Время выполнения перемножения: {timer.Elapsed}");
            }, token);
            matrici.Start();
            Thread.Sleep(100);
            cancelCourse.Cancel();
            Thread.Sleep(100);
            cancelCourse.Dispose();
            Thread.Sleep(500);
            var firstNum = new Task<int>(() =>
            {
                return 25;
            });
            var  secondNum = new Task<int>(() =>
            {
                return 50;
            });
            var thirdNum = new Task<int>(() =>
            {
                return 75;
            });
            firstNum.Start();
            secondNum.Start();
            thirdNum.Start();
            Task resultNum = new Task(() =>
            {
                Console.WriteLine($"Результат третьего задания: {firstNum.Result + secondNum.Result + thirdNum.Result}");
            });
            resultNum.Start();
            Thread.Sleep(1000);
            Console.WriteLine("Задача 4");
            Task stroka1 = new Task(() =>
            {
                Console.WriteLine("Первая строка");
            });
            Task stroka2 = stroka1.ContinueWith((Task t) => 
            {
                Console.WriteLine("Вторая строка");
            });
            stroka1.Start();

            stroka2.Wait();
            Console.WriteLine("\t---");
            stroka1 = new Task(() =>
            {
                Console.WriteLine("Первая строка");
            });
            stroka2 = new Task(() =>
            {
                Console.WriteLine("Вторая строка");
            });
            stroka1.GetAwaiter().OnCompleted(() =>
            {
                stroka2.Start();
            });
            stroka1.Start();
            Thread.Sleep(500);
            Console.WriteLine("Задача 5 и 6");
            int[] list = new int[1000000];
            Stopwatch watcher = new Stopwatch();
            watcher.Start();
            for(int i = 0; i < 1000000; i++)
            {
                list[i] = i;
            }
            watcher.Stop();
            Console.WriteLine($"Время заполнения одного массива элементами: {watcher.Elapsed}");
            Thread.Sleep(1000);
            int[] ints1 = new int[1000000];
            int[] ints2 = new int[1000000];
            watcher.Start();
            Parallel.Invoke(() =>
            {
                Parallel.For(1, 1000000, (int i) => ints1[i] = i);
                Console.WriteLine("Первый заполнен");

            }, () =>
            {
                Parallel.ForEach(list, (int i) => { ints2[i] = i;});
                Console.WriteLine("Второй заполнен");
            });
            watcher.Stop();
            Console.WriteLine($"Время заполнения двух массивов через Parallel элементами: {watcher.Elapsed}");
            Console.WriteLine("7 задание");
            using (BlockingCollection<string> bc = new BlockingCollection<string>())
            {
                Task bcAdder = Task.Run(() =>
                {

                    bc.Add("да");
                    Thread.Sleep(100);
                    bc.Add("как");
                    Thread.Sleep(70);
                    bc.Add("меня");
                    Thread.Sleep(184);
                    bc.Add("это");
                    Thread.Sleep(240);
                    bc.Add("задолбало");
                    bc.CompleteAdding();
                });

                Task bcCustomers = Task.Run(() =>
                {
                    try
                    {
                        while (true)
                        {
                            Console.WriteLine("Сейчас на складе");
                            foreach (var item in bc)
                            {
                                Console.WriteLine(item);
                            }
                            Thread.Sleep(200);
                            Console.WriteLine($"{bc.Take()} был куплен");
                        };
                    }
                    catch(InvalidOperationException)
                    {
                        Console.WriteLine("Склад пуст 0_o");
                    }
                });
                Task.WhenAll(bcAdder, bcCustomers).Wait();
            };
            Console.WriteLine("8 задание");
            Freedom().Wait();
        }
            async static Task Freedom()
        {
            void Hello(string name)
            {
                Thread.Sleep(500);
                Console.WriteLine($"result: {"hello " + name}");
            }
            async Task Printasync()
            {
                Console.WriteLine("begin");
                await Task.Run(() => Hello("Andrew"));
                await Task.Run(() => Hello("Oleg"));
                await Task.Run(() => Hello("Roma"));
                Console.WriteLine("end");
            }
            await Printasync();
        }
    }
}