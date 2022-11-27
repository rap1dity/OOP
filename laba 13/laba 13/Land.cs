namespace laba_13
{
    [Serializable]
    public abstract class Land : IGetPopulation
    {
        public abstract string Population { get; }
        abstract public void Area();
        abstract public void Type();
        public abstract void GetPopulation();
        public override string ToString() => "Суша";
    }
}
