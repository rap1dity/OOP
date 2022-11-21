using laba_10;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string[] winter = { "December", "January", "February" };
            string[] summer = { "June", "July", "August" };
            string[] months = { "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" };
            var fourSymbols = from m in months where m.Length == 4 select m;
            var winterAndSummer = from m in months where winter.Contains(m) || summer.Contains(m) select m;
            var monthsInAlphabetOrder = from m in months orderby m select m;
            var multiConditionmonths = from m in months where m.Length > 4 && m.Contains('u') select m;
            Console.WriteLine("Месяца, имена которых содержат 4 символа:");
            foreach (var item in fourSymbols)
            {
                Console.WriteLine(item);
            }
            Console.WriteLine("Зимние и летние месяца");
            foreach (var item in winterAndSummer)
            {
                Console.WriteLine(item);
            }
            Console.WriteLine("Месяца отсортированные по алфавитному порядку");
            foreach (var item in monthsInAlphabetOrder)
            {
                Console.WriteLine(item);
            }
            Console.WriteLine("Месяца содержащие букву u и длинной имени больше 4 символов");
            foreach (var item in multiConditionmonths)
            {
                Console.WriteLine(item);
            }
            var airlines = new List<Airline> {
            new Airline("Минск", "124124", "Эконом", "15:40", DayOfWeek.Friday),
            new Airline("Москва", "23423", "Бизнес", "16:20", DayOfWeek.Monday),
            new Airline("СПБ", "132122", "Эконом", "5:30", DayOfWeek.Thursday),
            new Airline("Нью-Йорк", "132134", "Бизнес", "14:00", DayOfWeek.Wednesday),
            new Airline("Киев", "753453", "Бизнес", "16:00", DayOfWeek.Friday),
            new Airline("Алматы", "345323", "Эконом", "20:20", DayOfWeek.Tuesday),
            new Airline("Вашингтон", "235423", "Эконом", "10:30", DayOfWeek.Sunday),
            new Airline("Варшава", "952342", "Эконом", "22:40", DayOfWeek.Saturday),
            new Airline("Минск", "642423", "Эконом", "16:50", DayOfWeek.Monday),
            new Airline("Канберра", "24234", "Бизнес", "4:30", DayOfWeek.Monday),
            new Airline("Вильнюс", "295318", "Бизнес", "7:00", DayOfWeek.Tuesday)
        };
            var time = "00:00";
            foreach (Airline airline in airlines)
            {
                if (airline.day == DayOfWeek.Monday && Convert.ToDateTime(airline.DepartureTime).Hour > Convert.ToDateTime(time).Hour)
                    time = Convert.ToDateTime(airline.DepartureTime).ToShortTimeString();
            }
            var destinationNumber = from dest in airlines where dest.FlightNumber == "235423" select dest;
            var dayOfWeekFlight = from dest in airlines where dest.day == DayOfWeek.Monday select dest;
            var maxDayOfWeekFlight = from dest in airlines where dest.day == DayOfWeek.Sunday select dest;
            var multiDayOfWeekFlight = from dest in airlines where dest.day == DayOfWeek.Monday && Convert.ToDateTime(dest.DepartureTime).Hour >= Convert.ToDateTime(time).Hour orderby dest.DepartureTime descending select dest;
            var orderedFlights = from dest in airlines orderby dest.day, dest.DepartureTime select dest;
            var sumOfBusinessFlights = airlines.Count(x => x.AirType == "Бизнес");
            Console.WriteLine("Список рейсов с номером 235423:");
            foreach(var item in destinationNumber)
            {
                Console.WriteLine(item.Destination);
            }
            Console.WriteLine("Список рейсов в понедельник:");
            foreach (var item in dayOfWeekFlight)
            {
                Console.WriteLine(item.Destination);
            }
            Console.WriteLine("Максимальный по дню недели рейс:");
            foreach (var item in maxDayOfWeekFlight)
            {
                Console.WriteLine(item.Destination);
            }
            Console.WriteLine("Все рейсы в понедельник с самым поздним временем вылета:");
            foreach (var item in multiDayOfWeekFlight)
            {
                Console.WriteLine($"Место посадки: {item.Destination} Время вылета: {item.DepartureTime}");
            }
            Console.WriteLine("Упорядоченные по дню и времени рейсы:");
            foreach (var item in orderedFlights)
            {
                Console.WriteLine(item.Destination);
            }
            Console.WriteLine($"Количество рейсов для бизнес типа самолёта: {sumOfBusinessFlights}");
            var complexRequest = from dest in airlines where dest.Destination.Length > 4 orderby dest.day descending group dest by dest.AirType;
            Console.WriteLine("Список рейсов с комплексным условием из > 5 операторов:");
            foreach (var item in complexRequest)
            {
                Console.WriteLine(item.Key);
            }
            var twoRequests = from item in orderedFlights
                              join item2 in dayOfWeekFlight on item.DepartureTime equals item2.DepartureTime
                              select item;
            Console.WriteLine("Использованный Join на два запроса");
            foreach (var item in twoRequests)
            {
                Console.WriteLine(item.Destination);
            }
        }
    }
}