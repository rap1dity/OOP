using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace laba_10
{
    public class Airline
    {
        public string Destination { get; set; }
        public string FlightNumber { get; set; }
        public string AirType { get; set; }
        public string DepartureTime { get; set; }
        public DayOfWeek day { get; set; }
        public Airline(string destination, string flightNumber, string airType, string departureTime, DayOfWeek day)
        {
            Destination = destination;
            FlightNumber = flightNumber;
            AirType = airType;
            DepartureTime = departureTime;
            this.day = day;
        }
    }
}
