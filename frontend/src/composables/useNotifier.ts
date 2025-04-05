import { useToast } from 'primevue/usetoast';

class Notifier {
    private static toast;

    static init() {
        if (!Notifier.toast) {
            Notifier.toast = useToast();
        }
    }

    static success(summary: string = 'Выполнено', detail: string = '') {
        Notifier.toast.add({ severity: 'success', summary, detail, life: 2000 });
    }

    static error(summary: string = 'Ошибка', detail: string = '') {
        Notifier.toast.add({ severity: 'error', summary, detail, life: 4000 });
    }

    static info(summary: string = 'Информация', detail: string = '') {
        Notifier.toast.add({ severity: 'info', summary, detail, life: 2000 });
    }

    static warn(summary: string = 'Предупреждение', detail: string = '') {
        Notifier.toast.add({ severity: 'warn', summary, detail, life: 3000 });
    }
}

export function useNotifier() {
    Notifier.init();
    return Notifier;
}
