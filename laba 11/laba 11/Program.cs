using laba_11;

namespace MyApp // Note: actual namespace depends on the project name.
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var test = new TestingClass(5);
            Reflector<TestingClass>.NameOfAssembly();
            Reflector<TestingClass>.ConstructorsCheck();
            var methodNames = new List<string>(Reflector<TestingClass>.GetMethods());
            var fieldsAndProperties = new List<string>(Reflector<TestingClass>.GetPropertiesAndFields());
            var interfaces = new List<string>(Reflector<TestingClass>.GetInterfaces());
            Console.WriteLine("Имена всех методов");
            foreach (var method in methodNames)
            {
                Console.WriteLine(method);
            }
            Console.WriteLine("Имена всех свойств и полей");
            foreach (var field in fieldsAndProperties)
            {
                Console.WriteLine(field);
            }
            Console.WriteLine("Список всех интерфейсов");
            foreach (var item in interfaces)
            {
                Console.WriteLine(item);
            }
            Reflector<TestingClass>.ShowMethods("str");
            using (StreamReader fs = new StreamReader("path.json"))
            {
                    Console.WriteLine("Введите имя метода, который хотите вызвать: ");
                    string? method = Console.ReadLine();
                while (true)
                {
                    string[] line = fs.ReadLine().Split(" : ");
                    if (line[0] == method)
                    {
                        string[] paramType = line[1].Split(",");
                        var result = new List<object>();
                        foreach (string item in paramType)
                        {
                            switch (item)
                            {
                                case "System.String":
                                    {
                                        result.Add("stroka");
                                        break;
                                    }
                                case "System.Int32":
                                    {
                                        result.Add(new Random().Next());
                                        break;
                                    }
                            }
                        }
                        object[] obj = new object[] { "hell" };
                        Reflector<TestingClass>.Invoke(test, method,obj);
                        return;
                    }
                }
            }
        }
    }
}