using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_9
{
    public class Services : IOrderedDictionary
    {
        public string? Name { get; set; }
        DateTime ExecutionTime { get; set; }
        List<string> Feedback { get; set; }
        public int Price { get; set; }
        public void GetExecuteDay()
        {
            var Difference = ExecutionTime - DateTime.Now;
            Console.WriteLine($"услуга {Name}, будет предоставлена через {Difference.Days} дней");
        }
        public void AddFeedback(string feedback)
        {
            if (!string.IsNullOrEmpty(feedback))
                Feedback.Add(feedback);
            else
                Console.WriteLine("Нелья задать пустой комментарий");
        }
        public string GetFeedBack()
        {
            return string.Join("\n", Feedback);
        }
        public Services(string? name, int executionDays, int price)
        {
            Name = name;
            ExecutionTime = DateTime.Now.AddDays(executionDays);
            Price = price;
            Feedback = new List<string>();
        }
    }
}
