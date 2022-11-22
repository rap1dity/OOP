namespace laba_12
{
    public class KAVLog
    {
        public static void RecordToFile(string message)
        {
            using(StreamWriter sw = new StreamWriter("kavlogfile.txt",true)) 
            {
                sw.WriteLine($"operation: {message} ; time: {DateTime.Now.ToShortTimeString()}"); 
            }
        }
    }
}
