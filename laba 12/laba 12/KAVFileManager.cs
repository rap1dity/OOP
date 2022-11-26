using System.IO.Compression;

namespace laba_12
{
    public class KAVFileManager
    {
        public void GetFilesAndFolders(DirectoryInfo dir)
        {
            var files = dir.GetFiles();
            var subDirectories = dir.GetDirectories();
            var result = new List<string>();
            foreach ( var file in files ) {
                result.Add(file.Name);
            }
            foreach (var sub in subDirectories)
            {
                result.Add(sub.Name);
            }
            Console.WriteLine($"Список файлов и папок: {string.Join(',', result)}");
            if (!dir.Exists)
            {
                dir.Create();
            }
            dir.CreateSubdirectory("KAVInspect");
            using(StreamWriter sw = new StreamWriter(dir.FullName + "\\KAVInspect\\kavdirinfo.txt"))
            {
                sw.WriteLine(string.Join(',', result));
            }
            File.Copy(dir.FullName + "\\KAVInspect\\kavdirinfo.txt", dir.FullName + "\\KAVInspect\\kavdirinfoCopied.txt");
            FileInfo fileRename = new FileInfo(dir.FullName + "\\KAVInspect\\kavdirinfoCopied.txt");
            File.Move(fileRename.FullName, dir.FullName + "\\KAVInspect\\renamedkavdirinfo.txt");
            File.Delete(dir.FullName + "\\KAVInspect\\kavdirinfo.txt");
            KAVLog.RecordToFile($"Записан новый файл по пути {dir.FullName + "\\KAVInspect\\kavdirinfo.txt"}");
        }
        public void CopyFilesToFolder(DirectoryInfo dir, DirectoryInfo SourcePath, string extension)
        {
            dir.CreateSubdirectory("KAVFiles");
            foreach (var item in SourcePath.GetFiles(extension))
            {
                File.Copy(item.FullName, dir + $"\\KAVFiles\\{item.Name}");
            }
            Directory.Move(dir + "\\KAVFiles", dir + "\\KAVInspect\\KAVFiles");
        }
        public void ArchiveFiles(DirectoryInfo dir)
        {
            ZipFile.CreateFromDirectory(dir.FullName, dir.FullName + ".zip");
            Console.WriteLine($"Создан архив из директории по пути: {dir.FullName}");
            KAVLog.RecordToFile($"Создан архив по пути: {dir.FullName}");
        }
        public void ExtractFiles(DirectoryInfo dir, DirectoryInfo destination) 
        {
            ZipFile.ExtractToDirectory(dir.FullName + ".zip", destination.FullName);
            Console.WriteLine($"Разохривирован архив по пути: {dir.FullName + ".zip"}");
            KAVLog.RecordToFile($"Разорхивирован архив по пути: {dir.FullName}");
        }
    }
}
