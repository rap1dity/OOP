using System.Reflection;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;

namespace laba_11
{
    public static class Reflector<T> where T : class
    {
        public static void NameOfAssembly()
        {
            using (StreamWriter fs = new StreamWriter("path.json", false))
            {
                fs.WriteLine($"Assembly: {typeof(T).Assembly.FullName}");
                //JsonSerializer.Serialize(fs, $"Assembly: {typeof(T).Assembly.FullName}\n");
            }
            Console.WriteLine($"Имя сборки : {typeof(T).Assembly}");
        }
        public static void ConstructorsCheck()
        {
            using (StreamWriter fs = new StreamWriter("path.json", true))
            {
                fs.WriteLine($"HavePublicConstructors : {typeof(T).GetConstructors().Length > 0}");
                //JsonSerializer.Serialize(fs, $"HavePublicConstructors : {typeof(T).GetConstructors().Length > 0}\n");
            }
            Console.WriteLine($"Наличие публичного конструктора: {typeof(T).GetConstructors().Length > 0}");
        }
        public static IEnumerable<string> GetMethods()
        {
            MethodInfo[] met =  typeof(T).GetMethods();
            var methods = new List<string>();
            foreach ( MethodInfo m in met ) {
                using (StreamWriter fs = new StreamWriter("path.json", true))
                {
                    var par = m.GetParameters();
                    var parTypes = new List<string>();
                    foreach (var item in par)
                    {
                        parTypes.Add(item.ParameterType.ToString());
                    }
                    fs.WriteLine($"{m.Name} : {string.Join(',', parTypes)}");
                }
                if(m.ReturnType== typeof(string))
                {
                    methods.Add(m.Name);
                }
            }
            return methods;
        }
        public static IEnumerable<string> GetPropertiesAndFields()
        {
            var props = typeof(T).GetProperties();
            var fields = typeof(T).GetFields();
            var result = new List<string>();
            foreach ( var field in fields )
            {
                result.Add(field.Name);
            }
            foreach (var prop in props)
            {
                result.Add(prop.Name);
            }
            return result;
        }
        public static IEnumerable<string> GetInterfaces()
        {
            var interfaces = typeof(T).GetInterfaces();
            var result = new List<string>();
            foreach (var item in interfaces)
            {
                result.Add(item.Name);
            }
            return result;
        }
        public static void ShowMethods(string parameter)
        {
            var methods = typeof(T).GetMethods();
            Console.WriteLine($"Список методов содержащих параметр: {parameter}");
            foreach (var method in methods) {
                var temp = method.GetParameters();
                if (temp.Any(par => par.Name == parameter))
                    Console.WriteLine(method.Name);
            }
        }
        public static void Invoke(T cls, string method, object[] param)
        {
            Console.WriteLine(typeof(T).GetMethod(method)?.Invoke(cls, param));
        }
    }
}
