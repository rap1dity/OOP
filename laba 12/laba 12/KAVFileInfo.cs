namespace laba_12
{
    public class KAVFileInfo
    {
        public void FullPath(FileInfo file)
        {
            Console.WriteLine($"Полный путь к файлу: {file.FullName}");
            KAVLog.RecordToFile($"Извлечен полный путь к файлу: {file.Name}");
        }
        public void ExtendedInfo(FileInfo file)
        {
            Console.WriteLine($"Размер файла: {file.Length}\nРасширение файла: {file.Extension}\nИмя файла: {file.Name}");
            KAVLog.RecordToFile($"Были получены данные о размере, расширении и имени файла по пути: {file.FullName}");
        }
        public void OpenAndCloseInfo(FileInfo file)
        {
            Console.WriteLine($"Дата создания файла: {file.CreationTime}\nДата последнего изменения файла: {file.LastWriteTime}");
            KAVLog.RecordToFile($"Были получены данные о дате создания и изменения файла по пути: {file.FullName}");
        }
    }
}
