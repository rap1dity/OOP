namespace laba_12
{
    public class KAVDiskInfo
    {
        public void FreeStorage(DriveInfo drive)
        {
            Console.WriteLine($"Свободного места на диске: {drive.AvailableFreeSpace}");
            KAVLog.RecordToFile($"Проверено свободное место на диске: {drive.Name}");
        }
        public void FileSystem(DriveInfo drive)
        {
            Console.WriteLine($"Имя файловой системы: {drive.DriveFormat}\nТип диска: {drive.DriveType}");
            KAVLog.RecordToFile($"Проверена информация о файловой системе: {drive.Name}");
        }
        public void DiskFullInfo(DriveInfo[] drives)
        {
            string names = "";
            foreach (var drive in drives)
            {
                Console.WriteLine($"Имя диска: {drive.Name}\nОбъём диска: {drive.TotalSize}\nДоступный объём: {drive.AvailableFreeSpace}\nМетка тома: {drive.VolumeLabel}");
                names += drive.Name + ' ';
            }
            KAVLog.RecordToFile($"Проверена полная информация о дисках: {names}");
        }
    }
}
