using System.Text.Json.Serialization;

namespace laba_11
{
    public class TestingClass : ITestingInterface
    {
        [JsonPropertyName("Name")]
        public string? Name;
        [JsonPropertyName("Key")]
        public int Key { get; set; }
        private TestingClass() { } // Отключаем конструктор по умолчанию создавая приватный конструктор без параметров
        public TestingClass(int key) { Key = key; }
        public string TestingString(string str)
        {
            return "Hello" + str;
        }
    }
}
