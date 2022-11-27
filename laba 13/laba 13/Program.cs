using System.Runtime.Serialization.Formatters.Binary;
using System.Text.Json;
using System.Xml;
using System.Xml.Linq;
using System.Xml.Serialization;

namespace laba_13
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var madagascar = new Island("fine", "madagascar");
            var iceland = new Island("not ok", "iceland");
            var binary = new BinaryFormatter();
            using(FileStream fs = new FileStream("binary.dat", FileMode.OpenOrCreate))
            {
                binary.Serialize(fs, madagascar);
                Console.WriteLine("Бинарный объект сериализован");
            }
            using(FileStream fs = new FileStream("binary.dat", FileMode.Open))
            {
                var deserialyzedBinary = (Island)binary.Deserialize(fs);
                Console.WriteLine($"Имя: {deserialyzedBinary.Name}\nКлимат: {deserialyzedBinary.Climate}");
            }
            //var soap = new SoapFormatter();
            //using(FileStream fs = new FileStream("soap.soap", FileMode.OpenOrCreate))
            //{
            //    soap.Serialize(fs, madagascar);
            //    Console.WriteLine("SOAP объект сериализован");
            //}
            //using(FileStream fs = new FileStream("soap.soap", FileMode.Open))
            //{
            //   Island deserialyzedSOAP = (Island)soap.Deserialize(fs);
            //    Console.WriteLine($"Имя: {deserialyzedSOAP.Name}\nКлимат: {deserialyzedSOAP.Climate}");
            //}
            using (FileStream fs = new FileStream("json.json", FileMode.OpenOrCreate))
            {
                JsonSerializer.Serialize(fs, madagascar);
                Console.WriteLine("JSON объект сериализован");
            }
            using (FileStream fs = new FileStream("json.json", FileMode.Open))
            {
                var deserialyzedJSON = JsonSerializer.Deserialize<Island>(fs);
                Console.WriteLine($"Имя: {deserialyzedJSON?.Name}\nКлимат: {deserialyzedJSON?.Climate}");
            }
            var xmlSerialyzer = new XmlSerializer(typeof(Island));
            using(FileStream fs = new FileStream("xml.xml", FileMode.OpenOrCreate))
            {
                xmlSerialyzer.Serialize(fs, madagascar);
                Console.WriteLine("XML объект сериализован");
            }
            using(FileStream fs = new FileStream("xml.xml", FileMode.Open))
            {
                var deserialyzedXML = xmlSerialyzer.Deserialize(fs) as Island;
                Console.WriteLine($"Имя: {deserialyzedXML?.Name}\nКлимат: {deserialyzedXML?.Climate}");
            }
            Island[] islands = new Island[] { madagascar, iceland };
            using(FileStream fs = new FileStream("islandArray.json", FileMode.OpenOrCreate))
            {
                JsonSerializer.Serialize(fs, islands);
                Console.WriteLine("Массив объектов записан");
            }
            using (FileStream fs = new FileStream("islandArray.json", FileMode.Open))
            {
                var readedIslands = JsonSerializer.Deserialize<Island[]>(fs);
                foreach (var item in readedIslands)
                {
                    Console.WriteLine($"Имя: {item?.Name}\nКлимат: {item?.Climate}");
                }
            }
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.Load("person.xml");
            XmlElement? xRoot = xmlDoc.DocumentElement;

            XmlNodeList? nodes = xRoot?.SelectNodes("person");
            if(nodes is not null)
            {
                if (nodes is not null)
                {
                    foreach (XmlNode node in nodes)
                    {
                        Console.WriteLine(node.SelectSingleNode("@name")?.Value);
                    }
                }
            }
            XmlNodeList? nodes2 = xRoot?.SelectNodes("*");
            if (nodes2 is not null)
            {
                foreach (XmlNode node in nodes2)
                {
                    Console.WriteLine(node.OuterXml);
                }
            }
            XDocument xDoc = new XDocument();

            XElement Andrew = new XElement("poibms");

            XAttribute AndrewName = new XAttribute("student", "Andrew");
            XElement AndrewEducation = new XElement("university", "BSTU");
            XElement AndrewAge = new XElement("age", "18");

            Andrew.Add(AndrewName);
            Andrew.Add(AndrewEducation);
            Andrew.Add(AndrewAge);

            XElement students = new XElement("students");

            students.Add(Andrew);

            xDoc.Add(students);

            xDoc.Save("students.xml");

            XmlDocument studentRequests = new XmlDocument();
            studentRequests.Load("students.xml");
            XmlElement studRoot = studentRequests.DocumentElement;

            XmlNodeList? studNodeList = studRoot?.SelectNodes("poibms");
            if(studNodeList is not null)
            {
                foreach (XmlNode item in studNodeList)
                {
                    Console.WriteLine($"{item.SelectSingleNode("@student")?.Value}");
                }
            }
        }
    }
}