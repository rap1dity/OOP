namespace laba_12
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Инструкция к использованию --> Перед тем как запускать программу, убедитесь, что в папке Debug отсутствует zip файл, в папке KAVInspect и ExtractedFiles нету файлов,
            // а также то, что вы изменили все пути к директориям и файлам, которые имеют полный путь начиная с диска, такие как C:\\ и подобные.
            // Разрабу было лень делать автоматизацию удаления, так что делаем всё ручками.
            // Забивание на правила могут привести к ошибке компиляции, будьте внимательны!
            DriveInfo[] drives = DriveInfo.GetDrives();
            KAVDiskInfo Disks = new KAVDiskInfo();
            Disks.FreeStorage(drives[0]);
            Disks.FileSystem(drives[1]);
            Disks.DiskFullInfo(drives);
            string PathToFile = "C:\\Users\\rap1dity\\source\\repos\\laba 12\\laba 12\\bin\\Debug\\net6.0\\kavlogfile.txt";
            FileInfo fi = new FileInfo(PathToFile);
            KAVFileInfo file = new KAVFileInfo();
            file.FullPath(fi);
            file.ExtendedInfo(fi);
            file.OpenAndCloseInfo(fi);
            string dirPath = "C:\\Users\\rap1dity\\source\\repos\\laba 12\\laba 12\\bin\\Debug\\net6.0";
            DirectoryInfo dir = new DirectoryInfo(dirPath);
            KAVDirInfo dirInfo = new KAVDirInfo();
            dirInfo.FileAmount(dir);
            dirInfo.GetCreationDate(dir);
            dirInfo.GetSubDirectoriesCount(dir);
            dirInfo.GetParentDirectories(dir);
            KAVFileManager manager = new KAVFileManager();
            manager.GetFilesAndFolders(dir);
            DirectoryInfo dir2 = new DirectoryInfo("C:\\Users\\rap1dity\\PycharmProjects\\update");
            manager.CopyFilesToFolder(dir, dir2, "*.py");
            manager.ArchiveFiles(dir);
            var destination = new DirectoryInfo("C:\\Users\\rap1dity\\source\\repos\\laba 12\\laba 12\\bin\\Debug\\net6.0\\ExtractedFiles");
            manager.ExtractFiles(dir, destination);
            KAVLog.RecordsForDay(26);
            KAVLog.RecordsInTime(23, 24);
            KAVLog.FindByKeyword("директории");
        }
    }
}