namespace laba_12
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //DriveInfo[] drives = DriveInfo.GetDrives();
            //KAVDiskInfo Disks = new KAVDiskInfo();
            //Disks.FreeStorage(drives[0]);
            //Disks.FileSystem(drives[1]);
            //Disks.DiskFullInfo(drives);
            //string PathToFile = "C:\\Users\\rap1dity\\source\\repos\\laba 12\\laba 12\\bin\\Debug\\net6.0\\kavlogfile.txt";
            //FileInfo fi = new FileInfo(PathToFile);
            //KAVFileInfo file = new KAVFileInfo();
            //file.FullPath(fi);
            //file.ExtendedInfo(fi);
            //file.OpenAndCloseInfo(fi);
            string dirPath = "C:\\Users\\rap1dity\\source\\repos\\laba 12\\laba 12\\bin\\Debug\\net6.0";
            DirectoryInfo dir = new DirectoryInfo(dirPath);
            //KAVDirInfo dirInfo = new KAVDirInfo();
            //dirInfo.FileAmount(dir);
            //dirInfo.GetCreationDate(dir);
            //dirInfo.GetSubDirectoriesCount(dir);
            //dirInfo.GetParentDirectories(dir);
            KAVFileManager manager = new KAVFileManager();
            //manager.GetFilesAndFolders(dir);
            DirectoryInfo dir2 = new DirectoryInfo("C:\\Users\\rap1dity\\PycharmProjects\\update");
            manager.CopyFilesToFolder(dir, dir2, "*.py");
        }
    }
}