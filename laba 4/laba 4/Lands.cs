namespace laba_4
{
    public class MainLand : Land
    {
        public override string Population => "5.349 Млрд";

        public override void Area()
        {
           Console.WriteLine("53.6 млн км^2");
        }

        public override void Type()
        {
            Console.WriteLine("Это континент");
        }
        public override string ToString()
        {
            return "Материк";
        }
    }
    public class Island : Land
    {
        public override string Population => "730 Млн";

        public override void Area()
        {
            Console.WriteLine("9.5 млн км^2");
        }
        public string Climate {get; set;}
        public string Name { get; set;}

        public Island(string Climate, string Name)
        {
            this.Climate = Climate;
            this.Name = Name;
        }

        public override void Type()
        {
            Console.WriteLine("Это остров");
        }
        public override string ToString()
        {
            return "Остров";
        }

    }
}
