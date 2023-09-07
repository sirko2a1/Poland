import os
import shutil

class FileSorter:
    def __init__(self, path):
        self.path = path
        self.extensions = {
            'images': ('.jpg', '.png', '.jpeg', '.svg'),
            'videos': ('.avi', '.mp4', '.mov', '.mkv'),
            'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
            'music': ('.mp3', '.ogg', '.wav', '.amr'),
            'archives': ('.zip', '.gz', '.tar')
        }
        self.unknown_extensions = set()

    def normalize(self, name):
        return ''.join(c for c in name if c.isalnum() or c in [' ', '.', '_']).rstrip()

    def sort_files(self):
        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                if folder.lower() in self.extensions.keys():
                    dirs.remove(folder)

            for file in files:
                filename, extension = os.path.splitext(file)
                found = False
                for folder, exts in self.extensions.items():
                    if extension.lower() in exts:
                        new_path = os.path.join(root, folder, self.normalize(file))
                        os.makedirs(os.path.dirname(new_path), exist_ok=True)
                        shutil.move(os.path.join(root, file), new_path)
                        found = True
                        break
                if not found:
                    self.unknown_extensions.add(extension.lower())

        for folder in ['archives']:
            for root, dirs, files in os.walk(os.path.join(self.path, folder)):
                for file in files:
                    filename, extension = os.path.splitext(file)
                    if extension.lower() == '.zip':
                        new_folder = os.path.join(root, self.normalize(filename))
                        os.makedirs(new_folder, exist_ok=True)
                        shutil.unpack_archive(os.path.join(root, file), new_folder)
                        os.remove(os.path.join(root, file))

    def print_results(self):
        print('Known extensions:')
        for folder, exts in self.extensions.items():
            print(f'{folder}: {", ".join(exts)}')
        print('Unknown extensions:')
        print(', '.join(self.unknown_extensions))

if __name__ == "__main__":
    path = str(input("Шлях до папки ==> "))
    sorter = FileSorter(path)
    sorter.sort_files()
    sorter.print_results()
