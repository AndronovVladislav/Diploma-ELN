import { FileSystem, FileSystemItem, Folder, SimplifiedView } from '@/views/Dashboard/typing';
import { Optional } from '@/typing';

const traverse = (result: SimplifiedView[], folder: Folder) => {
    let found = false;

    if (!folder.children.length) {
        if (!result.some(project => project.id == folder.id)) {
            result.push({ id: folder.id, path: folder.path });
            found = true;
        }
    }

    for (const child of folder.children) {
        if ('kind' in child) {
            if (!result.some(project => project.id == folder.id)) {
                result.push({ id: folder.id, path: folder.path });
                found = true;

            }
        }

        if ('children' in child && traverse(result, child as Folder)) {
            if (!result.some(project => project.id == folder.id)) {
                result.push({ id: folder.id, path: folder.path });
                found = true;
            }
        }
    }

    return found;
};

export const findById = (folders: FileSystem, id: string): Optional<FileSystemItem> => {
    for (const folder of folders) {
        if (folder.id === id) {
            return folder;
        }
        if ('children' in folder) {
            const found = findById(folder.children as FileSystem, id);
            if (found) return found;
        }
    }
    return null;
};

export const findParent = (root: FileSystem, childId: string): Optional<Folder> => {
    for (const folder of root) {
        if ('children' in folder) {
            if (folder.children.some(child => child.id === childId)) {
                return folder;
            }
            const parent = findParent(folder.children as FileSystem, childId);
            if (parent) return parent;
        }
    }
    return null;
};

export const removeFromFS = (fs: FileSystem, id: string): boolean => {
    for (const child of fs) {
        if ('children' in child) {
            const index = child.children.findIndex((item: FileSystemItem) => item.id === id);
            if (index !== -1) {
                child.children.splice(index, 1);
                return true;
            } else {
                if (removeFromFS(child.children as Folder[], id)) return true;
            }
        } else {
            if (child.id === id) {
                fs.splice(fs.indexOf(child), 1);
                return true;
            }
        }
    }
    return false;
};

export const getFullPath = (fs: FileSystem, item: SimplifiedView): string => {
    const parent = findParent(fs, item.id);
    return parent ? `${getFullPath(fs, { id: parent.id, path: parent.path })}/${item.path}` : `${item.path}`;
};

export const getSuggestedFolders = (fs: FileSystem): SimplifiedView[] => {
    const result: SimplifiedView[] = [];

    fs.filter(item => 'children' in item).forEach(folder => traverse(result, folder));
    return result;
};
