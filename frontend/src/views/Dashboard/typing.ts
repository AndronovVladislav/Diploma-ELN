export enum ExperimentKind {
    LABORATORY = 'Лабораторный',
    COMPUTATIONAL = 'Вычислительный',
    ANY = 'Любой'
}

export interface Experiment {
    id: string;
    path: string;
    createdAt: string;

    kind: ExperimentKind;
}

export interface Folder {
    id: string;
    path: string;

    children: FileSystemItem[];
}

export interface Template {
    id: string;
    path: string;

    input: string;
    output: string;
    parameters: string;
    context: string;
}

export type SimplifiedView = Pick<Experiment | Folder, 'id' | 'path'>;
export type FileSystemItem = Folder | Experiment | Template;
export type FileSystem = FileSystemItem[];
