namespace laba_13
{
    [Serializable]
    public class Island : Land
    {
        public override string Population => "730 Млн";
        public override void GetPopulation()
        {
            Console.WriteLine("как же я хочу пойти спать 0_o");
        }
        public override void Area()
        {
            Console.WriteLine("9.5 млн км^2");
        }
        public string Climate { get; set; }
        public string Name { get; set; }
        public Island(string Climate, string Name)
        {
            this.Climate = Climate;
            this.Name = Name;
        }
        public Island() { }
        [NonSerialized]
        public int Celsius;


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
