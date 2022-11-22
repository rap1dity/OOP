namespace laba_12
{
    public class KAVDirInfo
    {
        public void FileAmount(DirectoryInfo dir)
        {
            Console.WriteLine($"Количество файлов в директории: {dir.GetFiles().Length}");
            KAVLog.RecordToFile($"Получено количество файлов в директории {dir.Name}");
        }
        public void GetCreationDate(DirectoryInfo dir)
        {
            Console.WriteLine($"Дата создания директории: {dir.CreationTime}");
            KAVLog.RecordToFile($"Были получены данные о дате создания директории {dir.Name}");
        }
        public void GetSubDirectoriesCount(DirectoryInfo dir)
        {
            Console.WriteLine($"Количество поддиректорий: {dir.GetDirectories().Length}");
            KAVLog.RecordToFile($"Получено количество поддидректорий в директории {dir.Name}");
        }
        public void GetParentDirectories(DirectoryInfo dir)
        {
            string[] directories = dir.FullName.Split('\\');
            var parentDirectories = new List<string>();
            for(int i =1;i<directories.Length;i++)
            {
                parentDirectories.Add(directories[i]);
            }
            Console.WriteLine($"Список родительских директорий {string.Join(',',parentDirectories)}");
            KAVLog.RecordToFile($"Получен список родительских поддиректорий у директории {dir.Name}");
        }
    }
}
