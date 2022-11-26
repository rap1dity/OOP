namespace laba_12
{
    public class KAVLog
    {
        public static void RecordToFile(string message)
        {
            using(StreamWriter sw = new StreamWriter("kavlogfile.txt",true)) 
            {
                sw.WriteLine($"{message};{DateTime.Now}");
            }
        }
        public static void RecordsForDay(int day)
        {
            Console.WriteLine($"Список всей записей за {day} число ->");
            using(StreamReader sr = new StreamReader("kavlogfile.txt"))
            {
                string? extracted;
                while((extracted = sr.ReadLine()) != null)
                {
                    var line = extracted.Split(';');
                    if (DateTime.Parse(line[1]).Day == day)
                    {
                        Console.WriteLine(extracted);
                    }
                }
            }
        }
        public static void RecordsInTime(int hour1, int hour2)
        {
            Console.WriteLine($"Список всей записей, сделанных в промежутке от {hour1}:00 до {hour2}:00");
            using (StreamReader sr = new StreamReader("kavlogfile.txt"))
            {
                string? extracted;
                while ((extracted = sr.ReadLine()) != null)
                {
                    var line = extracted.Split(';');
                    var parsed = DateTime.Parse(line[1]).Hour;
                    if (parsed >= hour1 && parsed < hour2)
                    {
                        Console.WriteLine(extracted);
                    }
                }
            }
        }
        public static void FindByKeyword(string keyword)
        {
            Console.WriteLine($"Список всех записей, имеющих вхождение {keyword}");
            using(StreamReader sr = new StreamReader("kavlogfile.txt"))
            {
                string? extracted;
                while((extracted = sr.ReadLine()) != null)
                {
                    var line = extracted.Split(";");
                    if (line[0].IndexOf(keyword, StringComparison.CurrentCultureIgnoreCase) >= 0)
                    {
                        Console.WriteLine(extracted);
                    }
                }
            }
        }
    }
}
