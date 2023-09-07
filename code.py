import os
import shutil

path = str(input(" Шлях до папки ==> "))

def normalize(name):
    return ''.join(c for c in name if c.isalnum() or c in [' ', '.', '_']).rstrip()


def sort_files_by_extension(path):

    extensions = {
        'images': ('.jpg', '.png', '.jpeg', '.svg'),
        'videos': ('.avi', '.mp4', '.mov', '.mkv'),
        'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
        'music': ('.mp3', '.ogg', '.wav', '.amr'),
        'archives': ('.zip', '.gz', '.tar')
    }

    unknown_extensions = set()

    for root, dirs, files in os.walk(path):
        for folder in dirs:
            if folder.lower() in extensions.keys():
                dirs.remove(folder)

        for file in files:
            filename, extension = os.path.splitext(file)
            found = False
            for folder, exts in extensions.items():
                if extension.lower() in exts:
                    new_path = os.path.join(root, folder, normalize(file))
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    shutil.move(os.path.join(root, file), new_path)
                    found = True
                    break
            if not found:
                unknown_extensions.add(extension.lower())

    for folder in ['archives']:
        for root, dirs, files in os.walk(os.path.join(path, folder)):
            for file in files:
                filename, extension = os.path.splitext(file)
                if extension.lower() == '.zip':
                    new_folder = os.path.join(root, normalize(filename))
                    os.makedirs(new_folder, exist_ok=True)
                    shutil.unpack_archive(os.path.join(root, file), new_folder)
                    os.remove(os.path.join(root, file))

    print('Known extensions:')
    for folder, exts in extensions.items():
        if folder != 'archives':
            print(f'{folder}: {", ".join(exts)}')
   
    print('Unknown extensions:')
    print(', '.join(unknown_extensions))


sort_files_by_extension(path)