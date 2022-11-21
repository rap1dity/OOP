using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_9
{
    public class SelfQueue<T> : Queue<T> where T : struct
    {
        public void Remove(int count)
        {
            if (count < 0 || count > Count)
            {
                Console.WriteLine("Вы попытались удалить некорректное количество элементов");
            }
            else
            {
                for (int i = 1; i < count; i++)
                {
                    Dequeue();
                }
            }
        }
    }
}
